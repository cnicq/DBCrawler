# Scrapy settings for dirbot project

SPIDER_MODULES = ['DBCrawler.spiders']
NEWSPIDER_MODULE = 'DBCrawler.spiders'
DEFAULT_ITEM_CLASS = 'DBCrawler.items.Website'

ITEM_PIPELINES = ['DBCrawler.pipelines.FilterWordsPipeline']
