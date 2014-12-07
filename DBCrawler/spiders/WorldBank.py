from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import WorldBankIndicatorItem

class WorldBankSpider(BaseSpider):
    name = "WorldBank"
    allowed_domains = ["data.worldbank.org.cn"]
    start_urls = [
        "http://data.worldbank.org.cn/indicator/all?display=default",
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
        print '--------11111------------'
        print item['xls_url']
        print '--------22222------------'
        if item['xls_url']  != "":
            return item
