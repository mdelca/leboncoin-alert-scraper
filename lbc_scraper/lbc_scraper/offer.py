# coding: utf-8
import requests

from datetime import datetime, timedelta
from urllib.parse import urlsplit
from lxml import html

MONTH_MAP = {
    'janvier': 1,
    'février': 2,
    'mars': 3,
    'avril': 4,
    'mai': 5,
    'juin': 6,
    'juillet': 7,
    'août': 8,
    'septembre': 9,
    'octobre': 10,
    'novembre': 11,
    'décembre': 12
}


class Offer(object):

    lxml_element = None
    dtt_publish = None
    link = None
    title = None
    price = None
    location = None
    image = None

    def __init__(self, lxml_element):
        self.lxml_element = lxml_element

        info_el = self.lxml_element.xpath('a/section')[0]

        # Récupération de la date de publication de l'annonce (probablement la date à laquelle
        # l'utilisateur à posté son annonce et non la date à laquelle lbc à publié l'annonce
        lbc_dtt =  info_el.xpath('div[@class="lFSBn"]/div[@class="_3YWZQ"]/div')[0].attrib['content']
        str_dt, str_time = lbc_dtt.split(',')

        now = datetime.now()
        year = now.year

        if str_dt == "Aujourd'hui":
            month = now.month
            day = now.day
        elif str_dt == 'Hier':
            yesterday = now - timedelta(1)
            month = yesterday.month
            day = yesterday.day
        else:
            day_, month_ = str_dt.split(' ')
            day = int(day_)
            month = MONTH_MAP.get(month_)

        hour_, minutes_ = str_time.split(':')
        hour = int(hour_)
        minutes = int(minutes_)

        self.dtt_publish = datetime(year, month, day, hour, minutes)

        # Récupération du lien de l'annonce
        href_value = self.lxml_element.xpath('a')[0].attrib['href']
        self.link = 'http://leboncoin.fr%s' % href_value

        # Récupération du titre de l'annonce
        self.title = info_el.xpath('p/span/text()')[0]

        # Récupération du prix de l'annonce (possible de n'avoir aucun prix)
        price_elements = info_el.xpath('div/div/span/span')
        if len(price_elements):
            self.price = price_elements[0].text

        # Récupération de l'image principale : pas réussi à récupérer l'image dans la liste des offres,
        # On passe par la page de l'offre
        offer_page_tree = html.fromstring(requests.get(self.link).content)
        self.image = offer_page_tree.xpath('//img[@alt="image-galerie-0"]')[0].attrib['src']

        # Récupération du lieu
        self.location = info_el.xpath('div[@class="_32V5I"]/p[@itemprop="availableAtOrFrom"]')[0].text
