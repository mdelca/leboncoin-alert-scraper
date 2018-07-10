# coding: utf-8
import os

from datetime import datetime, timedelta
from urllib.parse import urlsplit



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

        self.info_el = self.lxml_element.xpath('a/section')[0]

        #self.p_el = info_el.xpath('aside/p')

        lbc_dtt =  self.info_el.xpath('div[@class="lFSBn"]/div[@class="_3YWZQ"]/div')[0].attrib['content']
        str_dt, str_time = lbc_dtt.split(',')

        now = datetime.now()

        year = now.year

        if str_date == "Aujourd'hui":
            month = now.month
            day = now.day
        elif str_date == 'Hier':
            yesterday = now - timedelta(1)
            month = yesterday.month
            day = yesterday.day
        else:
            dtt = datetime.strptime('%B')    # locale ?
            month = None
            day = None

        hour = None
        minute = None

        #dtt =
#9        str_date = p_el.attrib['content']
#9        str_time = p_el.xpath('text()')[-1].strip().split(',')[-1].strip()
#9
#9        #self.dtt_publish = datetime.strptime('%s %s' % (str_date, str_time), '%Y-%m-%d %H:%M')
        self.dtt_publish = datetime(now.year)
        href_value = self.lxml_element.xpath('a')[0].attrib['href']
        self.link = 'http://leboncoin.fr%s' % href_value
        self.title = self.info_el.xpath('p/span/text()')[0]
#9        price_elements = info_el.xpath('h3[@class="item_price"]')
#9        #if len(price_elements):
#9            #self.price = price_elements[0].xpath('text()')[0]
#9
#9        image_elements = self.lxml_element.xpath('a/div[@class="item_image"]/span[@class="item_imagePic"]/span')
#9        #if image_elements:
#9            #self.image = image_elements[0].attrib['data-imgsrc']
#9
#9        locations_elements = info_el.xpath('p[@itemtype="http://schema.org/Place"]/meta')
#9
#9        #self.location = '/'.join([location.attrib['content'] for location in locations_elements])
