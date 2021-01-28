# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from  scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import KindleItem
from ..utils.common import get_md5
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class KindlepushSpider(CrawlSpider):
    name = "Kindlepush"
    allowed_domains = ["kindlepush.com"]
    start_urls = ['http://kindlepush.com/']
    rules = (Rule(LinkExtractor(allow=r"/category/"), follow=True),
             Rule(LinkExtractor(allow=r"/book/\d+"), callback="parse_detail"),)

    def parse_detail(self, response):
        try:
            item = KindleItem()
            item['kindle_name'] = response.xpath("//div[@class='desc']/h3").xpath("string(.)").extract()[0].strip()
            item['kindle_author'] = response.xpath("//div[@class='desc']//div[@class='data']/h3/text()").extract()[0]
            item['kindle_score'] = response.xpath("//div[@class='desc']//div[@class='data']/h5[1]/text()").extract()[0].strip()
            item['kindle_url'] = response.url
            item['kindle_id'] = get_md5(response.url)
            item['kindle_type'] = response.xpath("//a[@id='to_category']/text()").extract()[0]
            item['kindle_intro'] = response.xpath("//article[@class='intro']/p/text()").extract()[0]
            return item
        except Exception as e:
            print e
            return
