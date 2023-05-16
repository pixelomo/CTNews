import scrapy
from articles.items import Article as ArticleItem
from app import app, db

class CryptoPanicSpider(scrapy.Spider):
    name = 'cryptopanic'
    start_urls = ['https://cryptopanic.com/news']
    allowed_domains = ["cryptopanic.com"]

    def parse(self, response):
        news_rows = response.css('.news-row')

        for row in news_rows:
            if not ('sponsored' in row.attrib['class'] or 'news-row-media' in row.attrib['class']):
                title = row.css('.title-text span:nth-child(1)::text').get()
                pub_date = row.css('.nc-date time::attr(datetime)').get()
                link = response.urljoin(row.css('.nc-title::attr(href)').get())
                source = row.css('.si-source-domain::text').get()

                # if link and "/magazine" not in link and not self.article_exists(title, link):
                yield scrapy.Request(link, callback=self.parse_article, meta={
                    'title': title,
                    'pubDate': pub_date,
                    'link': link,
                    "source": source,
                })

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]
        scraped_html = response.css(".post-content").get()
        scraped_text = "".join(response.css(".post-content *::text").getall())
        source = response.source

        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": source
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
