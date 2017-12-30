#!/usr/local/bin/python
# coding: utf-8

import os
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
    return parser


def get_config(config_filepath):
    config = RawConfigParser()
    config.read(config_filepath)
    return config


def start_scraper():

    parser = create_parser()

    args = parser.parse_args()

    config_file = os.path.join(os.getcwd(), args.config)

    config = get_config(config_file)

    data_dir = config.get('global', 'data_dir')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    logging.config.fileConfig(config_file)
    logger = logging.getLogger('scrapper')

    # Iterate over all URLS from config
    alert_sections = [section for section in config.sections() if section.startswith('alert')]
    logger.info('starting process: %s request to treat', len(alert_sections))
    for alert_section in alert_sections:
        # Load html page
        alert_name = alert_section.lstrip('alert_')
        url = config.get(alert_section, 'url')
        logger.info('treating %s : %s', alert_name, url)
        page = requests.get(url)
        if page.status_code == 404:
            logger.info('404 : bad url')
            continue
        tree = html.fromstring(page.content)
        offer_elements = [Offer(lxml_element) for lxml_element in tree.xpath(OFFER_XPATH)]

        f_path = os.path.join(data_dir, 'last_alert_%s.txt' % alert_name)

        if not os.path.exists(f_path):
            # first execution, we just keep datetime of most recent ad
            logger.info('first execution: creating file')
            with open(f_path, 'a') as file_:
                file_.write(offer_elements[0].dtt_publish.strftime('%Y-%m-%d %H:%M'))
            break

        # Read last alert time
        last_alert_dtt = datetime.strptime(utils.read_file(f_path), '%Y-%m-%d %H:%M')
        logger.info('last alert detected : %s', last_alert_dtt)

        ### This algorithm is based on the date of the post
        ### Also, I had to do lots of sketchy conditions to get the element I wanted
        ### maybe there's a better way to scrap this data, feel free to improve it !
        new_offers = []
        for offer_element in reversed(offer_elements):
            logger.debug('offer published at %s', offer_element.dtt_publish)

            if offer_element.dtt_publish > last_alert_dtt:
                new_offers.append(offer_element)
                link = offer_element.lxml_element.xpath('a')[0].attrib['href']
                logger.info("Alerte %s ! Nouvelle annonce detectée à : %s (%s)", alert_name, time.strftime('%H:%M:%S'), link)
                # Here I'm sending an email but you can do whatever you want, for exemple connect it to IFTTT maker channel, or send you a tweet
                # Send the email
                email_me.send_email(config['server_mail'], "Alerte "+ alert_name +" !", "Nouvelle annonce detectée à : " + time.strftime('%H:%M:%S')+".\n"+ link)
                # Save the new alert hour
                utils.write_to_file(f_path, offer_element.dtt_publish.strftime('%Y-%m-%d %H:%M'))
                logger.info("email send, new last_alert_time : %s", offer_element.dtt_publish)

        logger.info('%s new offer(s)', len(new_offers))
    logger.info('ending process')


if __name__ == "__main__":
    start_scraper()
