# -*- coding: utf-8 -*-
import scrapy

from movieproject.items import MovieprojectItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']
    
    # 自己实现多页爬取

    def parse(self, response):
        # 解析首页
        # 首先找到包含所有电影的div或者table
        div_list = response.xpath('//div[starts-with(@class,"col-xs-1-5")]')
        # 遍历这个div_list列表，提取每一个电影的信息
        for odiv in div_list:
            # 创建对象
            item = MovieprojectItem()
            # 电影海报
            item['poster'] = odiv.xpath('.//img/@data-original').extract()[0]
            # 电影名字
            item['name'] = odiv.xpath('.//h1/a/text()').extract()[0]
            # 电影评分
            item['score'] = odiv.xpath('.//h1/em/text()').extract()[0]
            # 电影类型
            item['movie_type'] = odiv.xpath('.//div[@class="otherinfo"]')[0].xpath('string(.)').extract()[0]
            
            # 提取所有详情页的链接
            detail_url = odiv.xpath('.//h1/a/@href').extract()[0]
            # 向详情页发送请求
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'xxx': item})
    
    def parse_detail(self, response):
        # 提取这个item的其它信息
        # 首先将item拿出来
        item = response.meta['xxx']
        # 接着提取其他信息
        # 获取导演信息
        director = response.xpath('//div[@class="col-xs-8"]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first()
        # 获取编剧
        try:
            editor = response.xpath('//span[contains(text(),"编剧")]/../../td[2]')[0].xpath('string(.)').extract_first()
        except:
            editor = ''
        # 获取主演
        # actor = response.xpath('//td[@id="casts"]')[0].xpath('string(.)').extract_first()
        try:
            actor = response.xpath('//span[contains(text(),"主演")]/../../td[2]')[0].xpath('string(.)').extract_first()
        except:
            actor = ''
        
        # rstrip(' 显示全部')
        # 获取地区
        # area = response.xpath('//div[@class="col-xs-8"]/table//tr[5]/td[2]/a/text()').extract_first()
        area = response.xpath('//span[contains(text(),"地区")]/../../td[2]')[0].xpath('string(.)').extract_first()
        # 获取上映时间
        # publish_time = response.xpath('//div[@class="col-xs-8"]/table//tr[7]/td[2]/text()').extract_first()
        publish_time = response.xpath('//span[contains(text(),"上映时间")]/../../td[2]')[0].xpath('string(.)').extract_first()
        # 获取简介
        info = response.xpath('//div[@class="col-xs-12 movie-introduce"]/p/text()').extract_first()
        # strip('\u3000')
        
        # item['director'] = director
        # item['editor'] = editor
        # item['actor'] = actor
        # item['area'] = area
        # item['publish_time'] = publish_time
        # item['info'] = info
        
        
        for field in ['director', 'editor', 'actor', 'area', 'publish_time', 'info']:
            # if item[field] == '':
            item[field] = eval(field)
        
        
        # 将item仍走
        yield item
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
