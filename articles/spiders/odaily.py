import scrapy
import json
from articles.items import Article as ArticleItem
from app import app, db
import datetime

class ODailySpider(scrapy.Spider):
    name = "odaily"
    allowed_domains = ["odaily.news"]
    start_urls = [
        'https://www.odaily.news/api/pp/api/info-flow/newsflash_columns/newsflashes?b_id=&per_page=10',
    ]

    def parse(self, response):
        data = json.loads(response.text)
        articles = data.get('data', {}).get('items', [])
        for article in articles:
            title = article.get('title')
            link = article.get('url')
            pubDateText = article.get('published_at')
            pubDate = self.convert_to_datetime(pubDateText)
            html = "<p></p>"
            text = article.get('description')

            # print("Title: {}".format(title))
            # print("Description: {}".format(text))

            # if self.article_exists(title, link):
            #     continue

            item = ArticleItem()
            item["title"] = title
            item["pubDate"] = pubDate
            item["link"] = link
            item["text"] = text
            item["html"] = "<p></p>"
            item["source"] = "ODaily"

            yield item

    def convert_to_datetime(self, pubDate_text):
        return datetime.datetime.strptime(pubDate_text, '%Y-%m-%d %H:%M:%S')

    def article_exists(self, title, link):
        with app.app_context():
            from app import Article as ArticleModel
            # Check if an article with the same link or title already exists in the database
            existing_article = ArticleModel.query.filter((ArticleModel.link == link) | (ArticleModel.title == title)).first()

            if existing_article:
                print(f"Article with the same link or title already exists: {link} - {title}")
                return True

        return False
