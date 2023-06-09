import scrapy
from articles.items import Article as ArticleItem
from app import app, db
import datetime

class WublockSpider(scrapy.Spider):
    name = "wublock"
    allowed_domains = ["t.me"]
    start_urls = [
        'https://t.me/s/wublockchainenglish',
    ]

    def parse(self, response):
        articles = response.xpath("//div[contains(@class, 'tgme_widget_message')]")
        for article in articles:
            pubDate = article.xpath(".//time/@datetime").get()
            if pubDate:
                pubDate = datetime.datetime.fromisoformat(pubDate)
            title = article.xpath(".//div[contains(@class, 'tgme_widget_message_text')]/text()").get()
            link = article.xpath(".//a[contains(@class, 'tgme_widget_message_link_preview')]/@href").get() or article.xpath(".//a[contains(@class, 'tgme_widget_message_bubble')]/@href").get() or None
            html = article.get()

            with app.app_context():
                from app import Article as ArticleModel
                existing_article = ArticleModel.query.filter_by(link=link).first()

                if existing_article:
                    print(f"Article with the same link already exists: {link}")
                    return

            yield {
                "title": title,
                "pubDate": pubDate,
                "link": link,
                "text": None,
                "html": html,
                "source": "WuBlockchain"
            }



# https://www.odaily.news/newsflash
#  https://foresightnews.pro/news