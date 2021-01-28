# -*- coding: utf-8 -*-
__author__ = 'jiechao'

from elasticsearch_dsl import DocType, Date, analyzer,Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class CommonbookType(DocType):

    suggest = Completion(analyzer=ik_analyzer)
    book_name = Text(analyzer="ik_max_word")
    book_author = Text(analyzer="ik_max_word")
    book_content = Text(analyzer="ik_max_word")
    book_type = Keyword()
    book_format = Keyword()
    book_time = Date()
    book_url = Keyword()
    book_downl_url = Keyword()
    book_source = Keyword()
    book_intro = Text(analyzer="ik_max_word")
    book_zip_pwd = Keyword()
    book_id = Keyword()
    book_chinese = Keyword()
    book_size = Integer()
    kindle_name = Text(analyzer="ik_max_word")
    kindle_author = Text(analyzer="ik_max_word")
    kindle_score = Keyword()
    kindle_intro = Text(analyzer="ik_max_word")
    kindle_url = Keyword()
    kindle_type = Keyword()
    kindle_id = Keyword()


    class Meta:
        index = "comeearch"
        # index建立索引的时候不能用大写
        doc_type = "article"


if __name__ == "__main__":
    CommonbookType.init()

