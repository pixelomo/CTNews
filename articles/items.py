# -*- coding: utf-8 -*-
import scrapy

class Article(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    pubDate = scrapy.Field()
    html = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
