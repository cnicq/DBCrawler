from DBCrawler.pipelines.File import FilePipeline
from scrapy.http import Request
import time
class SinaPipeline(FilePipeline):

    def get_media_requests(self, item, info):
        if item.get('cate'):
			csv_url = "http://money.finance.sina.com.cn/mac/view/vMacExcle.php?cate=%s&event=%s&from=0&num=9999999&condition=" % (item.get('cate')[0].encode("gbk"),item.get('event'))
			yield Request(csv_url)
