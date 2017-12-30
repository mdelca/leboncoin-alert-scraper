#!/usr/local/bin/python
# coding: utf-8

import os

import logging
from logging.handlers import RotatingFileHandler

from datetime import datetime

from lxml import html
import requests, time
import email_me, utils, settings

DATA_FILEPATH = '/tmp/lbc_alert_scraper'

OFFER_XPATH = '//li[@itemtype="http://schema.org/Offer"]'

def create_logger():
    logger = logging.getLogger('scrapper')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler('/var/log/lbc_scraper/activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':

    if not os.path.exists(DATA_FILEPATH):
        os.mkdir(DATA_FILEPATH)

    logger = create_logger()
    # Iterate over all URLS from settings
    logger.info('starting process: %s request to treat', len(settings.URLS))

    for url in settings.URLS :
        # Load html page
        logger.info('treating %s : %s', url, settings.URLS[url])
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(settings.URLS[url], headers=headers)
        tree = html.fromstring(page.content)
        offer_elements = tree.xpath(OFFER_XPATH)
        link_index = 0

        f_path = os.path.join(DATA_FILEPATH, 'last_alert_%s.txt' % url)

        if not os.path.exists(f_path):
            # first execution, we just keep datetime of most recent ad
            logger.info('first execution: creating file')
            p_el = offer_elements[0].xpath('a/section/aside/p')[0]
            str_date = p_el.attrib['content']
            str_time = p_el.xpath('text()')[0].strip().split(',')[1].strip()
            with open(f_path, 'a') as file_:
                file_.write('%s %s' % (str_date, str_time))
            break

        # Read last alert time
        last_alert_dtt = datetime.strptime(utils.read_file(f_path), '%Y-%m-%d %H:%M')
        logger.info('last alert detected : %s', last_alert_dtt)

        ### This algorithm is based on the date of the post
        ### Also, I had to do lots of sketchy conditions to get the element I wanted
        ### maybe there's a better way to scrap this data, feel free to improve it !
        new_offers = []
        for offer_element in reversed(offer_elements):
            # Get date element of ad
            p_el = offer_element.xpath('a/section/aside/p')[0]
            str_date = p_el.attrib['content']
            str_time = p_el.xpath('text()')[0].strip().split(',')[1].strip()

            dtt_offer = datetime.strptime('%s %s' % (str_date, str_time), '%Y-%m-%d %H:%M')
            logger.debug('offer published at %s', dtt_offer)

            if dtt_offer > last_alert_dtt:
                new_offers.append(offer_element)
                link = offer_element.xpath('a')[0].attrib['href']
                logger.info("Alerte %s ! Nouvelle annonce detectée à : %s (%s)", url, time.strftime('%H:%M:%S'), link)
                # Here I'm sending an email but you can do whatever you want, for exemple connect it to IFTTT maker channel, or send you a tweet
                # Send the email
                email_me.send_email("Alerte "+ url +" !", "Nouvelle annonce detectée à : " + time.strftime('%H:%M:%S')+".\n"+ link)
                # Save the new alert hour
                utils.write_to_file(f_path, '%s %s' % (str_date, str_time))
                logger.info("email send, new last_alert_time : %s %s", str_date, str_time)

        logger.info('%s new offer(s)', len(new_offers))
    logger.info('ending process')
