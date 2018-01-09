#!/usr/local/bin/python
# coding: utf-8

import os
import shutil
import argparse
from configparser import RawConfigParser

import logging.config

from datetime import datetime

from lxml import html
import requests, time

from lbc_alert_scraper import email_me, utils
from lbc_alert_scraper.offer import Offer

OFFER_XPATH = '//li[@itemtype="http://schema.org/Offer"]'


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file', default='/etc/lbc_scraper.ini')
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

    for alert_name, alert_url in alert_sections.items():
        # Load html page
        logger.info('treating %s : %s', alert_name, alert_url)
        page = requests.get(alert_url)
        if page.status_code == 404:
            logger.info('404 : bad url')
            continue
        tree = html.fromstring(page.content)
        offer_elements = [Offer(lxml_element) for lxml_element in tree.xpath(OFFER_XPATH)]

        f_path = os.path.join(data_dir, 'last_alert_%s.txt' % alert_name)

        if not os.path.exists(f_path):
            # first execution, we just keep datetime of most recent ad
            logger.info('first execution: creating file')
            if offer_elements:
                last_alert_dtt = offer_elements[0].dtt_publish
            else:
                last_alert_dtt = datetime.now()
            with open(f_path, 'a') as file_:
                file_.write(last_alert_dtt.strftime('%Y-%m-%d %H:%M'))
            continue

        # Read last alert time
        last_alert_dtt = datetime.strptime(utils.read_file(f_path), '%Y-%m-%d %H:%M')
        logger.info('last alert detected : %s', last_alert_dtt)

        ### This algorithm is based on the date of the post
        ### Also, I had to do lots of sketchy conditions to get the element I wanted
        ### maybe there's a better way to scrap this data, feel free to improve it !
        for offer in reversed(offer_elements):
            logger.debug('offer published at %s', offer.dtt_publish)

            if offer.dtt_publish > last_alert_dtt:
                logger.info("Alerte %s ! Nouvelle annonce detectée à : %s (%s)", alert_name, time.strftime('%H:%M:%S'), offer.link)
                if alert_name not in new_offers:
                    new_offers[alert_name] = []
                new_offers[alert_name].append(offer)
                # Save the new alert hour
                utils.write_to_file(f_path, offer.dtt_publish.strftime('%Y-%m-%d %H:%M'))
                logger.info("saving new last_alert_time : %s", offer.dtt_publish)

        logger.info('%s new offer(s)', len(new_offers))
    if new_offers:
        # Here I'm sending an email but you can do whatever you want, for exemple connect it to IFTTT maker channel, or send you a tweet
        # Send the email
        email_me.send_email(logger, config['server_mail'], new_offers)

    logger.info('ending process')


if __name__ == "__main__":
    start_scraper()
