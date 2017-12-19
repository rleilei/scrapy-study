# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from douban_books.items import DoubanBooksItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['read.douban.com']
    def start_requests(self):
        urls = (
            'https://read.douban.com/kind/1?sort=hot&promotion_only=False&min_price=None&works_type=None&max_price=None',
        )
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        for url in urls:
            yield scrapy.Request(url = url,headers=header,callback=self.parse)

    def parse(self, response):
        book_list = response.xpath(".//*[@class='list-lined ebook-list column-list']")
        books = book_list.xpath(".//*[@class='item store-item']")
        for book in books:
            book_url = urljoin(response.url,book.xpath(".//*[@class='title']/a/@href").extract()[0])
            title = book.xpath(".//*[@class='title']/a/text()").extract()[0]
            author = book.xpath(".//*[@class='labeled-text']/a/text()").extract()[0]
            style = book.xpath(".//*[@class='labeled-text']/span/text()").extract()[0].strip()
            try:
                score = book.xpath(".//*[@class='rating-average']/text()").extract()[0]
                score_num = book.xpath(".//*[@class='ratings-link']/span/text()").extract()[0]
            except:
                score=None
                score_num=None
            price = book.xpath("string(.//*[@class='action-buttons'])").extract()[0]
            item = DoubanBooksItem(book_url=book_url,title=title,author=author,style=style,score=score,score_num=score_num,price=price)
            yield item
            next_page = urljoin(response.url,response.xpath(".//*[@class='next']/a/@href").extract()[0])
            if next_page:
                yield scrapy.Request(url = next_page,callback=self.parse)
