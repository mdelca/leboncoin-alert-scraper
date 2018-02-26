# coding: utf-8
import requests

from lxml import html

from lbc_scraper.offer import Offer

OFFER_XPATH = '//li[@itemtype="http://schema.org/Offer"]'


class LBCScraper(object):
    alert = None
    last_offers_elements = None

    def __init__(self, config, logger, alert):
        """
        Initialize scrapper. Creating last_alert_* file
        Initialisation du "scrapper", création du fichier last_alert_* qui va
        permettre de sauvegarder l'heure de la dernière annonce récupérée
        """
        self.config = config
        self.logger = logger
        self.alert = alert
        self.last_offers_elements = []

        self.logger.info('new scraper for %s (last offer catching up at %s)', self.alert.url, self.alert.last_check)

    def get_last_offers(self):
        self.logger.info('getting last offers')
        page = requests.get(self.alert.url)

        if page.status_code == 404:
            self.logger.info('404 : bad url')
            return

        tree = html.fromstring(page.content)
        for offer_el in tree.xpath(OFFER_XPATH):
            offer = Offer(offer_el)
            if offer.dtt_publish > self.alert.last_check:
                self.last_offers_elements.append(offer)

        self.logger.info('%s new offers since last execution', len(self.last_offers_elements))
        return self.last_offers_elements
