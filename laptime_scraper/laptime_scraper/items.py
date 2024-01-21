# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LaptimeItem(scrapy.Item):
    lap = scrapy.Field()
    position = scrapy.Field()
    lap_time = scrapy.Field()
    pit_stop_time = scrapy.Field()
    driver_name = scrapy.Field()
    driver_surname = scrapy.Field()
    race = scrapy.Field()
    pass
