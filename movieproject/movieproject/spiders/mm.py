# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from movieproject.items import MovieprojectItem

class MmSpider(CrawlSpider):
    name = 'mm'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']

    page_link = LinkExtractor(allow=r'/movie/\?page=\d+')
    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )
    
    '''
    (1)向起始url发送请求之后，响应过来，没有回调处理这个响应，会使用默认的parse函数解析响应，就是根据规则提取链接的
        第一页提取的链接为：2 3 4 5 6 371
        
        从第2页的响应中接着按照规则提取链接：1 3 4 5 6 7 371
        第3也提取链接： 1 2 4 5 6 7 8 371
        4： 1 2 3 5 6 7 8 371
        
        3000，好多重复的，重复没有关系，关键是这3000个有没有全部的包含1-371
        重复会给你自动过滤掉
    '''

    def parse_item(self, response):
        print('*' * 100)
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
            
            yield item
