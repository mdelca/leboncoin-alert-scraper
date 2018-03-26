import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults

from database.models import Alert, Subscription, User

from lbc_scraper_admin.utils import check_url


@view_defaults(route_name='alerts', renderer='../templates/alerts.pt')
class AlertView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_alerts(self, message=None):
        id_user = int(self.request.matchdict['id_user'])
        self.logger.info('request : alerts for user %s', id_user)
        user = self.request.dbsession.query(User).filter_by(id_user=id_user).one()
        alerts = self.request.dbsession.query(Alert).join(Subscription)\
            .filter(Subscription.id_user == id_user).all()
        self.logger.info('%s alerts available for user %s', len(alerts), user.name)
        return {'alerts': alerts, 'user': user, 'message': message}

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
        id_user = int(self.request.matchdict['id_user'])
        user = self.request.dbsession.query(User).filter_by(id_user=id_user).one()
        return {'user': user, 'message': message}

    @view_config(request_method='GET')
    def get(self):
        return self.get_new_alert_form()

    @view_config(request_method='POST')
    def post(self):
        if 'add' in self.request.params:
            name = self.request.POST['name'].strip()
            url = self.request.POST['url'].strip()
            id_user = int(self.request.matchdict['id_user'])

            if not (url or name):
                return self.get_new_alert_form(message="Tous les champs sont obligatoires")

            result = check_url(url)
            if not result.is_valid:
                return self.get_new_alert_form(message=result.message)

            self.add_new_alert(name, url, id_user)

        return HTTPFound(location=self.request.route_url('alerts', id_user=id_user))

    def add_new_alert(self, name, url, id_user):
        self.logger.info('request : add new alert (%s) for user %s', url, id_user)

        user = self.request.dbsession.query(User).filter_by(id_user=id_user).one()

        new_alert = Alert(name=name, url=url)
        new_subscription = Subscription(alert=new_alert, user=user)

        self.request.dbsession.add(new_subscription)


@view_defaults(route_name='alert', renderer='../templates/alert.pt')
class AlertsView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    def get_alert(self, message=None):
        id_alert = int(self.request.matchdict['id_alert'])
        id_user = int(self.request.matchdict['id_user'])

        alert = self.request.dbsession.query(Alert).filter_by(id_alert=id_alert).one()
        user = self.request.dbsession.query(User).filter_by(id_user=id_user).one()
        return {'alert': alert, 'user': user, 'message': message}

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
            id_user = int(self.request.matchdict['id_user'])

            if not (url or name):
                return self.get_alert(message="Tous les champs sont obligatoires")

            result = check_url(url)
            if not result.is_valid:
                return self.get_alert(message=result.message)

            self.update_alert(id_alert, name, url)

            return HTTPFound(location=self.request.route_url('alerts', id_user=id_user))
