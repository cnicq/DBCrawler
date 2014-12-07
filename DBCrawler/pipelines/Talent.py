from DBCrawler.pipelines.File import FilePipeline
from scrapy.http import Request

class TalentPipeline(FilePipeline):

    def get_media_requests(self, item, info):
        if item.get('xls_url') and len(item['xls_url']) > 0:
            yield Request(item['xls_url'][0]);