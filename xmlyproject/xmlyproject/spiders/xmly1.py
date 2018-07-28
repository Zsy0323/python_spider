# -*- coding: utf-8 -*-
import scrapy
from ..items import XmlyprojectItem

class Xmly1Spider(scrapy.Spider):
    name = 'xmly1'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['https://www.ximalaya.com/youshengshu/']
    page = 2

    custom_settings = {
        'ITEM_PIPELINES': {
            'xmlyproject.pipelines.XmlyprojectPipeline': 300,
            'xmlyproject.pipelines.XmlyprojectMysqlPipeline': 301,
        }
    }

    def parse(self, response):
        item = XmlyprojectItem()
        # 找所有li
        li_list = response.xpath('//div[@class="content"]/ul/li')
        # 遍历
        for li in li_list:
            # 作者
            item['author'] = li.xpath('.//a[@class="e-2896848410 album-author"]/@title').extract_first()
            # 书名
            item['name'] = li.xpath('.//a[@class="e-2896848410 album-title"]/@title').extract_first()
            # 图片地址
            item['img'] = li.xpath('.//a[@class="e-1889510108 album-cover false needhover"]/img/@src').extract_first()
            # 热度
            item['hot'] = li.xpath('.//span[@class="e-1889510108"]').xpath('string(.)').extract_first()
            # 详情页链接
            href  = li.xpath('.//a[@class="e-2896848410 album-title"]/@href').extract_first()
            item['detail'] = 'https://www.ximalaya.com' + href


            yield item
        if self.page <= 5:
            url = 'https://www.ximalaya.com/youshengshu/p%d/' % self.page

            yield scrapy.Request(url=url,callback=self.parse)
            self.page += 1



