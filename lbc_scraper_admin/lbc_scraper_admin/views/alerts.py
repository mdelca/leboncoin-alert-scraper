from pyramid.view import view_config, view_defaults
from lbc_scraper.models import Alert, Subscription, Recipient


@view_defaults(route_name='alerts', renderer='../templates/alerts.pt')
class AlertView(object):

    def __init__(self, request):
        self.request = request

    def get_alerts(self):
        id_recipient = int(self.request.matchdict['id_user'])
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()
        alerts = self.request.dbsession.query(Alert).join(Subscription)\
            .filter(Subscription.id_recipient==id_recipient).all()
        return {'alerts': alerts, 'recipient': recipient}

    @view_config(request_method='GET')
    def get(self):
        return self.get_alerts()

    @view_config(request_method='POST')
    def post(self):
        name = self.request.POST['name']
        url = self.request.POST['url']
        id_recipient = int(self.request.matchdict['id_user'])

        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()

        new_alert = Alert(name=name, url=url)
        new_subscription = Subscription(alert=new_alert, recipient=recipient)

        self.request.dbsession.add(new_subscription)
        return self.get_alerts()
