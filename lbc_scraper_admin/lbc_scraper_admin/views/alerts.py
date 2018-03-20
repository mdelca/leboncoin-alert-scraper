import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults

from lbc_scraper.models import Alert, Subscription, Recipient

from lbc_scraper_admin.utils import check_url


@view_defaults(route_name='alerts', renderer='../templates/alerts.pt')
class AlertView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_alerts(self, message=None):
        id_recipient = int(self.request.matchdict['id_user'])
        self.logger.info('request : alerts for user %s', id_recipient)
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()
        alerts = self.request.dbsession.query(Alert).join(Subscription)\
            .filter(Subscription.id_recipient == id_recipient).all()
        self.logger.info('%s alerts available for user %s', len(alerts), recipient.name)
        return {'alerts': alerts, 'recipient': recipient, 'message': message}

    def delete_alert(self, id_alert):
        self.logger.info('request : delete alert %s', id_alert)
        alert = self.request.dbsession.query(Alert).filter_by(id_alert=id_alert).one()
        self.request.dbsession.delete(alert)

    @view_config(request_method='GET')
    def get(self):
        return self.get_alerts()

    @view_config(request_method='POST')
    def post(self):

        if 'delete' in self.request.params:
            id_alert = self.request.POST['id_alert']
            self.delete_alert(id_alert)
        return self.get_alerts()


@view_defaults(route_name='new_alert', renderer='../templates/new_alert.pt')
class NewAlertView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_new_alert_form(self, message=None):
        id_recipient = int(self.request.matchdict['id_user'])
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()
        return {'recipient': recipient, 'message': message}

    @view_config(request_method='GET')
    def get(self):
        return self.get_new_alert_form()

    @view_config(request_method='POST')
    def post(self):
        if 'add' in self.request.params:
            name = self.request.POST['name'].strip()
            url = self.request.POST['url'].strip()
            id_recipient = int(self.request.matchdict['id_user'])

            if not (url or name):
                return self.get_new_alert_form(message="Tous les champs sont obligatoires")

            result = check_url(url)
            if not result.is_valid:
                return self.get_new_alert_form(message=result.message)

            self.add_new_alert(name, url, id_recipient)

        return HTTPFound(location=self.request.route_url('alerts', id_user=id_recipient))

    def add_new_alert(self, name, url, id_recipient):
        self.logger.info('request : add new alert (%s) for user %s', url, id_recipient)

        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()

        new_alert = Alert(name=name, url=url)
        new_subscription = Subscription(alert=new_alert, recipient=recipient)

        self.request.dbsession.add(new_subscription)


@view_defaults(route_name='alert', renderer='../templates/alert.pt')
class AlertsView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_alert(self, message=None):
        id_alert = int(self.request.matchdict['id_alert'])
        id_recipient = int(self.request.matchdict['id_user'])

        alert = self.request.dbsession.query(Alert).filter_by(id_alert=id_alert).one()
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()
        return {'alert': alert, 'recipient': recipient, 'message': message}

    def update_alert(self, id_alert, name, url):
        self.logger.info('request : updating alert (%s) with name=%s, url=%s', id_alert, name, url)

        alert = self.request.dbsession.query(Alert).filter_by(id_alert=id_alert).one()
        alert.name = name
        alert.url = url

        self.request.dbsession.add(alert)

    @view_config(request_method='GET')
    def get(self):
        return self.get_alert()

    @view_config(request_method='POST')
    def post(self):
        if 'update' in self.request.params:
            name = self.request.POST['name'].strip()
            url = self.request.POST['url'].strip()
            id_alert = int(self.request.matchdict['id_alert'])
            id_recipient = int(self.request.matchdict['id_user'])

            if not (url or name):
                return self.get_alert(message="Tous les champs sont obligatoires")

            result = check_url(url)
            if not result.is_valid:
                return self.get_alert(message=result.message)

            self.update_alert(id_alert, name, url)

            return HTTPFound(location=self.request.route_url('alerts', id_user=id_recipient))
