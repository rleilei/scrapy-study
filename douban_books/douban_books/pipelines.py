# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.exceptions import DropItem
import csv

class DoubanBooksPipeline(object):
    #将数据保存在json格式中
    def __init__(self):
        self.file = codecs.open('../books_1000_2.json','wb',encoding = 'utf-8')
    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item),ensure_ascii=False) + '\n'
            self.file.write(line)
            return item
        else:
            raise DropItem('mising title is %s'%item)

    #将数据保存在csv中
    # def __init__(self):
    #     self.file = codecs.open('../books_1000.csv', 'w', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     if item['title']:
    #         headers = ['书名','作者','类型','价格','评分','评价人数','本书链接']
    #         rows = [(item['title'],item['author'],item['style'],item['price'],item['score'],item['score_num'],item['book_url']),]
    #         f_csv = csv.writer(self.file)
    #         f_csv.writerow(headers)
    #         f_csv.writerows(rows)
    #         return item
    #     else:
    #         raise DropItem('mising title is %s' % item)


