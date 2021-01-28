# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DoubanItem
from ..utils.common import get_md5
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class DoubanSpider(CrawlSpider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ['https://book.douban.com/tag/']
    rules = (Rule(LinkExtractor(allow=r"/tag/"),follow=True),
             Rule(LinkExtractor(allow=r"https://book.douban.com/subject/\d+/$"),callback="douban_parse"))

    def douban_parse(self, response):
        try:
            item = DoubanItem()
            item['kindle_url']=response.url
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
