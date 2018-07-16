# -*- coding: utf-8 -*-
import scrapy

from qiubaiproject.items import QiubaiprojectItem


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    page = 1
    url = 'https://www.qiushibaike.com/8hr/page/{}/'

    def parse(self, response):
        items = []
        # print(response.text)
        div_list = response.xpath('//div[starts-with(@id,"qiushi_tag")]')
        # print(len(div_list))
        # 遍历这个列表，依次找到每一个段子的这些你要的数据
        for odiv in div_list:
            # 获取用户头像   这个点必须加
            face = odiv.xpath('.//div[@class="author clearfix"]/a/img/@src').extract_first()
            # 获取用户名字
            name = odiv.xpath('.//h2/text()')[0].extract()
            # 用户年龄
            age = odiv.xpath('.//div[starts-with(@class,"articleGender")]/text()').extract_first()
            # 发表内容
            content = odiv.xpath('.//div[@class="content"]/span[1]')[0].xpath('string(.)')[0].extract().strip('\n\r\t ')
            # 获取好笑个数
            haha_count = odiv.xpath('.//span[@class="stats-vote"]//i/text()')[0].extract()
            # 获取评论个数
            ping_count = odiv.xpath('.//span[@class="stats-comments"]//i/text()')[0].extract()

            item = QiubaiprojectItem()

            item['face'] = face
            item['name'] = name
            item['age'] = age
            item['content'] = content
            item['haha_count'] = haha_count
            item['ping_count'] = ping_count

            yield item

        # 接着发送请求

        if self.page <= 5:
            self.page += 1
            url = self.url.format(self.page)
            # 接着发送
            yield scrapy.Request(url=url,callback=self.parse)