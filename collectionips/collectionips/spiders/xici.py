# -*- coding: utf-8 -*-
import scrapy
from collectionips.items import CollectionipsItem
from urllib.parse import urljoin

class XiciSpider(scrapy.Spider):
    name = 'xici'
    def start_requests(self):
        start_urls = [
            'http://www.xicidaili.com/nn',
        ]
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse,headers=header)
    def parse(self, response):
        ip_list = response.xpath("//*[@id='ip_list']")
        trs = ip_list.xpath('.//tr')
        for tr in trs:
            if tr.xpath('.//td[2]/text()').extract():#去掉表格中的标题栏
                ip = tr.xpath('.//td[2]/text()').extract()[0]
                port = tr.xpath('.//td[3]/text()').extract()[0]
                addrs = tr.xpath('string(.//td[4])').extract()[0].strip()
                style = tr.xpath('.//td[6]/text()').extract()[0]
                speed= tr.xpath(".//*[@class='bar']/@title").extract()[0]
                alive_time = tr.xpath('.//td[9]/text()').extract()[0]
                proof_time = tr.xpath('.//td[10]/text()').extract()[0]
                item = CollectionipsItem(ip=ip,port=port,addrs=addrs,style=style,speed=speed,alive_time=alive_time,proof_time=proof_time)
                yield item
            next_page = urljoin(response.url, response.xpath(".//*[@class='next_page']/@href").extract()[0])
            if next_page:
                yield scrapy.Request(url=next_page,callback=self.parse)



