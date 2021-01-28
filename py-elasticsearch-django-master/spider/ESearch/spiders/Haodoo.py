# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import EsearchItem
from ..utils.common import get_md5
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class HaodooSpider(CrawlSpider):
    name = "Haodoo"
    allowed_domains = ["haodoo.net"]
    start_urls = ['http://haodoo.net/']
    rules = (Rule(LinkExtractor(allow=r"M=hd&(P=\w+|P=100)"), follow=True),
             Rule(LinkExtractor(allow=r"M=(book|Share)&P=([\d][\d\w]*|[\w]\w*\d+)", deny=r"M=hd&P=100|p=audio"),
                  callback="paser_book"),)

    def paser_book(self, response):

        if response.xpath("//pre[@id='SourceText']"):
            return
        try:
            item = EsearchItem()
            item['book_url'] = response.url
            item['book_id'] = get_md5(response.url)
            book_author = response.xpath("//font[@color='CC0000']")[1].xpath("./text()").extract()
            if book_author!=[]:
                item['book_author'] = book_author[0]
            else:
                item['book_author'] = " "
            book_name = response.xpath("//font[@color='CC0000']")[1].xpath("./parent::td/text()[2]").extract()
            if book_name!=[]:
                item['book_name'] = response.xpath("//font[@color='CC0000']")[1].xpath("./parent::td/text()[2]").extract()[0]
            else:
                item['book_name'] =" "
            item['book_source'] = "好读网"
            item['book_type'] = "prc/epub/mobi"
            time_size = response.xpath("//font[@color='CC0000']")[1].xpath(
                "./parent::td/input[3]/following::font[1]/text()").extract()[0].strip()
            if time_size!=[]:
                item['book_time'] = re.search(r"\).*", time_size).group()[1:]
                item['book_size'] = re.search(r"\(.*?\)", time_size).group()[1:-1]
            else:
                item['book_time'] = " "
                item['book_size'] = " "
            item['book_intro'] = "".join(
                response.xpath("//font[@color='CC0000']")[1].xpath("./parent::td/text()").extract())

            # 缺失5个字段，book_content、book_downl_url、
            # book_zip_pswd、book_chinese、book_type
            item['book_content'] = " "
            item['book_downl_url'] = " "
            item['book_zip_pswd'] = " "
            item['book_chinese'] = " "
            item['book_type'] = " "
            return item
        except Exception as e:
            print e
            return
