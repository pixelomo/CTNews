# -*- coding: utf-8 -*-
import scrapy
from CTNews.items import Article

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["cointelegraph.com"]
    start_urls = [
        'https://cointelegraph.com/rss',
    ]

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            if link:
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    "title": item.xpath("title/text()").get(),
                    "pubDate": item.xpath("pubDate/text()").get(),
                })

    def parse_article(self, response):
        article = Article()
        article["title"] = response.meta["title"]
        article["link"] = response.url
        article["pubDate"] = response.meta["pubDate"]
        article["content"] = "".join(response.css(".post-full-text *::text").getall())