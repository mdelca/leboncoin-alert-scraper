# coding: utf-8
from datetime import datetime


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
        p_el = info_el.xpath('aside/p')[0]
        str_date = p_el.attrib['content']
        str_time = p_el.xpath('text()')[0].strip().split(',')[1].strip()

        self.dtt_publish = datetime.strptime('%s %s' % (str_date, str_time), '%Y-%m-%d %H:%M')
        self.link = self.lxml_element.xpath('a')[0].attrib['href']
        self.title = self.lxml_element.xpath('a')[0].attrib['title']
        price_elements = info_el.xpath('h3[@class="item_price"]')
        if len(price_elements):
            self.price = price_elements[0].attrib['content']

        image_elements = self.lxml_element.xpath('a/div[@class="item_image"]/span[@class="item_imagePic"]/span')
        if image_elements:
            self.image = image_elements[0].attrib['data-imgsrc']

        locations_elements = info_el.xpath('p[@itemtype="http://schema.org/Place"]/meta')

        self.location = '/'.join([location.attrib['content'] for location in locations_elements])
