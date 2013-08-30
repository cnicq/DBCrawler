from DBCrawler.pipelines.File import FilePipeline
from scrapy.http import Request
import time
class HeXunPipeline(FilePipeline):

    def get_media_requests(self, item, info):
    	print "HeXunPipeline";
