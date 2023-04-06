import scrapy
import requests
from articles.items import Article

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
                })

    def parse_article(self, response):
        # ... scraping code ...
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".post-content").get()
        scraped_text = "".join(response.css(".post-content *::text").getall())

        # Send a POST request to the Flask API with the scraped data
        api_url = "http://localhost:5000/api/save_article"  # Update this URL if your Flask app is hosted elsewhere
        requests.post(api_url, json={
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html
        })

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html
        }


# import scrapy
# from articles.items import Article
# from app import app, Article as ArticleModel, db

# class ArticlesSpider(scrapy.Spider):
#     name = "articles"
#     allowed_domains = ["cointelegraph.com"]
#     start_urls = [
#         'https://cointelegraph.com/rss',
#     ]

#     def parse(self, response):
#         items = response.xpath("//item")
#         for item in items:
#             link = item.xpath("link/text()").get()
#             if link:
#                 yield scrapy.Request(link, callback=self.parse_article, meta={
#                     "title": item.xpath("title/text()").get(),
#                     "pubDate": item.xpath("pubDate/text()").get(),
#                 })

#     def parse_article(self, response):
#         scraped_title = response.meta["title"]
#         scraped_link = response.url
#         scraped_pubDate = response.meta["pubDate"]
#         scraped_html = response.css(".post-content").get()
#         scraped_text = "".join(response.css(".post-content *::text").getall())

#         with app.app_context():
#             article = ArticleModel(
#                 title=scraped_title,
#                 pubDate=scraped_pubDate,
#                 link=scraped_link,
#                 text=scraped_text,
#                 html=scraped_html
#             )
#             db.session.add(article)
#             db.session.commit()

#         yield {
#             "title": scraped_title,
#             "pubDate": scraped_pubDate,
#             "link": scraped_link,
#             "text": scraped_text,
#             "html": scraped_html
#         }