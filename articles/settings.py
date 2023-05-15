# -*- coding: utf-8 -*-
BOT_NAME = 'articles'

SPIDER_MODULES = ['articles.spiders']
NEWSPIDER_MODULE = 'articles.spiders'
DOWNLOAD_TIMEOUT = 240  # Set the download timeout
DOWNLOAD_DELAY = 2  # Add a delay between requests
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
HTTPCACHE_ENABLED = True
ITEM_PIPELINES = {
    'articles.pipelines.ArticlesPipeline': 300,
}
