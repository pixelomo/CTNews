import scrapy
import requests
from requests.exceptions import RequestException
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
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".post-content").get()
        scraped_text = "".join(response.css(".post-content *::text").getall())

        api_url = "https://gentle-earth-02543.herokuapp.com/api/save_article"
        try:
            requests.post(api_url, json={
                "title": scraped_title,
                "pubDate": scraped_pubDate,
                "link": scraped_link,
                "text": scraped_text,
                "html": scraped_html
            })
        except RequestException as e:
            self.logger.error(f"Error sending data to the API: {e}")

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html
        }