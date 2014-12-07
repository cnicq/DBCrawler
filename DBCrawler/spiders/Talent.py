from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from DBCrawler.items import TalentItem

class TalentSpider(BaseSpider):
	name = "Talent"
	allowed_domains= ["unet.hunteron.com"]
	login_page = 'http://unet.hunteron.com'
	start_urls=[
		"http://unet.hunteron.com/?m=candidate&c=candidate&a=list"
	]

	def init_request(self):
		return Request(url=self.login_page, callback=self.login)
	def loing(self, response):
		return FormRequest.form_response(response, formdata={'username':'joyce','password':'joyce123'}, callback=self.check_login_response)

	def check_login_response(self, response):
		if "Check your username and password" in response.body:
			self.log("Bad times :(")
		# Something went wrong, we couldn't log in, so nothing happens.
		else:
			self.log("Successfully logged in. Let's start crawling!")
		# Now the crawling can begin..
		self.initialized()

	def parse(self, response):
		for id in xrange(1, 2):
			url_str = "http://unet.hunteron.com/?m=candidate&c=candidate&a=show&id=%d"%(id)
			yield Request(url=url_str, callback=self.parse_talent)

	def parse_talent(self, response):
		response_selector = HtmlXPathSelector(response)
		candidate_info = response_selector.select(u'//body/node()').extract()
		item = TalentItem()
		print '--------11111------------'
		print candidate_info
		print '--------22222------------'
		return item;