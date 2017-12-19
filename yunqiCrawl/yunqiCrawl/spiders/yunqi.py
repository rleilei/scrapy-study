# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yunqiCrawl.items import YunqiBookListItem,yunqiBookDetailItem
import re


class YunqiSpider(CrawlSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        book_list = response.xpath(".//*[@class = 'book']")
        for book in book_list:
            novelId = book.xpath(".//*[@class='book_info']/h3/a/@id").extract_first()
            novelName = book.xpath(".//*[@class='book_info']/h3/a/text()").extract_first()
            novelLink = book.xpath(".//*[@class='book_info']/h3/a/@href").extract_first()
            novelAuthor = book.xpath(".//*[@class='book_info']/dl[1]/dd[1]/a/text()").extract_first()
            novelType = book.xpath(".//*[@class='book_info']/dl[1]/dd[2]/a/text()").extract_first()
            novelStatus = book.xpath(".//*[@class='book_info']/dl[1]/dd[3]/text()").extract_first()
            novelUpdateTime = book.xpath(".//*[@class='book_info']/dl[2]/dd[1]/text()").extract_first()
            novelWords = book.xpath(".//*[@class='book_info']/dl[2]/dd[2]/text()").extract_first()
            novelImgUrl = book.xpath("./a/img/@src").extract_first()
            bookListItem = YunqiBookListItem(novelId=novelId,novelName=novelName,novelLink=novelLink,novelAuthor=novelAuthor,novelType=novelType,novelStatus=novelStatus,novelUpdateTime=novelUpdateTime,novelWords=novelWords,novelImgUrl=novelImgUrl)
            yield bookListItem
            request = scrapy.Request(url=novelLink,callback=self.parse_book_detail)
            request.meta['novelId'] = novelId
            yield request

    def parse_book_detail(self,response):
        novelId = response.meta['novelId']
        try:
            novelLabel = re.search('\s+.{5}\s+(\S+)',response.xpath(".//*[@class='tags']/text()").extract_first()).group(1)
        except:
            novelLabel = None
        try:
            novelAllClick = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()).group(1)
        except:
            novelAllClick = None
        try:
            novelAllPopular = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()).group(1)
        except:
            novelAllPopular = None
        try:
            novelAllComm = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()).group(1)
        except:
            novelAllComm = None
        try:
            novelMonthClick = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()).group(1)
        except:
            novelMonthClick=None
        try:
            novelMonthPopular = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()).group(1)
        except:
            novelMonthPopular=None
        try:
            novelMonthComm = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()).group(1)
        except:
            novelMonthComm=None
        try:
            novelWeekClick = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()).group(1)
        except:
            novelWeekClick = None
        try:
            novelWeekPopular = re.search('\D+(\d+)',response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()).group(1)
        except:
            novelWeekPopular=None
        try:
            novelWeekComm = re.search('\D+(\d+)', response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()).group(1)
        except:
            novelWeekComm=None
        try:
            novelCommentNum = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()
        except:
            novelCommentNum=None
        bookDetailItem = yunqiBookDetailItem(novelId=novelId,novelLabel=novelLabel,novelAllClick=novelAllClick,novelAllPopular=novelAllPopular,novelAllComm=novelAllComm,
                                             novelMonthClick=novelMonthClick,novelMonthPopular=novelMonthPopular,novelMonthComm=novelMonthComm,novelWeekClick=novelWeekClick,
                                             novelWeekPopular=novelWeekPopular,novelWeekComm=novelWeekComm,novelCommentNum=novelCommentNum)
        yield  bookDetailItem


