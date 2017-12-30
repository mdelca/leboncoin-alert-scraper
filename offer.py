# coding: utf-8
from datetime import datetime


class Offer(object):

    lxml_element = None
    dtt_publish = None

    def __init__(self, lxml_element):
        self.lxml_element = lxml_element

        p_el = self.lxml_element.xpath('a/section/aside/p')[0]
        str_date = p_el.attrib['content']
        str_time = p_el.xpath('text()')[0].strip().split(',')[1].strip()

        self.dtt_publish = datetime.strptime('%s %s' % (str_date, str_time), '%Y-%m-%d %H:%M')
