# -*- coding: utf-8 -*-
BOT_NAME = 'articles'

SPIDER_MODULES = ['articles.spiders']
NEWSPIDER_MODULE = 'articles.spiders'
DOWNLOAD_TIMEOUT = 480  # Set the download timeout
DOWNLOAD_DELAY = 1.5  # Add a delay between requests
HTTPCACHE_ENABLED = True
ITEM_PIPELINES = {
    'articles.pipelines.ArticlesPipeline': 300,
}
