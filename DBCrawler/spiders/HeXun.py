from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import HeXunItem
import re
import csv

#Two step : 
#1.Parse cate name and event id from http://mac.hexun.com
class HeXunSpider(BaseSpider):
    name = "HeXun"
    allowed_domains = ["mac.hexun.com"]
    start_urls = [
        "http://mac.hexun.com/",
    ]
    indicatort_info = {}

    def parse(self, response):
        self.totalpage = 0;
        hxs = HtmlXPathSelector(response)
        ids = hxs.select('//a[contains(@href, "Default.shtml?id=")]/@href').extract();
        for id in ids:
            id_param = re.match(r'Default.shtml\?id=(.*)', id)
            if id_param is not None:
                urllink = "http://mac.hexun.com/Details/" + id_param.group(1).strip() + ".shtml?pid=1";
                print urllink;
                yield Request(url=urllink, callback=self.parse_firestpage)
    
    def parse_firestpage(self, response):
        Item = HeXunItem()
        hxs = HtmlXPathSelector(response)
        self.indicatort_info['total_pages'] = '';
        self.indicatort_info['taget2s'] = [];

        #"Talbe scroll_title, scroll_title1, scroll_list, scroll_list1";
        #1.check scroll_list1 tr counter
        rows = hxs.select("//table[@id='scroll_title1']/tr")
        for row in rows:
            spans = row.select("//td[contains(@id,'col')]/span/text()");
            print len(spans);
            for span in spans:
                print span.extract();
        #for id in ids:
        #    print id;
        #print len(rows);
        #yield Request(url=urllink, callback=self.parse_nextpage)

    def parse_nextpage(self, response):
        Item = HeXunItem()
        hxs = HtmlXPathSelector(response)

