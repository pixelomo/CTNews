import scrapy
import re
from articles.items import Article as ArticleItem
from app import app, db
from urllib.parse import urljoin

class BlockworksSpider(scrapy.Spider):
    name = "blockworks"
    allowed_domains = ["blockworks.co"]
    start_urls = [
        'https://blockworks.co/news',
    ]

    def parse(self, response):
        articles = response.css('main .grid-cols-1')
        for article in articles:
            title = article.css('.font-headline::text').get().strip()
            link = article.css('.font-headline::attr(href)').get()
            # Join the base URL with the extracted link
            link = urljoin(response.url, link)
            pubDate = article.css('time::attr(datetime)').get()
            if not self.article_exists(title, link):
                content_request = scrapy.Request(link, callback=self.parse_article)
                content_request.meta['title'] = title
                content_request.meta['pubDate'] = pubDate
                content_request.meta['link'] = link
                content_request.meta['source'] = "Blockworks"
                yield content_request

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css("article .gap-6.w-full").get()
        scraped_text = "".join(response.css("article .gap-6.w-full *::text").getall())
        # print(scraped_title)
        # print(scraped_html)
        # print(scraped_text)
        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "Blockworks"
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
