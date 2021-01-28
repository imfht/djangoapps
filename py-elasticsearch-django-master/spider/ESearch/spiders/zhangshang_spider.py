# -*- coding:utf-8 -*-
import scrapy
import sys
from scrapy.selector import Selector
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5

# reload(sys)
# sys.setdefaultencoding("utf-8")


class DmozSpider(scrapy.Spider):
    name = "zhangshang"
    start_urls = []
    main_url = 'https://www.cnepub.com'

    def start_requests(self):
        for x in range(2, 500000):
                self.start_urls.append(self.main_url + '/' + str(x))
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

        item['book_url'] = response.url
        item['book_downl_url'] = response.url
        item['book_id'] = get_md5(response.url)

        name = ''.join(selector.xpath('//h5/text()')[0].extract())
        item['book_name'] = name.replace(' ', '').replace('\n', '').replace('\t', '')

        item['book_intro'] = selector.xpath('//div[@id="book_intro_content"]/text()').extract()

        info_list = selector.xpath('//div[@class="col-xs-12 col-sm-4 col-md-4"]/div')

        item['book_author'] = info_list[0].xpath('a/text()')[0].extract()

        item['book_type'] = info_list[1].xpath('a/text()').extract()

        yield item







