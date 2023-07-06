import scrapy
import re
from articles.items import Article as ArticleItem
from app import app, db
from urllib.parse import urljoin
import datetime

class CoinpostSpider(scrapy.Spider):
    name = "coinpost"
    allowed_domains = ["coinpost.jp"]
    start_urls = [
        'https://coinpost.jp/?cat=313',
    ]


    def parse(self, response):
        articles = response.css('.homelistnew-in')
        for article in articles:
            title = article.css('.homelnew-text a::text').get().strip()
            link = article.css('.homelnew-text a::attr(href)').get()
            link = urljoin(response.url, link)
            if not self.article_exists(title):
                content_request = scrapy.Request(link, callback=self.parse_article)
                content_request.meta['title'] = title
                content_request.meta['link'] = link
                content_request.meta['source'] = "Coinpost"
                yield content_request

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.css(".post-date time::text").get()
        scraped_text = ''.join(response.css("#the-content :not(script)::text").getall())
        scraped_text = re.sub(r'\n\s*\n', '\n\n', scraped_text.strip())
        # print("<<<<<<<<<><><><><><><><><><><><><>>>>>>>>>>>")
        # print("title: "+ scraped_title)
        # print("link: "+scraped_link)
        # print("text: "+scraped_text)
        # print("date: "+scraped_pubDate)
        print("finished scraping coinpost")
        # print("<<<<<<<<<><><><><><><><><><><><><>>>>>>>>>>>")

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "source": "Coinpost"
        }

    def article_exists(self, title):
        with app.app_context():
            from app import ArticleStats
            # Check if an article with the same title already exists in the database
            existing_article = ArticleStats.query.filter((ArticleStats.title == title)).first()

            if existing_article:
                print(f"Stats article with the same link or title already exists:  - {title}")
                return True

        return False
