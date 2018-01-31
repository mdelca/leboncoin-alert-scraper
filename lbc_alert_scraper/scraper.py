# coding: utf-8
import os
import requests

from datetime import datetime

from lxml import html

from lbc_alert_scraper.offer import Offer

OFFER_XPATH = '//li[@itemtype="http://schema.org/Offer"]'


class LBCScraper(object):
    name = None
    request = None
    last_alert_dtt = None
    last_alert_file = None
    last_offers_elements = None

    def __init__(self, config, logger, name, request):
        """
        Initialize scrapper. Creating last_alert_* file
        Initialisation du "scrapper", création du fichier last_alert_* qui va
        permettre de sauvegarder l'heure de la dernière annonce récupérée
        """
        self.config = config
        self.logger = logger
        self.name = name
        self.request = request
        self.last_offers_elements = []

        data_dir = config.get('global', 'data_dir')

        self.last_alert_file = os.path.join(data_dir, 'last_alert_%s.txt' % self.name)

        if not os.path.exists(self.last_alert_file):
            logger.info('first execution: creating data file')
            self.save_last_alert_dtt()
            self.last_alert_dtt = datetime.now()
        else:
            with open(self.last_alert_file, 'r') as file_:
                self.last_alert_dtt = datetime.strptime(file_.read().strip(), '%Y-%m-%d %H:%M')

        self.logger.info('new scraper for %s (last offer catching up at %s)', self.request, self.last_alert_dtt)

    def get_last_offers(self):
        self.logger.info('getting last offers')
        page = requests.get(self.request)
        if page.status_code == 404:
            self.logger.info('404 : bad url')
            return
        tree = html.fromstring(page.content)
        for offer_el in tree.xpath(OFFER_XPATH):
            offer = Offer(offer_el)
            if offer.dtt_publish > self.last_alert_dtt:
                self.last_offers_elements.append(offer)

        self.logger.info('%s new offers since last execution', len(self.last_offers_elements))
        return self.last_offers_elements

    def save_last_alert_dtt(self):
        dtt = datetime.now()
        with open(self.last_alert_file, 'w') as file_:
            file_.write(dtt.strftime('%Y-%m-%d %H:%M'))

        self.logger.info('updating data file with : %s', dtt)
