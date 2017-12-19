# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import codecs
import json
from collectionips import settings
from scrapy import log

class CollectionipsPipeline(object):
    def __init__(self):
        self.file = codecs.open('./ips.json','wb',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
class MySQLPipeline(object):
    def process_item(self,item,spider):
        DBKWARGS = settings.DBKWARGS
        con = pymysql.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into ips_tb(ip,port,addrs,style,speed,alive_time,proof_time)VALUES('%s','%s','%s','%s','%s','%s','%s')")
        lis = (item['ip'],item['port'],item['addrs'],item['style'],item['speed'],item['alive_time'],item['proof_time'])
        try:
            cur.execute(sql%lis)
        except Exception as e:
            print('Insert error:',e)
            log.err(e)
            con.rollback()
        else:
            con.commit()
        print('成功插入', cur.rowcount, '条数据')
        cur.close()
        con.close()
        return item

