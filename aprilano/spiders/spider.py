import scrapy

from scrapy.loader import ItemLoader
from ..items import AprilanoItem
from itemloaders.processors import TakeFirst


class AprilanoSpider(scrapy.Spider):
	name = 'aprilano'
	start_urls = ['https://www.aprila.no/no/newsfeed?hsLang=no']

	def parse(self, response):
		post_links = response.xpath('//article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/span/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::header)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=AprilanoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
