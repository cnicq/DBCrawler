from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class IndicatorItem(Item):
	loc_name = Field()

class WorldBankIndicatorItem(IndicatorItem):
	xls_url = Field()
	code = Field()

class SinaItem(IndicatorItem):
	cate = Field()
	event = Field()

class HeXunItem(IndicatorItem):
	id = Field()
	url = Field()	