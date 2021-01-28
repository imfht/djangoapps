# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import EsearchItem
from ..utils.common import get_md5
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class EsearchSpider(CrawlSpider):
    name = "ESearch"
    allowed_domains = ["eshuba.com"]
    start_urls = ['http://eshuba.com/']
    rules = (Rule(LinkExtractor(allow=r"sort/(.+?)\.htm"), follow=True),
             Rule(LinkExtractor(allow=r"soft/(\d+)\.htm"), callback='parse_detail'),)

    def parse_detail(self, response):
        try:
            item = EsearchItem()
            item['book_id'] = get_md5(response.url)
            item['book_url'] = response.url
            item['book_name'] = response.xpath("//font[@size='2']/strong/text()").extract()[0]
            item['book_size'] = response.xpath(
                    "/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[3]//td[@width='50%']/text()").extract()[0]
            item['book_type'] = response.xpath("/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[5]//td/text()").extract()[0]
            item['book_time'] = response.xpath("/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[6]//td/text()").extract()[0]
            book_format=response.xpath("/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[7]//td/text()").extract()
            if book_format!=[]:
                item['book_format'] = book_format[0]
            else:
                item['book_format'] =" "
            item['book_author'] = response.xpath("/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[8]//td/b/text()").extract()[0]
            item['book_source'] = response.xpath("/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[10]//td/text()").extract()[0]
            item['book_intro'] = "".join(response.xpath(
                "/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[11]/td/table/tbody/tr[2]//p/text()").extract())
            book_downl_url=response.xpath(
                "/html/body/center[2]/table[2]/tr[1]/td[4]/table/tr[11]/td/table/tbody/tr[7]/td/a[2]/@href").extract()
            if book_downl_url!=[]:
                item['book_downl_url'] = book_downl_url[0]
            else:
                item['book_downl_url'] =" "
            # 缺失3个字段，book_content、book_zip_pswd、book_chinese
            item['book_content'] = " "
            item['book_zip_pswd'] = " "
            item['book_chinese'] = " "
            return item
        except Exception as e:
            print e
            return
