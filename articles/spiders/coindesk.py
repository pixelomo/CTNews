import scrapy
from articles.items import Article as ArticleItem
from app import app, db
from selenium import webdriver
from scrapy.selector import Selector

class CoindeskSpider(scrapy.Spider):
    name = "coindesk"
    allowed_domains = ["coindesk.com"]
    start_urls = [
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
    ]

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            title = item.xpath("title/text()").get()
            if link and not self.article_exists(title, link):
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    "title": title,
                    "pubDate": item.xpath("pubDate/text()").get(),
                    "source": "CoinDesk",
                })

    def parse_article(self, response):
        self.driver.get(response.url)
        scrapy_selector = Selector(text=self.driver.page_source)

        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]

        scraped_html_element = scrapy_selector.css(".at-content-wrapper > .at-content-wrapper")
        scraped_html = scraped_html_element.get()
        scraped_text = "".join(scraped_html_element.css("*::text").getall())

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "CoinDesk"
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
