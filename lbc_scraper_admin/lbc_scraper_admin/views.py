from pyramid.view import view_config
from lbc_scraper.models import Recipient, Alert, Subscription


@view_config(route_name='main', renderer='template.pt')
def main_view(request):
    recipients = request.dbsession.query(Recipient).all()
    for recipient in recipients:
        recipient.alerts = [subscription.alert for subscription in recipient.subscriptions]
    return {'recipients': recipients}


@view_config(route_name='main', renderer='template.pt', request_method='POST')
def add_alert(request):
    name = request.POST['name']
    url = request.POST['url']
    id_recipient = request.POST['id_recipient']
    recipient = request.dbsession.query(Recipient).filter_by(id_recipient=id_recipient).one()

    new_alert = Alert(name=name, url=url)
    new_subscription = Subscription(alert=new_alert, recipient=recipient)

    request.dbsession.add(new_subscription)
    recipients = request.dbsession.query(Recipient).all()
    for recipient in recipients:
        recipient.alerts = [subscription.alert for subscription in recipient.subscriptions]
    return {'recipients': recipients}
