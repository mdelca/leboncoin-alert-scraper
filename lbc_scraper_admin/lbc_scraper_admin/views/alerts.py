import logging

from pyramid.view import view_config, view_defaults

from lbc_scraper.models import Alert, Subscription, Recipient


@view_defaults(route_name='alerts', renderer='../templates/alerts.pt')
class AlertView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_alerts(self):
        id_recipient = int(self.request.matchdict['id_user'])
        self.logger.info('request : alerts for user %s', id_recipient)
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()
        alerts = self.request.dbsession.query(Alert).join(Subscription)\
            .filter(Subscription.id_recipient==id_recipient).all()
        self.logger.info('%s alerts available for user %s', len(alerts), recipient.name)
        return {'alerts': alerts, 'recipient': recipient}

    def add_new_alert(self, name, url, id_recipient):
        self.logger.info('request : add new alert (%s) for user %s', url, id_recipient)

        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()

        new_alert = Alert(name=name, url=url)
        new_subscription = Subscription(alert=new_alert, recipient=recipient)

        self.request.dbsession.add(new_subscription)

    def delete_alert(self, id_alert):
        self.logger.info('request : delete alert %s', id_alert)
        alert = self.request.dbsession.query(Alert).filter_by(id_alert=id_alert).one()
        self.request.dbsession.delete(alert)

    @view_config(request_method='GET')
    def get(self):
        return self.get_alerts()

    @view_config(request_method='POST')
    def post(self):
        if 'add' in self.request.params:
            name = self.request.POST['name']
            url = self.request.POST['url']
            id_recipient = int(self.request.matchdict['id_user'])

            self.add_new_alert(name, url, id_recipient)

        if 'delete' in self.request.params:
            id_alert = self.request.POST['id_alert']
            self.delete_alert(id_alert)
        return self.get_alerts()
