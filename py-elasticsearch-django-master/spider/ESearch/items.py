# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EsearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_type = scrapy.Field()
    book_format = scrapy.Field()
    book_time = scrapy.Field()
    book_url = scrapy.Field()
    book_size = scrapy.Field()
    book_downl_url = scrapy.Field()
    book_source = scrapy.Field()
    book_intro = scrapy.Field()
    book_content = scrapy.Field()
    book_zip_pswd = scrapy.Field()
    book_chinese = scrapy.Field()
    book_id = scrapy.Field()


class KindleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kindle_name = scrapy.Field()
    kindle_author = scrapy.Field()
    kindle_score = scrapy.Field()
    kindle_intro = scrapy.Field()
    kindle_url = scrapy.Field()
    kindle_type = scrapy.Field()
    kindle_id = scrapy.Field()


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kindle_name = scrapy.Field()
    kindle_author = scrapy.Field()
    kindle_score = scrapy.Field()
    kindle_intro = scrapy.Field()
    kindle_url = scrapy.Field()
    kindle_type = scrapy.Field()
    kindle_id = scrapy.Field()
