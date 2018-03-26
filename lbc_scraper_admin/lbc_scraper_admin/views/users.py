import logging

from pyramid.view import view_config, view_defaults

from database.models import User


@view_defaults(route_name='users', renderer='../templates/users.pt')
class UserView(object):

    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger()

    @view_config(request_method='GET')
    def get(self):
        users = self.request.dbsession.query(User).all()
        self.logger.info('%s users', len(users))
        return {'users': users}
