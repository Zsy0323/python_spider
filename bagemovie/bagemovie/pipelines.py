# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.utils.project import get_project_settings
# 存储到文本文件
class BagemoviePipeline(object):
    def __init__(self):
        self.fp = open('bage.txt','w',encoding='utf8')
    def process_item(self, item, spider):

        self.fp.write(str(item)+'\n')
        return item

    def close_spider(self,spider):
        self.fp.close()

class MovieImgPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        for url in item['img_path']:
            yield Request(url)

    def item_completed(self, results, item, info):
        img_path = [x['path'] for ok,x in results if ok]
        os.rename(self.img_store + '\\' + img_path[0],self.img_store + '\\' + item['title'] + '.jpg')

        if not img_path:
            raise DropItem('NO images')

        item['img_path'] = self.img_store + '\\' + item['title']


        return item

