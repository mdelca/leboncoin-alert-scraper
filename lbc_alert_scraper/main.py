#!/usr/local/bin/python
# coding: utf-8

import os
import shutil
import argparse
from configparser import RawConfigParser

import logging.config

from lbc_alert_scraper import email_me
from lbc_alert_scraper.scraper import LBCScraper


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

    return


def start_scraper():

    parser = create_parser()

    args = parser.parse_args()

    config_file = os.path.join(os.getcwd(), args.config)

    config = get_config(config_file)

    logging.config.fileConfig(config_file)
    logger = logging.getLogger('scrapper')

    data_dir = config.get('global', 'data_dir')

    initialize_data_dir(data_dir, args.reset)

    alert_sections = config['alerts']
    logger.info('starting process: %s request to treat', len(alert_sections))

    new_offers = {}

    # initialize scrappers
    scrappers = []
    for alert_name, alert_url in alert_sections.items():
        scrapper = LBCScraper(config, logger, alert_name, alert_url)
        last_offers = scrapper.get_last_offers()
        if last_offers:
            new_offers[scrapper.name] = last_offers
            scrapper.save_last_alert_dtt()

        scrappers.append(scrapper)

    if new_offers:
        # sending notifications
        logger.info('prepare mail notifications')
        recipient_sections = [section for section in config.sections() if section.startswith('recipient_')]
        for recipient_section in recipient_sections:
            recipient = config[recipient_section]['mail'].strip().split('\n')
            alerts = [alert.lower() for alert in config[recipient_section]['alerts'].strip().split('\n')]
            subscribed_alerts = {}
            for alert_name, offers in new_offers.items():
                if alert_name in alerts:
                    subscribed_alerts[alert_name] = offers

            email_me.send_email(logger, config['server_mail'], recipient, subscribed_alerts)
    else:
        logger.info('no mail to send')

    logger.info('ending process')


if __name__ == "__main__":
    start_scraper()
