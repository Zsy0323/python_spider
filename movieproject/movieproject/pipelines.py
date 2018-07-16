# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class MovieprojectPipeline(object):
    def open_spider(self, spider):
        self.fp = open('movie.txt', 'w', encoding='utf8')
        
    def process_item(self, item, spider):
        d = dict(item)
        string = json.dumps(d, ensure_ascii=False)
        self.fp.write(string + '\n')
        return item
    
    def close_spider(self, spider):
        self.fp.close()

import pymysql
from scrapy.utils.project import get_project_settings 

class MovieMysqlPipeline(object):
    def open_spider(self, spider):
        # 读取配置文件中的配置信息
        settings = get_project_settings()
        host = settings['HOST']
        port = settings['PORT']
        user = settings['USER']
        password = settings['PASSWORD']
        dbname = settings['DBNAME']
        charset = settings['CHARSET']
        # 链接数据库
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname, charset=charset)
        # 获取游标
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        # 执行sql语句，写入到数据库中
        # 拼接sql语句
        sql = 'insert into movie(poster, name, score, movie_type, director, editor, actor, area, publish_time, info) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item['poster'], item['name'], item['score'], item['movie_type'], item['director'], item['editor'], item['actor'], item['area'], item['publish_time'], item['info'])

        # 执行sql语句
        try:
            self.cursor.execute(sql)
            # 提交一下
            self.conn.commit()
        except Exception as e:
            print('*' * 100)
            print(e)
            print('*' * 100)
            # 回滚
            self.conn.rollback()
        return item
    
    def close_spider(self, spider):
        #关闭游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()














