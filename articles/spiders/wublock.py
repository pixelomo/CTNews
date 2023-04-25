import scrapy
from articles.items import Article

class WublockSpider(scrapy.Spider):
    name = "wublock"
    allowed_domains = ["web.telegram.org", "t.me"]
    start_urls = [
        'http://fetchrss.com/rss/6447538cda605f38e77dc503644753962bdd8d1a31560e23.xml',  # Replace with the fetchrss.com generated RSS feed URL
    ]

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            if link:
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    "title": item.xpath("title/text()").get(),
                    "pubDate": item.xpath("pubDate/text()").get(),
                    "source": "Wublock",
                })

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".post-content").get()
        scraped_text = "".join(response.css(".post-content *::text").getall())

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": response.meta["source"],
        }
