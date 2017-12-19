# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from yunqiCrawl.items import YunqiBookListItem,yunqiBookDetailItem
from scrapy.conf import settings
import codecs
import json
from scrapy.exceptions import DropItem

class YunqicrawlPipeline(object):
    def __init__(self,mongo_uri,mongo_db,replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE','yunqi'),
            replicaset=crawler.settings.get('REPLICASET')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]
    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        if isinstance(item,YunqiBookListItem):
            self._process_booklist_item(item)
        else:
            self._process_bookDetail_item(item)
    def _process_booklist_item(self,item):
        self.db.bookInfo.insert(dict(item))
    def _process_bookDetail_item(self,item):
        self.db.bookDetail.insert(dict(item))
class JsonPipeline(object):
    def __init__(self):
        self.file1 = codecs.open('./bookinfo.json','wb',encoding='utf-8')
        self.file2 = codecs.open('./bookDetail.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        if isinstance(item,YunqiBookListItem):
            if item['novelId']:
                line = json.dumps(dict(item)) + "\n"
                self.file1.write(line)
                return item
            else:
                raise DropItem('miss novelId in %s'%item)
        else:
            if item['novelId']:
                line = json.dumps(dict(item)) + "\n"
                self.file2.write(line)
                return item
            else:
                raise DropItem('miss novelId in %s'%item)
