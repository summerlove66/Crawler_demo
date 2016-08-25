# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class S1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car = scrapy.Field()
    addition = scrapy.Field()
    price = scrapy.Field()
    local = scrapy.Field()
    dirving = scrapy.Field()
    data = scrapy.Field()
    link = scrapy.Field()
    phone = scrapy.Field()
    img = scrapy.Field()
    jiaoqiangxian = scrapy.Field()
    shangyexian = scrapy.Field()
