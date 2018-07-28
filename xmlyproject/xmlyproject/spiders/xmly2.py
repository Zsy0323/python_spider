# -*- coding: utf-8 -*-
import scrapy
from ..items import XmlyprojectItem
from scrapy_redis.spiders import RedisSpider

# class Xmly2Spider(RedisSpider):
class Xmly2Spider(scrapy.Spider):
    name = 'xmly2'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['https://www.ximalaya.com/youshengshu/']
    redis_key = 'xmly2spider:start_urls'

    page = 2

    custom_settings = {


        'ITEM_PIPELINES': {
            'xmlyproject.pipelines2.Xmly2projectPipeline': 300,
            'xmlyproject.pipelines2.Xmly2projectMysqlPipeline': 301,
        },
        'DOWNLOAD_DELAY': '1',

    }

    def parse(self, response):

        # 找所有li
        li_list = response.xpath('//div[@class="content"]/ul/li')
        # 遍历
        for li in li_list:
            # 详情页链接
            href  = li.xpath('.//a[@class="e-2896848410 album-title"]/@href').extract_first()
            href = 'https://www.ximalaya.com' + href
            yield scrapy.Request(url=href,callback=self.parse_detail)


        if self.page <= 5:
            url = 'https://www.ximalaya.com/youshengshu/p%d/' % self.page

            yield scrapy.Request(url=url,callback=self.parse)
            self.page += 1

    def parse_detail(self,response):
        item = XmlyprojectItem()
        # 书名
        item['name'] = response.xpath('//h1[@class="e-630486218 title"]/text()').extract_first()
        #更新日期
        item['update'] = response.xpath('//span[@class="e-630486218 time"]').xpath('string(.)').extract_first()

        # 图片地址
        item['img'] = response.xpath('//img[@class="e-630486218 img"]/@src').extract_first()
        # 热度
        item['hot'] = response.xpath('//span[@class="e-630486218 count"]').xpath('string(.)').extract_first()

        # 类型
        item['types'] = response.xpath('//div[@class="e-630486218 tags"]').xpath('string(.)').extract_first()
        # 简介
        item['info'] = response.xpath('//article[@class="e-630486218 intro"]/p/span').xpath('string(.)').extract_first()

        #声音标题和地址


        yield item


