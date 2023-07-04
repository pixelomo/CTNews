import scrapy
from articles.items import Article as ArticleItem
from app import app, db

class CTJPSpider(scrapy.Spider):
    name = "ctjp"
    allowed_domains = ["jp.cointelegraph.com"]
    start_urls = [
        'https://jp.cointelegraph.com/rss',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'articles.stats_pipelines.StatsPipeline': 300,
        }
    }

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            title = item.xpath("title/text()").get()
            if link and "/magazine" not in link and not self.article_exists(title, link):
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    "title": title,
                    "pubDate": item.xpath("pubDate/text()").get(),
                    "source": "CTJP",
                })

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_text = "".join(response.css(".post-content *::text").getall())
        # print(scraped_title)

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "source": "CTJP"
        }

    def article_exists(self, title, link):
        with app.app_context():
            from app import ArticleStats
            # Check if an article with the same link or title already exists in the database
            existing_article = ArticleStats.query.filter((ArticleStats.link == link) | (ArticleStats.title == title)).first()

            if existing_article:
                print(f"Article with the same link or title already exists: {link} - {title}")
                return True

        return False
