import scrapy
import re
import time
import os
from articles.items import Article as ArticleItem
from app import app, db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Check if the app is running on Heroku by looking for the 'DYNO' environment variable
on_heroku = 'DYNO' in os.environ

if on_heroku:
    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', 'chromedriver')
    chrome_driver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
else:
    chrome_driver_path = '/usr/local/bin/webdrivers/chromedriver'
    chrome_bin = None

options = Options()
options.headless = True
if chrome_bin:
    options.binary_location = chrome_bin

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

class CoindeskSpider(scrapy.Spider):
    name = "coindesk"
    allowed_domains = ["coindesk.com"]
    start_urls = [
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
    ]

    def parse(self, response):
        items = response.xpath("//item")
        for item in items:
            link = item.xpath("link/text()").get()
            title = item.xpath("title/text()").get()
            # if link and not self.article_exists(title, link):
            yield scrapy.Request(link, callback=self.parse_article, meta={
                "title": title,
                "pubDate": item.xpath("pubDate/text()").get(),
                "source": "CoinDesk",
            })

    def parse_article(self, response):
        scraped_title = response.meta["title"]
        scraped_link = response.url
        scraped_pubDate = response.meta["pubDate"]

        driver.get(scraped_link)

        time.sleep(5)

        scraped_html = driver.find_element(By.CSS_SELECTOR,"article div:nth-of-type(2)").get_attribute("outerHTML")
        scraped_text = "".join([elem.text for elem in driver.find_elements(By.CSS_SELECTOR,"article div:nth-of-type(2) *")])

        # Remove the h1 tag from the scraped_html and scraped_text
        scraped_html = re.sub(r'<h1[^>]*>.*?</h1>', '', scraped_html)
        # Remove the h1 / first line from the scraped_text
        scraped_text_lines = scraped_text.splitlines()
        if len(scraped_text_lines) > 1:
            scraped_text = '\n'.join(scraped_text_lines[1:])
        else:
            scraped_text = ""
        # print("<---------------------------------scraped_text------------------------------------------->")
        # print(scraped_title)
        # print(scraped_html)
        # print("<---------------------------------scraped_text------------------------------------------->")
        yield {
            "title": scraped_title,
            "pubDate": scraped_pubDate,
            "link": scraped_link,
            "text": scraped_text,
            "html": scraped_html,
            "source": "CoinDesk"
        }

    def closed(self, reason):
        driver.quit()

    def article_exists(self, title, link):
        with app.app_context():
            from app import Article as ArticleModel
            # Check if an article with the same link or title already exists in the database
            existing_article = ArticleModel.query.filter((ArticleModel.link == link) | (ArticleModel.title == title)).first()

            if existing_article:
                print(f"Article with the same link or title already exists: {link} - {title}")
                return True

        return False
