import scrapy
import datetime
from articles.items import Article

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
            link = article.xpath(".//a[contains(@class, 'tgme_widget_message_link_preview')]/@href").get() or article.xpath(".//a[contains(@class, 'tgme_widget_message_bubble')]/@href").get()

            yield Article(
                title=title,
                pubDate=pubDate,
                link=link,
                text=None,
                source="WuBlockchain",
            )

# https://www.odaily.news/newsflash
#  https://foresightnews.pro/news