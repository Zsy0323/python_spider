# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XmlyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    hot = scrapy.Field()
    detail = scrapy.Field()

    # 详情页
    update = scrapy.Field()
    types = scrapy.Field()
    info = scrapy.Field()


    voice = scrapy.Field()

