# -*- coding: utf-8 -*-
import scrapy


class PostSpider(scrapy.Spider):
    name = 'post'
    allowed_domains = ['www.baidu.com']
    # start_urls = ['http://www.baidu.com/']
    #

    def start_requests(self):
        post_url = 'https://cn.bing.com/ttranslationlookup?&IG=BD9FBE8C6A4849D199FAD4276795A317&IID=translator.5036.7'
        data = {
        'from': 'zh - CHS',
        'to': 'en',
        'text': '女王',
        }

        yield scrapy.FormRequest(url=post_url,formdata=data,callback=self.parse)
    def parse(self, response):
        print('-'*100)
        print(response)
        print('-' * 100)