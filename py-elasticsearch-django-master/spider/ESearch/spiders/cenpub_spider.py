# -*- coding:utf-8 -*-
import scrapy
import re
import sys
from scrapy.selector import Selector
from scrapy.http import Request
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5

reload(sys)
sys.setdefaultencoding("utf-8")


class DmozSpider(scrapy.Spider):
    name = "cenpub"
    start_urls = []

    def start_requests(self):
        for i in range(110):
            url = "http://vol.moe/list/all,all,all,sortpoint,all,all/" + str(i+1) + ".htm"
            self.start_urls.append(url)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        item = XiangmuItem()

        item["book_name"] = ''
        item["book_author"] = ''
        item["book_type"] = ''
        item["book_format"] = ''
        item["book_time"] = ''
        item["book_url"] = ''
        item["book_size"] = ''
        item["book_downl_url"] = ''
        item["book_source"] = ''
        item["book_intro"] = ''
        item["book_content"] = ''
        item["book_zip_pswd"] = ''
        item["book_chinese"] = ''
        item["book_id"] = ''

        selector = Selector(response)

        is_list_page = selector.xpath('//table[@class="book_list"]')
        if is_list_page:
            lists = selector.xpath('//td[@height="200px"]')
            for each in lists:
                href = each.xpath('a/@href').extract()
                yield Request(href[0], callback=self.parse)

        is_content_page = selector.xpath('//div[@id="nav_left"]')
        if is_content_page:
            name = selector.xpath("//b/text()").extract()
            item['book_name'] = name[0]

            inf_list = selector.xpath('//font[@id="status"]')

            author = inf_list[0].xpath('a/text()').extract()
            item['book_author'] = author

            item['book_type'] = str(inf_list[1].extract()).split('\n')[3].split('：')[-1]

            item['book_time'] = str(inf_list[-1].extract()).split('\n')[2].split('：')[-1]

            item['book_url'] = response.url
            item['book_downl_url'] = response.url

            item['book_intro'] = selector.xpath('//div[@id="desc_text"]/text()').extract()

            item['book_id'] = get_md5(response.url)

            item['book_format'] = "mobi/epub"
            yield item




