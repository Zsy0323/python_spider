# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 第一个页面要的信息
    # 电影海报
    poster = scrapy.Field()
    # 电影名字
    name = scrapy.Field()
    # 电影评分
    score = scrapy.Field()
    # 电影类型
    movie_type = scrapy.Field()
    
    # 第二个页面要的信息
    # 导演
    director = scrapy.Field()
    # 编剧
    editor = scrapy.Field()
    # 主演
    actor = scrapy.Field()
    # 地区
    area = scrapy.Field()
    # 上映时间
    publish_time = scrapy.Field()
    # 简介
    info = scrapy.Field()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
