# -*- coding: utf-8 -*-
BOT_NAME = 'articles'

SPIDER_MODULES = ['articles.spiders']
NEWSPIDER_MODULE = 'articles.spiders'
DOWNLOAD_TIMEOUT = 240  # Set the download timeout
DOWNLOAD_DELAY = 2  # Add a delay between requests
HTTPCACHE_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
ITEM_PIPELINES = {
    'articles.pipelines.ArticlesPipeline': 300,
}
