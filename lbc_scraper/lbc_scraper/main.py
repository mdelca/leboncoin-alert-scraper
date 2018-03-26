#!/usr/local/bin/python
# coding: utf-8

import os
import argparse

from configparser import RawConfigParser

import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Alert, User

from lbc_scraper import email_me
from lbc_scraper.scraper import LBCScraper

here = os.path.abspath(os.path.dirname(__file__))


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file')
    parser.add_argument('--reset', help='reset', action='store_const', const=True, default=False)
    return parser


def get_config(config_filepath):
    config = RawConfigParser()
    config.read(config_filepath)
    return config


def initialize_database(config):
    db_file = config.get('global', 'db_url')

    engine = create_engine('sqlite:///%s' % db_file)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def start_scraper():

    parser = create_parser()

    args = parser.parse_args()

    if args.config:
        config_file = os.path.join(os.getcwd(), args.config)
    else:
        config_file = os.path.join(here, '../config.ini')

    config = get_config(config_file)

    logging.config.fileConfig(config_file)
    logger = logging.getLogger('scrapper')

    session = initialize_database(config)

    alerts = session.query(Alert).all()
    logger.info('starting process: %s request to treat', len(alerts))

    new_offers = {}

    # initialize scrappers
    scrappers = []
    for alert in alerts:
        scrapper = LBCScraper(config, logger, session, alert)
        last_offers = scrapper.get_last_offers()
        if last_offers:
            new_offers[alert.name] = last_offers

        scrappers.append(scrapper)

    if new_offers:
        # sending notifications
        logger.info('prepare mail notifications')
        users = session.query(User).all()
        for user in users:
            alerts = [subscription.alert.name for subscription in user.subscriptions]
            logger.info("treating user '%s' (subscriptions: %s)", user.email, ', '.join(alerts))
            alerts_to_send = {}
            for alert_name, offers in new_offers.items():
                if alert_name in alerts:
                    alerts_to_send[alert_name] = offers

            if alerts_to_send:
                logger.info("%s alerts to send (%s)", len(alerts_to_send), ', '.join(alerts_to_send.keys()))
                email_me.send_email(logger, config['server_mail'], user.email, alerts_to_send)
            else:
                logger.info('no alerts to send')
    else:
        logger.info('no mail to send')

    logger.info('ending process')


if __name__ == "__main__":
    start_scraper()
