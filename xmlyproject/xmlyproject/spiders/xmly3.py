# -*- coding: utf-8 -*-
import scrapy
from ..items import XmlyprojectItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


# class Xmly3Spider(RedisCrawlSpider):
class Xmly3Spider(CrawlSpider):
    name = 'xmly3'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['https://www.ximalaya.com/youshengshu/']
    # redis_key = 'xmly3spider:start_urls'

    page_link = LinkExtractor(allow=r'/youshengshu/\d+/')
    # 还要提取详情页链接
    detail_link = LinkExtractor(allow=r'/youshengshu/\d+/p\d+/')
    # 响应来了，从响应里面提取规则
    # 第一页的所有的详情页全部提取，解析数据并且保存
    # 页码链接也提取，但是提取后什么也不做，所以只有第一页的数据
    rules = (
        Rule(detail_link, callback='parse_item', follow=False),
        Rule(page_link, callback='parse_item', follow=False),
    )


    custom_settings = {

        # 'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        # 'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        # 'SCHEDULER_PERSIST': True,
        'ITEM_PIPELINES': {
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
            # 'xmlyproject.pipelines2.XmlyprojectPipeline': 300,
            'xmlyproject.pipelines2.Xmly3projectMysqlPipeline': 301,
        },
        # 'DOWNLOAD_DELAY': '1',
        # # 配置redis的地址和端口
        # 'REDIS_HOST': '10.36.132.227',
        # 'REDIS_PORT': '6379',
    }


    def parse_item(self,response):
        item = XmlyprojectItem()

        #声音标题和地址
        li_list = response.xpath('//li[@class="e-2304105070"]')
        dic = {}
        for i in range(len(li_list)):
            dic[str(i + 1) + 'title'] = li_list[i].xpath('.//div[@class="e-2304105070 text"]/a/text()').extract_first()

            dic[str(i + 1) + 'href'] = 'https://www.ximalaya.com' + li_list[i].xpath('.//div[@class="e-2304105070 text"]/a/@href').extract_first()
        item['voice'] = str(dic)

        yield item


