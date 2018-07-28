# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.utils.project import get_project_settings
# 爬虫一
class XmlyprojectPipeline(object):
    def __init__(self):
        self.fp = open('首页.json','w',encoding='utf8')

    def process_item(self, item, spider):
        jsr = json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(jsr + '\n')
        return item

    def close_spider(self,spider):
        self.fp.close()

# 存到数据库
class XmlyprojectMysqlPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['HOST']
        self.port = settings['PORT']
        self.user = settings['USER']
        self.password = settings['PASSWORD']
        self.charset = settings['CHARSET']
        self.db = settings['DBNAME']

        self.cnn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                                   charset=self.charset)

        self.cursor = self.cnn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into xmla1 (author,name1,img,hot,detail) values ("%s","%s","%s","%s","%s")' % (item['author'],item['name'],item['img'],item['hot'],item['detail'])
        # print('*'*100)
        # self.cursor.execute(sql)
        # self.cnn.commit()
        try:
            self.cursor.execute(sql)
            self.cnn.commit()
        except:
            print('*' * 100)
            self.cnn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.cnn.close()




