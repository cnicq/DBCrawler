from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import WorldBankIndicatorItem
#Two step : 
#1.Parse cate name and event id from http://finance.sina.com.cn/mac/
#2.Download csv by URL : http://money.finance.sina.com.cn/mac/view/vMacExcle.php?cate=?&event=?&from=0&num=9999999&condition=
class SinaSpider(BaseSpider):
    name = "WorldBank"
    allowed_domains = ["finance.sina.com.cn/mac"]
    start_urls = [
        "http://finance.sina.com.cn/mac/",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        indicators = hxs.select('//a/@href')
        for indicator in indicators:
            url_str = indicator.extract()
            if ("http://data.worldbank.org.cn/indicator/") in url_str:
                yield Request(url=url_str, callback=self.parse_indicator)

    def parse_indicator(self, response):
        response_selector = HtmlXPathSelector(response)
        item = WorldBankIndicatorItem()
        item['xls_url'] = response_selector.select('//li[@class="download-xls first"][1]/a/@href').extract()
        if item['xls_url']  != "":
            return item
