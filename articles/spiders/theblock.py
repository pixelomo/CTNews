import scrapy
import re
from articles.items import Article as ArticleItem
from app import app, db
from urllib.parse import urljoin

class TheBlockSpider(scrapy.Spider):
    name = "theblock"
    allowed_domains = ["theblock.co"]
    start_urls = [
        'https://www.theblock.co/latest',
    ]

    def parse(self, response):
        articles = response.css('article.articleCard')
        for article in articles:
            title = article.css('.headline a h2 span::text').get().strip()
            link = article.css('.headline a::attr(href)').get()
            # Join the base URL with the extracted link
            link = urljoin(response.url, link)
            pubDate = article.css('.pubDate::text').get()
            if not self.article_exists(title, link):
                content_request = scrapy.Request(link, callback=self.parse_article)
                content_request.meta['title'] = title
                content_request.meta['pubDate'] = pubDate
                content_request.meta['link'] = link
                content_request.meta['source'] = "TheBlock"
                yield content_request

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css("div#articleContent>span").get()
        scraped_text = "".join(response.css("div#articleContent>span *::text").getall())
        # print(scraped_title)
        # print(scraped_text)
        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "TheBlock"
        }

    def article_exists(self, title, link):
        with app.app_context():
            from app import Article as ArticleModel
            # Check if an article with the same link or title already exists in the database
            existing_article = ArticleModel.query.filter((ArticleModel.link == link) | (ArticleModel.title == title)).first()

            if existing_article:
                print(f"Article with the same link or title already exists: {link} - {title}")
                return True

        return False
