# -*- coding:utf-8 -*-
import scrapy
import re
import urllib2
from scrapy.http import Request
from scrapy import Selector
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5


# 32406
class DmozSpider(scrapy.Spider):
    name = "haoyang"
    start_urls = []
    main_url = "http://www.9lizhi.com"

    def start_requests(self):
        file_object = open(r'haoyang_url.csv', 'r')
        try:
            for line in file_object:
                x = line.strip()
                self.start_urls.append(x)
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()

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

        is_lists_page = selector.xpath('//ul[@id="resultsContainer"]')
        if is_lists_page:
            info_lists = is_lists_page.xpath('li/div[@class="item_title"]/strong/h2/a/@href').extract()
            for each in info_lists:
                yield Request(each, callback=self.parse)

            page_lists = is_lists_page.xpath('//select[@name="select"]/option/@value').extract()
            for each_page in page_lists[1:-1]:
                yield Request(self.main_url + each_page, callback=self.parse)
            pass

        is_info_page = selector.xpath('//div[@id="detail"]')
        if is_info_page:
            item['book_url'] = response.url
            item['book_id'] = get_md5(response.url)
            item['book_downl_url'] = response.url

            type = selector.xpath('//div[@class="posi"]/a/text()').extract()
            type_url = selector.xpath('//div[@class="posi"]/a/@href').extract()
            if "http://www" in type_url[-1]:
                item['book_type'] = type[-2]
            else:
                item['book_type'] = type[-1]

            information = is_info_page.xpath('div[@class="tb-detail-hd"]')
            item['book_name'] = information.xpath('h1/text()').extract()
            time = information.xpath('li[@class="dated"]/span[@class="datetime"]/text()').extract()
            time = ''.join(time).split('：')[-1]
            item['book_time'] = time
            author = information.xpath('li[@class="dated"]/span[@class="author"]/text()').extract()
            item['book_author'] = ''.join(author).replace('\r', '').replace('\n', '')
            yield item


