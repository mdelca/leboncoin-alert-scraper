#!/usr/local/bin/python
# coding: utf-8

import os

import logging
from logging.handlers import RotatingFileHandler

from lxml import html
import requests, re, time
import email_me, utils, settings

DATA_FILEPATH = '/tmp/lbc_alert_scraper'


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
        # Select all <a/> elements by class name
        links_el = tree.xpath('//a[@class="list_item clearfix trackable"]')
        link_index = 0

        f_path = os.path.join(DATA_FILEPATH, 'last_alert_%s.txt' % url)

        if not os.path.exists(f_path):
            logger.info('first execution: creating file')
            open(f_path, 'a')
            break

        # Read last alert time
        last_alert_time = utils.read_file(f_path)
        ### This algorithm is based on the date of the post
        ### Also, I had to do lots of sketchy conditions to get the element I wanted
        ### maybe there's a better way to scrap this data, feel free to improve it !
        for i, el in enumerate(reversed(links_el), start=0):
            # Get date element of ad
            date = el.xpath('.//p[@class="item_supp"]/text()')
            # Get link element of ad
            link = tree.xpath('.//a[@class="list_item clearfix trackable"]/@href')
            day_hour = ''
            for d in date:
                # Remove all useless char from html element
                day_hour = ''.join(map(lambda s: re.sub('\s+', '', s),d ))
            if day_hour != '':
                # We have now someting like : <day>,<hour>:<minute>
                # So we split the string
                splitted_day_hour = day_hour.split(',')
                day = splitted_day_hour[0]
                hour = splitted_day_hour[1]
                if len(splitted_day_hour) == 2:
                    # If the ad is from today
                    if day == "Aujourd'hui":
                        # And is not the same and newer than the last
                        if hour != last_alert_time and hour > last_alert_time:
                            link = link[link_index][2:-8]
                            link_index +=1
                            # Here I'm sending an email but you can do whatever you want, for exemple connect it to IFTTT maker channel, or send you a tweet
                            # Send the email
                            email_me.send_email("Alerte "+ url +" !", "Nouvelle annonce detectée à : " + time.strftime('%H:%M:%S')+".\n"+ link)
                            # Save the new alert hour
                            utils.write_to_file(f_path, hour)
                            logger.info("email send, new last_alert_time : %s", hour)
                else:
                    logger.info('no new ad since last execution')

    logger.info('ending process')
