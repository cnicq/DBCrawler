from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import SinaItem

#Two step : 
#1.Parse cate name and event id from http://finance.sina.com.cn/mac/
#2.Download csv by URL : http://money.finance.sina.com.cn/mac/view/vMacExcle.php?cate=?&event=?&from=0&num=9999999&condition=
class SinaSpider(BaseSpider):
    name = "Sina"
    allowed_domains = ["finance.sina.com.cn/mac"]
    start_urls = [
        "http://finance.sina.com.cn/mac/",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        cates = hxs.select('//div[@class="tree_wrap"]/dl')
        n = 0
        for cate in cates:
            cate_param = cate.select('dt/@param').extract()
            n += 1;
            events = cate.select('dd/@param')
            for event in events:
                item = SinaItem()
                item['cate'] = cate_param
                item['event'] = event.extract()
                if item['cate']  != "":
                    yield item