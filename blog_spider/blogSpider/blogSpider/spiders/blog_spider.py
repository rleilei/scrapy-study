import scrapy
#from scrapy.contrib.spiders import CrawlSpider
from blogSpider.items import BlogspiderItem
from scrapy import Selector

class BlogSpider(scrapy.Spider):
    name = 'blog_spider'
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]
    def parse(self, response):
        papers = response.xpath(".//*[@class='day']")
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle2']/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle2']/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='c_b_p_desc']/text()").extract()[0]
            item = BlogspiderItem(url = url,title=title,time=time,content=content)
            #request = scrapy.Request(url=url,meta={'item':item},callback=self.parse_body)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item
            yield request
            next_page = Selector(response).re(r'<a href="(\S+?)">下一页</a>')
            if next_page:
                yield scrapy.Request(url =next_page[0],callback=self.parse)

    def parse_body(self,response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['image_urls'] = body.xpath(".//img//@src").extract()
        yield item