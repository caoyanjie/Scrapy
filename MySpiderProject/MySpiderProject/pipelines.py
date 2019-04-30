# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as settings


class MyspiderprojectPipeline(object):
    def process_item(self, item, spider):
        return item


class VgchartzPipeline(object):
    def __init__(self):
        dbargs = {
            'host': 'localhost',
            'db': 'vgchartz',
            'user': 'root',
            'passwd': 'hello',
            'charset': 'utf8',
            'cursorclass': MySQLdb.cursors.DictCursor,
            'use_unicode': True,
        }
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):
        sql = f'''INSERT INTO vgchartzinfo(pos, game, weeks, yearly, total)
                  VALUES('{item.get("pos")}',
                         '{item.get("game")}',
                         '{item.get("weeks")}',
                         '{item.get("yearly")}',
                         '{item.get("total")}')'''
        conn.execute(sql)