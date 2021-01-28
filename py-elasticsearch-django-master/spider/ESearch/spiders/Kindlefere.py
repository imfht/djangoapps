# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from  scrapy.linkextractors import LinkExtractor
import scrapy
from ..items import KindleItem
from ..utils.common import get_md5
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class KindlefereSpider(CrawlSpider):
    name = "Kindlefere"
    allowed_domains = ["kindlefere.com", "douban.com"]
    start_urls = ['http://kindlefere.com/']
    rules = (Rule(LinkExtractor(allow=r"kindlefere.com/post(/page/\d*)?$"), ),
             Rule(LinkExtractor(allow=r"kindlefere.com/books(/page/\d*)?$"), ),
             Rule(LinkExtractor(allow=r"kindlefere.com/books/weekly"), ),
             Rule(LinkExtractor(allow=r"^https://kindlefere.com/post/\d+\.html"), callback="parse_kindle"),)

    def filters(self, index):
        return re.match(r"https://book.douban.com/subject/\d+/", index)

    def parse_kindle(self, response):
        s = {"https://kindlefere.com/books",
             "https://kindlefere.com/books/weekly"}
        # 过滤一些非推荐书籍网页
        if response.xpath("//nav[@class='current_nav']/a[2]/@href").extract()[0] not in s:
            return
        list_url = response.xpath("//div[@class='entry-content']//a/@href").extract()
        # 找到书籍对应的豆瓣网的地址，其他地址过滤掉
        for url in filter(self.filters, list_url):
            item = KindleItem()
            item['kindle_url'] = response.url
            return scrapy.Request(url=url, callback=self.parse_douban, meta={"item": item})

    def parse_douban(self, response):
        try:
            item = response.meta['item']
            item['kindle_name'] = response.xpath("//h1/span/text()").extract()[0]
            item['kindle_author'] = response.xpath("//div[@id='info']/a[1]/text()").extract()[0]
            item['kindle_score'] = response.xpath("//strong[@class='ll rating_num ']/text()").extract()[0]
            item['kindle_id'] = get_md5(response.url)
            item['kindle_type'] = " "
            item['kindle_intro'] = "".join(response.xpath("//div[@class='intro']//p").xpath("string(.)").extract())
            return item
        except Exception as e:
            print e
            return
