import scrapy
from bs4 import BeautifulSoup
from articles.items import Article

class WublockSpider(scrapy.Spider):
    name = "wublock"
    allowed_domains = ["fetchrss.com"]
    # https://t.me/s/wublockchainenglish
    start_urls = [
        'http://fetchrss.com/rss/6447538cda605f38e77dc503644753962bdd8d1a31560e23.xml',
    ]

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            description = item.xpath("description/text()").get()
            soup = BeautifulSoup(description, "html.parser")
            link = soup.find("a", href=True)["href"]

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
        scraped_html = response.body  # The entire content as there is no specific container
        scraped_text = "".join(response.css("body *::text").getall())

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": response.meta["source"],
        }
