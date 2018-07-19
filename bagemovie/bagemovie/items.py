# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BagemovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    movie_type = scrapy.Field()
    update = scrapy.Field()
    actor = scrapy.Field()
    director = scrapy.Field()
    img_path = scrapy.Field()
    info = scrapy.Field()


