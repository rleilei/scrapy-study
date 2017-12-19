# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CollectionipsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    addrs = scrapy.Field()
    style = scrapy.Field()
    speed = scrapy.Field()
    alive_time = scrapy.Field()
    proof_time = scrapy.Field()

