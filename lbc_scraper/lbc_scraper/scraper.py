# coding: utf-8
import requests

from lxml import html

from lbc_scraper.offer import Offer

OFFER_XPATH = '//li[@itemtype="http://schema.org/Offer"]'


class LBCScraper(object):
    alert = None

    def __init__(self, config, logger, session, alert):
        """
        Initialize scrapper. Creating last_alert_* file
        Initialisation du "scrapper", création du fichier last_alert_* qui va
        permettre de sauvegarder l'heure de la dernière annonce récupérée
        """
        self.config = config
        self.logger = logger
        self.session = session
        self.alert = alert

        self.logger.info('new scraper for %s (last offer catching up at %s)', self.alert.url, self.alert.last_check)

    def get_last_offers(self):
        self.logger.info('getting last offers')
        page = requests.get(self.alert.url)

        last_offers_elements = []

        if page.status_code == 404:
            self.logger.info('404 : bad url')
            return

        tree = html.fromstring(page.content)
        offers_to_inspect = tree.xpath(OFFER_XPATH)

        if not offers_to_inspect:
            self.logger.info('no new offers since last execution')
            return

        # we keep first offer to determine last_check datetime
        first_offer = Offer(offers_to_inspect.pop(0))

        if first_offer.dtt_publish > self.alert.last_check:
            last_offers_elements.append(first_offer)
            new_last_check_dtt = first_offer.dtt_publish
        else:
            self.logger.info('no new offers since last execution')
            return

        for offer_el in offers_to_inspect:
            offer = Offer(offer_el)
            if offer.dtt_publish > self.alert.last_check:
                last_offers_elements.append(offer)

        self.alert.last_check = new_last_check_dtt
        self.session.add(self.alert)
        self.session.commit()

        self.logger.info('%s new offers since last execution', len(last_offers_elements))
        return last_offers_elements

