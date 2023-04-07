# -*- coding: utf-8 -*-

BOT_NAME = 'articles'

SPIDER_MODULES = ['articles.spiders']
NEWSPIDER_MODULE = 'articles.spiders'

ROBOTSTXT_OBEY = True
HTTPCACHE_ENABLED = True
ITEM_PIPELINES = {
    'articles.pipelines.ArticlesPipeline': 300,
}
