import scrapy

from scrapy.loader import ItemLoader

from ..items import AfrilandfirstbankItem
from itemloaders.processors import TakeFirst


class AfrilandfirstbankSpider(scrapy.Spider):
	name = 'afrilandfirstbank'
	start_urls = ['https://www.afrilandfirstbank.com/index.php/en/news?limitstart=0']

	def parse(self, response):
		post_links = response.xpath('//p[@class="readmore"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content-frame"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AfrilandfirstbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
