import scrapy


class AfrilandfirstbankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
