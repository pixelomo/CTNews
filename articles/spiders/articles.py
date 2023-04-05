# -*- coding: utf-8 -*-
import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["cointelegraph.com"]
    start_urls = [
        'https://cointelegraph.com/rss',
    ]

    def parse(self, response):
        for article in response.xpath("//channel/item")
            article_url = article.xpath('link//text()').extract_first()
            # yield {
            #     'title' : article.xpath('title//text()').extract_first(),
            #     'link': article.xpath('link//text()').extract_first(),
            #     # scrapy.Request(response.urljoin(article.xpath('link//text()').extract_first()), callback=self.parse_article_page)
            #     # 'pubDate' : post.xpath('pubDate//text()').extract_first(),
            # }
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article_page)
        # next_page = response.css("li.next > a ::attr(href)").extract_first()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article_page(self, response):
        item = {}
        article = response.css(".post__article")
        item["title"] = article.css("h1.post__title").extract_first()
        item['lead'] = article.css(".post__block_lead-text").extract_first()
        item['content'] = article.css(".post-content").extract_first()
