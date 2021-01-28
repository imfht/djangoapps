# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import Selector
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5


class DmozSpider(scrapy.Spider):
    name = "qidian"
    start_urls = []
    main_url = "http:"

    def start_requests(self):
        for x in range(1, 30866):
            string = "http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=&update=-1&page=" + str(x) + "&month=-1&style=1&action=-1&vip=-1"
            self.start_urls.append(string)
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
        is_lists_page = selector.xpath('//ul[@class="all-img-list cf"]')
        if is_lists_page:
            info_lists = is_lists_page.xpath('li/div[@class="book-mid-info"]/h4/a/@href').extract()
            for each in info_lists:
                yield Request(self.main_url + each, callback=self.parse)

        is_info_page = selector.xpath('//div[@class="book-info "]')
        if is_info_page:
            item["book_name"] = is_info_page.xpath('h1/em/text()').extract()
            item["book_author"] = is_info_page.xpath('h1/span/a/text()').extract()
            type = is_info_page.xpath('p[@class="tag"]/a/text()').extract()
            item["book_type"] = ",".join(type)
            item["book_intro"] = is_info_page.xpath('p[@class="intro"]/text()').extract()
            item["book_size"] = is_info_page.xpath("p")[-2].xpath('em/text()')[0].extract() +'万字'
            item["book_content"] = ''.join(selector.xpath('//div[@class="book-intro"]/p/text()').extract()).replace(" ", "").replace("\n", '').replace("\r", "")
            item["book_url"] = response.url
            item["book_downl_url"] = response.url
            item["book_id"] = get_md5(response.url)
            yield item



