import scrapy


class CareerHistoryItem(scrapy.Item):
    politician_name = scrapy.Field()
    political_party_name = scrapy.Field()
    url = scrapy.Field()
