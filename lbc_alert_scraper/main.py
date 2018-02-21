#!/usr/local/bin/python
# coding: utf-8

import os
import shutil
import argparse
from configparser import RawConfigParser

import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lbc_alert_scraper import email_me
from lbc_alert_scraper.scraper import LBCScraper
from lbc_alert_scraper.models import Base, Alert, Recipient


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file', default='/etc/lbc_scraper/config.ini')
    parser.add_argument('--reset', help='reset', action='store_const', const=True, default=False)
    return parser


def get_config(config_filepath):
    config = RawConfigParser()
    config.read(config_filepath)
    return config


def initialize_data_dir(data_dir, reset=False):
    if os.path.exists(data_dir) and reset:
        shutil.rmtree(data_dir)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)


def initialize_database(config):
    db_file = config.get('global', 'db_url')

    engine = create_engine('sqlite:///%s' % db_file)

    if not os.path.exists(db_file):
        Base.metata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def start_scraper():

    parser = create_parser()

    args = parser.parse_args()

    config_file = os.path.join(os.getcwd(), args.config)

    config = get_config(config_file)

    logging.config.fileConfig(config_file)
    logger = logging.getLogger('scrapper')

    data_dir = config.get('global', 'data_dir')

    initialize_data_dir(data_dir, args.reset)

    session = initialize_database(config)

    alerts = session.query(Alert).all()
    logger.info('starting process: %s request to treat', len(alerts))

    new_offers = {}

    # initialize scrappers
    scrappers = []
    for alert in alerts:
        scrapper = LBCScraper(config, logger, alert.name, alert.url)
        last_offers = scrapper.get_last_offers()
        if last_offers:
            new_offers[scrapper.name] = last_offers
            scrapper.save_last_alert_dtt()

        scrappers.append(scrapper)

    if new_offers:
        # sending notifications
        logger.info('prepare mail notifications')
        recipients = session.query(Recipient).all()
        for recipient in recipients:
            alerts = [subscription.alert.name for subscription in recipient.subscriptions]
            logger.info("treating recipient '%s' (subscriptions: %s)", recipient.email, ', '.join(alerts))
            alerts_to_send = {}
            for alert_name, offers in new_offers.items():
                if alert_name in alerts:
                    alerts_to_send[alert_name] = offers

            if alerts_to_send:
                logger.info("%s alerts to send (%s)", len(alerts_to_send), ', '.join(alerts_to_send.keys()))
                email_me.send_email(logger, config['server_mail'], recipient.email, alerts_to_send)
            else:
                logger.info('no alerts to send')
    else:
        logger.info('no mail to send')

    logger.info('ending process')


if __name__ == "__main__":
    start_scraper()
