# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from maitian1.items import Maitian1Item

class Maitian1Pipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.db[Maitian1Item.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,Maitian1Item):
            self.db[item.collection].update({'id':item.get("id")},{'$set':item},True)
        return item