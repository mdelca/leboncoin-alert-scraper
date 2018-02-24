from pyramid.view import view_config, view_defaults
from lbc_scraper.models import Recipient, Alert, Subscription


@view_defaults(route_name='main', renderer='template.pt')
class AdminView(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        recipients = self.request.dbsession.query(Recipient).all()
        for recipient in recipients:
            recipient.alerts = [subscription.alert for subscription in recipient.subscriptions]
        return {'recipients': recipients}

    @view_config(request_method='POST')
    def post(self):
        name = self.request.POST['name']
        url = self.request.POST['url']
        id_recipient = self.request.POST['id_recipient']
        recipient = self.request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()

        new_alert = Alert(name=name, url=url)
        new_subscription = Subscription(alert=new_alert, recipient=recipient)

        self.request.dbsession.add(new_subscription)
        recipients = self.request.dbsession.query(Recipient).all()
        for recipient in recipients:
            recipient.alerts = [subscription.alert for subscription in recipient.subscriptions]
        return {'recipients': recipients}
