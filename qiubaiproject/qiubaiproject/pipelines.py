# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class QiubaiprojectPipeline(object):
    def open_spider(self,spider):
        self.fp = open('qiu.json','w',encoding='utf-8')

    # 处理item方法，每个item都会调用这个方法
    def process_item(self, item, spider):

        # 将item写入文件中
        # 先将item转换为字典
        dic_item = dict(item)
        # 将字典转换成json字符串
        json_str = json.dumps(dic_item,ensure_ascii=False)
        # 存到文件
        self.fp.write(json_str + '\n')
        return item

    def close_spider(self,spider):
        self.fp.close()