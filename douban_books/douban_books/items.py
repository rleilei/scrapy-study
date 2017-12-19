# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    style = scrapy.Field()
    #word_num = scrapy.Field()
    score = scrapy.Field()
    score_num = scrapy.Field()
    price = scrapy.Field()
    book_url = scrapy.Field()


