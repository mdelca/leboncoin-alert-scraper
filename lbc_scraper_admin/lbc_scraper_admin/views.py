from pyramid.view import view_config
from lbc_scraper.models import Recipient


@view_config(route_name='main', renderer='template.pt')
def main_view(request):
    recipients = request.dbsession.query(Recipient).all()
    for recipient in recipients:
        recipient.alerts = [subscription.alert for subscription in recipient.subscriptions]
    return {'recipients': recipients}
