# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    location = scrapy.Field()
    workday = scrapy.Field()
    duration = scrapy.Field()
    modality = scrapy.Field()
    image = scrapy.Field()

    pass
