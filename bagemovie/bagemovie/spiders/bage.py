# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bagemovie.items import BagemovieItem

class BageSpider(CrawlSpider):
    name = 'bage'
    allowed_domains = ['www.8gw.com']
    start_urls = ['http://www.8gw.com/movie.html']

    rules = (
        # 定制按类型链接提取规则
        Rule(LinkExtractor(allow=r'/8gli/index\d+\.html'),  follow=False),
        # 定制页码提取规则
        Rule(LinkExtractor(allow=r'/8gli/index\d+_\d+\.html'),follow=True),
        # 定制详情页链接提取规则
        Rule(LinkExtractor(allow=r'/8gvi/\w+\.html'),callback='parse_item',follow=False)
    )

    def parse_item(self, response):
        item = BagemovieItem()

        # 提取数据
        item['title'] = response.xpath('//div[@class="moviedteail_tt"]/h1/text()').extract()[0]

        item['movie_type'] = response.xpath('//ul[@class="moviedteail_list"]/li[1]/a/text()').extract()[0]

        item['update'] = response.xpath('//ul[@class="moviedteail_list"]/li[2]/text()').extract()[0]

        item['actor'] = response.xpath('//ul[@class="moviedteail_list"]/li[3]').xpath('string(.)').extract()[0]

        item['director'] = response.xpath('//ul[@class="moviedteail_list"]/li[5]/a/text()').extract()[0]

        img = response.xpath('//div[@class="moviedteail_img"]/img/@src').extract()[0]
        item['img_path'] = ['http:'+ img]
        item['info'] = response.xpath('//div[@class="txt"]/text()').extract()[0]

        return item
