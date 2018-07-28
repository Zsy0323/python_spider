# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.utils.project import get_project_settings


# 爬虫一
class Xmly2projectPipeline(object):
    def __init__(self):
        self.fp = open('详情页.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        jsr = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write(jsr + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()


# 存到数据库
class Xmly2projectMysqlPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['HOST']
        self.port = settings['PORT']
        self.user = settings['USER']
        self.password = settings['PASSWORD']
        self.charset = settings['CHARSET']
        self.db = settings['DBNAME']

        self.cnn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)

        self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into xmla2 (img,name1,update_time,hot,types,info) values ("%s","%s","%s","%s","%s","%s")' % (
        item['img'], item['name'], item['update'], item['hot'], item['types'],item['info'])
        # print('*'*100)
        try:
            self.cursor.execute(sql)
            self.cnn.commit()
        except:
            print('*' * 100)
            self.cnn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnn.close()



class Xmly3projectMysqlPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['HOST']
        self.port = settings['PORT']
        self.user = settings['USER']
        self.password = settings['PASSWORD']
        self.charset = settings['CHARSET']
        self.db = settings['DBNAME']

        self.cnn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)

        self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into xmla3 (voice) values ("%s")' % (
        item['voice'])
        # print('*'*100)
        try:
            self.cursor.execute(sql)
            self.cnn.commit()
        except:
            print('*' * 100)
            self.cnn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnn.close()
