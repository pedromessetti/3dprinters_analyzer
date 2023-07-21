# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PrinterscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PrinterItem(scrapy.Item):
    fonte = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    stars = scrapy.Field()
    num_reviews = scrapy.Field()
    #area = scrapy.Field()
    url = scrapy.Field()