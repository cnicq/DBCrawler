# Scrapy settings for dirbot project
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

SPIDER_MODULES = ['DBCrawler.spiders']
NEWSPIDER_MODULE = 'DBCrawler.spiders'
DEFAULT_ITEM_CLASS = 'DBCrawler.items.IndicatorItem'

ITEM_PIPELINES = ['DBCrawler.pipelines.WorldBank.WorldBankPipeline',
'DBCrawler.pipelines.Sina.SinaPipeline',
'DBCrawler.pipelines.HeXun.HeXunPipeline',
'DBCrawler.pipelines.Talent.TalentPipeline']

FILE_STORE = os.path.join(PROJECT_DIR,'media/talent')
FILE_STORE_SINA = os.path.join(PROJECT_DIR,'media/sina')
FILE_STORE_HEXUN = os.path.join(PROJECT_DIR,'media/hexun')
FILE_EXTENTION = ['.csv','.xml','.xls','.zip','.doc','.txt','.docx','.rar','.pdf']
ATTACHMENT_FILENAME_UTF8_DOMAIN = []
FILE_EXPIRES = 30