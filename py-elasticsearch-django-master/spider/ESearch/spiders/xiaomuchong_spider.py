# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import Selector
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5


class DmozSpider(scrapy.Spider):
    name = "xiaomuchong"
    start_urls = []
    main_url = "http://muchong.com"

    def start_requests(self):
        file_object = open(r'xiaomuchong_url.csv', 'r')
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
        print response.url
        is_lists_page = selector.xpath('//div[@class="article-list pt10"]')
        if is_lists_page:
            info_lists = is_lists_page.xpath('//h3[@class="article-title_list"]/a/@href').extract()
            for each in info_lists:
                yield Request(self.main_url + each, callback=self.parse)

            page_lists = is_lists_page.xpath('div[@class="page ui-pagination"]/ul/li').extract()
            length = len(page_lists)-1
            for each_page in page_lists:
                if "curPage" in each_page:
                    cur_page = page_lists.index(each_page)
            next_links = is_lists_page.xpath('div[@class="page ui-pagination"]/ul/li/a/@href').extract()
            try:
                yield Request(self.main_url + next_links[cur_page+1])
            finally:
                pass

        is_info_page = selector.xpath('//div[@class="article"]')
        if is_info_page:
            item["book_type"] = selector.xpath('//div[@class="crumb"]/a/text()').extract()[-1]
            item["book_name"] = is_info_page.xpath('h1/text()').extract()
            item["book_source"] = is_info_page.xpath('div[@class="article-info clearfix"]/span[@class="fl"]/text()').extract()
            item["book_author"] = is_info_page.xpath('div[@class="article-info clearfix"]/span[@class="ml15"]/a/text()').extract()
            item["book_content"] = is_info_page.xpath('div[@id="article-main"]/p/text()').extract()
            item["book_url"] = response.url
            item["book_downl_url"] = response.url
            item["book_id"] = get_md5(response.url)
            yield item



