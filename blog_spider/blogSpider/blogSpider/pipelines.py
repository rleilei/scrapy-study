# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
import codecs

class BlogspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open(r'E:\scrapy_study\blog_spider\papers.json','wb',encoding='gbk')
    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            return item
        else:
            raise DropItem('Missing title in %s'%item)
