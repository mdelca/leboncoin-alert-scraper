import zope.sqlalchemy

from pyramid.config import Configurator

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from lbc_scraper.models import Base


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('.routes')
    config.scan()

    # configure db
    config.include('pyramid_tm')

    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    config.add_static_view('static', 'static', cache_max_age=3600)

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
    return config.make_wsgi_app()
