# -*- coding:utf-8 -*-
import scrapy
import json
import re
import urllib2
from ESearch.items import XiangmuItem
from ESearch.utils.common import get_md5


# 32406
class DmozSpider(scrapy.Spider):
    name = "zoudupai"
    start_urls = []
    main_url = "http://www.zoudupai.com"

    def start_requests(self):
        for i in range(46):
            url = "http://www.zoudupai.com/services/service.php?m=index&a=share&width=190&p=" + str(
                i + 1) + "&v=72738092.94328749"
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

        sites = json.loads(response.body)

        for each in sites['result']:

            item["book_intro"] = each['content']
            item["book_url"] = self.main_url + each['url']
            item["book_downl_url"] = self.main_url + each['url']
            item["book_time"] = each['time']
            item["book_type"] = each['album_title']
            item["book_format"] = 'mobi'

            url = self.main_url + each['url']
            data = urllib2.urlopen(url).read().decode('utf-8')
            reg = r'<span>大小：(.*?)</span>'.decode('utf-8')
            gre = re.compile(reg, re.S)
            size = re.findall(gre, data)
            item["book_size"] = size
            item["book_id"] = get_md5(url)

            reg = r'《(.*?)》'.decode('utf-8')
            gre = re.compile(reg, re.S)
            name = re.findall(gre, data)
            if name:
                item['book_name'] = name[0]
            else:
                item['book_name'] = ''

            return item
