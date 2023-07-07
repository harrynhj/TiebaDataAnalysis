# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem
import sqlite3
import hashlib
from scrapy.utils.python import to_bytes
from . import datatier
from scrapy.pipelines.images import ImagesPipeline


class TiebaPipeline:
    def __init__(self):
        self.dbConn = None
        self.cnt = 0

    def open_spider(self, spider):
        self.dbConn = spider.dbConn
        pass

    def process_item(self, item, spider):
        if 'image_urls' in item:
            return item
        self.cnt += 1
        if item.item_name == 'SubTieba':
            self.insert_subtieba(item)
        elif item.item_name == 'Thread':
            self.insert_thread(item)
        elif item.item_name == 'Post':
            self.insert_post(item)
        elif item.item_name == 'Reply':
            self.insert_reply(item)
        elif item.item_name == 'Proxy':
            self.insert_proxy(item)
        elif item.item_name == 'User':
            self.insert_user(item)
        else:
            pass
        if self.cnt == 10:
            self.dbConn.commit()
            self.cnt = 0
        return item

    def insert_subtieba(self, item):
        sql = 'INSERT OR REPLACE INTO SubTiebas VALUES((?),(?),(?),(?),(?),(?));'
        datatier.perform_action(self.dbConn, sql, (item['sub_name'],
                                                   item['sub_title'],
                                                   item['follower_num'],
                                                   item['thread_num'],
                                                   item['mod_num'],
                                                   item['mod_id']))
        pass

    def insert_thread(self, item):
        sql = 'INSERT OR REPLACE INTO Threads VALUES((?),(?),(?),(?),(?),(?),(?),(?));'
        datatier.perform_action(self.dbConn, sql, (item['thread_id'],
                                                   item['thread_title'],
                                                   item['author_id'],
                                                   item['post_time'],
                                                   item['is_good'],
                                                   item['post_num'],
                                                   item['page_num'],
                                                   item['sub_name']))
        pass

    def insert_post(self, item):
        sql = 'INSERT OR REPLACE INTO Posts VALUES ((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?))'
        datatier.perform_action(self.dbConn, sql, (item['post_id'],
                                                   item['author_id'],
                                                   item['author_level'],
                                                   item['author_ip'],
                                                   item['author_device'],
                                                   item['date'],
                                                   item['content'],
                                                   item['floor'],
                                                   item['reply_num'],
                                                   item['image_num'],
                                                   item['image_str'],
                                                   item['thread_id']))

    def insert_reply(self, item):
        sql = 'INSERT OR REPLACE INTO Replies VALUES ((?),(?),(?),(?),(?),(?))'
        datatier.perform_action(self.dbConn, sql, (item['reply_id'],
                                                   item['author_id'],
                                                   item['content'],
                                                   item['time'],
                                                   item['reply_to'],
                                                   item['post_id']))

    def insert_user(self, item):
        sql = 'INSERT OR REPLACE INTO Users VALUES((?),(?),(?),(?),(?),(?),(?),(?),(?));'
        datatier.perform_action(self.dbConn, sql, (item['id'],
                                                   item['username'],
                                                   item['ip'],
                                                   item['age'],
                                                   item['gender'],
                                                   item['post_num'],
                                                   item['follower_num'],
                                                   item['following_num'],
                                                   item['gift_num']))

    def insert_proxy(self, item):
        sql = 'INSERT OR REPLACE INTO Proxies VALUES((?),(?),(?),(?),(?));'
        datatier.perform_action(self.dbConn, sql, (item['ip'],
                                                   item['port'],
                                                   item['type'],
                                                   item['username'],
                                                   item['password'],))
