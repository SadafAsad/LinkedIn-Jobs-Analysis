# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    level = scrapy.Field()
    type = scrapy.Field()
    function = scrapy.Field()
    description = scrapy.Field()
