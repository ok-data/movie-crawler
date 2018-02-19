# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	movie_name = scrape.Field()
	movie_code = scrape.Field()
	dir_name = scrape.Field()
	dir_code = scrape.Field()
	release_year = scrape.Field()
	nation = scrape.Field()

    pass
