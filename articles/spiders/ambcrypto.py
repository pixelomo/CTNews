import scrapy
import re
from articles.items import Article as ArticleItem
from app import app, db
from urllib.parse import urljoin
import datetime

class AmbcryptoSpider(scrapy.Spider):
    name = "ambcrypto"
    allowed_domains = ["ambcrypto.com"]
    start_urls = [
        'https://ambcrypto.com/category/new-news/',
    ]

    def parse(self, response):
        articles = response.css('.home-post')
        for article in articles:
            title = article.css('.home-post-content h2::text').get().strip()
            link = article.css('.home-post-image a::attr(href)').get()
            # Join the base URL with the extracted link
            link = urljoin(response.url, link)
            pubDateText = article.css('.home-post-cat .mvp-cd-date::text').get()
            pubDate = self.convert_to_datetime(pubDateText)
            if not self.article_exists(title, link):
                content_request = scrapy.Request(link, callback=self.parse_article)
                content_request.meta['title'] = title
                content_request.meta['pubDate'] = pubDate
                content_request.meta['link'] = link
                content_request.meta['source'] = "Ambcrypto"
                yield content_request

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        # Filter out script tags from the HTML
        scraped_html = ''.join(response.css(".single-post-main-middle").xpath('//*[not(self::script)]').getall())
        # Filter out script tags from the text
        scraped_text = ''.join(response.css(".single-post-main-middle *:not(script)::text").getall())
        scraped_text = re.sub(r'\n\s*\n', '\n\n', scraped_text)
        # print(scraped_text)
        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "Ambcrypto"
        }

    def convert_to_datetime(self, pubDate_text):
        if "hour" in pubDate_text:
            hours_ago = int(pubDate_text.split()[0])
            pubDate = datetime.datetime.now() - datetime.timedelta(hours=hours_ago)
        elif "minute" in pubDate_text:
            minutes_ago = int(pubDate_text.split()[0])
            pubDate = datetime.datetime.now() - datetime.timedelta(minutes=minutes_ago)
        else:
            # Handle other cases if needed
            pubDate = None

        if pubDate:
            return pubDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None

    def article_exists(self, title, link):
        with app.app_context():
            from app import Article as ArticleModel
            # Check if an article with the same link or title already exists in the database
            existing_article = ArticleModel.query.filter((ArticleModel.link == link) | (ArticleModel.title == title)).first()

            if existing_article:
                print(f"Article with the same link or title already exists: {link} - {title}")
                return True

        return False
