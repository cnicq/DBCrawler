from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class IndicatorItem(Item):
	loc_name = Field()
	xls_url = Field()
	code = Field()
