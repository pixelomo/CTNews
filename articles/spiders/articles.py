import scrapy
from app import app, db, Article

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["cointelegraph.com"]
    start_urls = [
        'https://cointelegraph.com/rss',
    ]

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            if link:
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    "title": item.xpath("title/text()").get(),
                    "pubDate": item.xpath("pubDate/text()").get(),
                    "source": "Cointelegraph",
                })

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".post-content").get()
        scraped_text = "".join(response.css(".post-content *::text").getall())

        # Check if an article with the same link already exists in the database
        existing_article = Article.query.filter_by(link=scraped_link).first()

        if existing_article:
            print(f"Article with the same link already exists: {scraped_link}")
            return

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "Cointelegraph"
        }