# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from movieproject.items import MovieprojectItem


class NnSpider(CrawlSpider):
    name = 'nn'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']

    # 提取页码链接
    page_link = LinkExtractor(allow=r'/movie/\?page=\d+')
    # 还要提取详情页链接
    detail_link = LinkExtractor(restrict_xpaths='//div[@class="movie-item-in"]/a')
    # 响应来了，从响应里面提取规则
    # 第一页的所有的详情页全部提取，解析数据并且保存
    # 页码链接也提取，但是提取后什么也不做，所以只有第一页的数据
    rules = (
        Rule(detail_link, callback='parse_item', follow=False),
        Rule(page_link, follow=False),
    )
    
    # 自己在当前的爬虫文件中定制管道这个选项，启动这个爬虫的时候，就是用下面的管道配置而不是settings里面的配置
    custom_settings = {
        'ITEM_PIPELINES': {
            'movieproject.pipelines.MovieMysqlPipeline': 301,
        }
    }

    # 就是处理详情页的函数
    def parse_item(self, response):
        # 就是在详情页提取电影的所有信息
        item = MovieprojectItem()
        # 接着提取其他信息
        # 提取海报
        poster = response.xpath('//a[@class="movie-post"]/img/@src').extract_first()
        # 提取电影名字
        name = response.xpath('//h1')[0].xpath('string(.)').extract_first()
        
        # 自己实现下面的两个提取
        # 提取电影类型
        movie_type = response.xpath('//span[contains(text(),"类型")]/../../td[2]')[0].xpath('string(.)').extract_first()
        # 提取电影评分
        score = response.xpath('//span[contains(text(),"评分")]/../../td[2]')[0].xpath('string(.)').extract_first()
        
        # 获取导演信息
        director = response.xpath('//div[@class="col-xs-8"]/table//tr[1]/td[2]')[0].xpath('string(.)').extract_first()
        # 获取编剧
        try:
            editor = response.xpath('//span[contains(text(),"编剧")]/../../td[2]')[0].xpath('string(.)').extract_first()
        except:
            editor = ''
        # 获取主演
        try:
            actor = response.xpath('//span[contains(text(),"主演")]/../../td[2]')[0].xpath('string(.)').extract_first()
        except:
            actor = ''
        # 获取地区
        area = response.xpath('//span[contains(text(),"地区")]/../../td[2]')[0].xpath('string(.)').extract_first()
        # 获取上映时间
        publish_time = response.xpath('//span[contains(text(),"上映时间")]/../../td[2]')[0].xpath('string(.)').extract_first()
        # 获取简介
        info = response.xpath('//div[@class="col-xs-12 movie-introduce"]/p/text()').extract_first()
        
        
        for field in ['director', 'editor', 'actor', 'area', 'publish_time', 'info', 'poster', 'name', 'movie_type', 'score']:
            item[field] = eval(field)
        
        # 将item仍走
        yield item
