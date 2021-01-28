# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import EsearchItem
from ..utils.common import get_md5
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class XuexiSpider(CrawlSpider):
    name = "XueXi"
    allowed_domains = ["xuexi111.com"]
    start_urls = ['http://xuexi111.com/']
    rules = (Rule(LinkExtractor(allow=r'^http://www.xuexi111.com/(\D+?)/$'), follow=True),
             Rule(LinkExtractor(allow=r'^http://www.xuexi111.com/(\D+?)index_(\d+)\.html$'), follow=True),
             Rule(LinkExtractor(allow=r'^http://www.xuexi111.com/(\D+?)(\d+)\.html$'), callback='parse_detail'),)

    def parse_detail(self, response):
        # 缺失5个字段，book_format（标题中包含）、book_zip_pswd、book_chinese
        # book_content、book_author
        try:
            item = EsearchItem()
            item['book_url'] = response.url
            item['book_id'] = get_md5(response.url)
            item['book_name'] = response.xpath("//h1/text()").extract()[0]
            item['book_source'] = response.xpath("//div[@class='cont_ltr']/ul/li[1]//a/text()").extract()[0]
            book_size = response.xpath("//div[@class='cont_ltr']/ul/li[2]/span/text()").extract()
            if book_size!=[]:
                item['book_size'] = book_size[0]
            else:
                item['book_size'] = " "
            item['book_type'] = response.xpath("//div[@class='cont_ltr']/ul/li[4]//a/text()").extract()[0]
            item['book_time'] = response.xpath("//div[@class='cont_ltr']/ul/li[7]/span/text()").extract()[0]
            item['book_downl_url'] = response.xpath("//table[@class='download-table']/tr[1]/td[1]/a/@href").extract()[0]
            item['book_intro'] = "".join(response.xpath("//div[@class='info-content']").xpath("string(.)").extract())
            # 缺失5个字段，book_format（标题中包含）、book_zip_pswd、book_chinese
            # book_content、book_author
            item['book_zip_pswd'] = " "
            item['book_chinese'] = " "
            item['book_content'] = " "
            item['book_author'] = " "

            # 书籍的文件类型
            if response.url.find('book') != -1:
                item['book_format'] = "PDF/EPUB"
            elif response.url.find('kaoyan') != -1:
                item['book_format'] = "zip"
            elif response.url.find("shipin") != -1:
                item['book_format'] = "video"
            else:
                item['book_format'] = " "

            return item
        except Exception as e:
            print e
            return
