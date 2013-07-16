# Scrapy settings for dirbot project
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

SPIDER_MODULES = ['DBCrawler.spiders']
NEWSPIDER_MODULE = 'DBCrawler.spiders'
DEFAULT_ITEM_CLASS = 'DBCrawler.items.IndicatorItem'

ITEM_PIPELINES = ['DBCrawler.pipelines.File.FilePipeline',]

FILE_STORE = os.path.join(PROJECT_DIR,'media/files')
FILE_EXTENTION = ['.csv','.xml','.xls','.zip']
ATTACHMENT_FILENAME_UTF8_DOMAIN = []
FILE_EXPIRES = 30