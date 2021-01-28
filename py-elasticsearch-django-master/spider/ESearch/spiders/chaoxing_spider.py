# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import Selector
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5


class DmozSpider(scrapy.Spider):
    name = "chaoxing"
    start_urls = []
    main_url = "http://book.chaoxing.com"

    def start_requests(self):
        file_object = open(r'chaoxing_url.csv', 'r')
        try:
            for line in file_object:
                x = line.strip()
                self.start_urls.append(x)
                start = x.split('_')[0] + "_" + x.split('_')[1]
                for i in range(200):
                    self.start_urls.append(start + "__page_" + str(i+2) + ".html?vip=false")
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
        is_lists_page = selector.xpath('//ul[@class="list"]')
        if is_lists_page:
            info_lists = is_lists_page.xpath('li/div[@class="pic_upost"]/a/@href').extract()
            for each in info_lists:
                yield Request(self.main_url + each, callback=self.parse)

            # next_link = selector.xpath('//a[@v="next"]/@href').extract()
            # yield Request(self.main_url + next_link[0], callback=self.parse)

        is_info_page = selector.xpath('//div[@class="box_title"]')
        if is_info_page:

            item["book_name"] = selector.xpath('//div[@class="box_title"]/h1/text()').extract()
            info = selector.xpath('//ul[@class="text01"]')
            item["book_type"] = info.xpath('li')[-1].xpath('a/text()').extract()
            author = info.xpath('li/text()').extract()[0]
            item["book_author"] = ''.join(author).split('>')[-1]
            source = info.xpath('li/text()').extract()[2]
            item["book_source"] = ''.join(source).split('>')[-1]
            size = info.xpath('li/text()').extract()[3]
            item["book_size"] = ''.join(size).split('>')[-1] + '页'

            intro = selector.xpath('//div[@class="abut_top_part"]/text()').extract()
            if intro:
                item['book_intro'] = intro

            item["book_url"] = response.url
            item["book_downl_url"] = response.url
            item["book_id"] = get_md5(response.url)
            yield item



