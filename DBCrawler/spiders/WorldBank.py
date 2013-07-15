from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import IndicatorItem


class WorldBankSpider(BaseSpider):
    name = "WorldBank"
    allowed_domains = ["data.worldbank.org.cn"]
    start_urls = [
        "http://data.worldbank.org.cn/indicator",
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

        theIndicatorItem = IndicatorItem()
        theIndicatorItem['loc_name'] = response_selector.select('//h1[@class="page_title"][1]/text()').extract()
        theIndicatorItem['xls_url'] = response_selector.select('//li[@class="download-xls first"][1]/a/@href').extract()
        theIndicatorItem['code'] = response_selector.select('//link[@rel="canonical"][1]/@href').extract()

        print theIndicatorItem

        return theIndicatorItem
