# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FAFilmItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    synopsis = scrapy.Field()
    pass
