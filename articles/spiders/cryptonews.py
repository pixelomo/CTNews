import scrapy
import re
from articles.items import Article as ArticleItem
from app import app, db

class CryptoNewsSpider(scrapy.Spider):
    name = "cryptonews"
    allowed_domains = ["cryptonews.com"]
    start_urls = [
        'https://cryptonews.com/news/',
    ]

    def parse(self, response):
        title = response.css('.article__title::text').get().strip()
        link = response.css('.article__title::attr(href)').get()
        pubDate = response.css('.article__badge-date::attr(data-utctime)').get()

        if not self.article_exists(title, link):
            # Fetch the article content
            content_request = scrapy.Request(link, callback=self.parse_article_content)
            content_request.meta['title'] = title
            content_request.meta['pubDate'] = pubDate
            content_request.meta['link'] = link
            content_request.meta['source'] = "CryptoNews"
            yield content_request

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".article-single__content").get()
        scraped_text = "".join(response.css(".article-single__content *::text").getall())
        # Remove the h1 tag from the scraped_html and scraped_text
        scraped_html = re.sub(r'<h1[^>]*>.*?</h1>', '', scraped_html)
        # Remove the first line from the scraped_text
        scraped_text_lines = scraped_text.splitlines()
        if len(scraped_text_lines) > 1:
            scraped_text = '\n'.join(scraped_text_lines[1:])
        else:
            scraped_text = ""

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "CryptoNews"
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
