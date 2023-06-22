# -*- coding: utf-8 -*-
import scrapy

class Article(scrapy.Item):
    title = scrapy.Field()
    pubDate = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    title_chinese = scrapy.Field()
    text_chinese = scrapy.Field()
    title_indonesian = scrapy.Field()
    text_indonesian = scrapy.Field()
    title_korean = scrapy.Field()
    text_korean = scrapy.Field()
    html = scrapy.Field()
    title_translated = scrapy.Field()
    content_translated = scrapy.Field()
    source = scrapy.Field()

