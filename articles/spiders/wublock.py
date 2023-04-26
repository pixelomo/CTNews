import scrapy
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
            pubDate = datetime.datetime.fromisoformat(pubDate)
            title = article.xpath(".//h4/text()").get()
            text = article.xpath(".//div[contains(@class, 'tgme_widget_message_text')]/text()").get()
            link = article.xpath(".//a[contains(@class, 'tgme_widget_message_link_preview')]/@href").get()

            yield Article(
                title=title,
                pubDate=pubDate,
                link=link,
                text=text,
                source="WuBlockchain",
            )

# https://t.me/s/wublockchainenglish
# https://twitter.com/WuBlockchain
# https://www.odaily.news/newsflash
#  https://foresightnews.pro/news