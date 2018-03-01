import logging

from pyramid.view import view_config, view_defaults

from lbc_scraper.models import Recipient


@view_defaults(route_name='users', renderer='../templates/users.pt')
class UserView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    @view_config(request_method='GET')
    def get(self):
        recipients = self.request.dbsession.query(Recipient).all()
        self.logger.info('%s recipients', len(recipients))
        return {'recipients': recipients}
