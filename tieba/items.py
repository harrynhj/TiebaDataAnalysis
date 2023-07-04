# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SubTiebaItem(scrapy.Item):
    item_name = 'SubTieba'
    sub_name = scrapy.Field()
    sub_title = scrapy.Field()
    follower_num = scrapy.Field()
    thread_num = scrapy.Field()
    mod_num = scrapy.Field()
    mod_id = scrapy.Field()


class ThreadItem(scrapy.Item):
    item_name = 'Thread'
    thread_id = scrapy.Field()
    thread_title = scrapy.Field()
    author_id = scrapy.Field()
    post_time = scrapy.Field()
    is_good = scrapy.Field()
    post_num = scrapy.Field()
    page_num = scrapy.Field()
    sub_name = scrapy.Field()


class PostItem(scrapy.Item):
    item_name = 'Post'
    post_id = scrapy.Field()
    author_id = scrapy.Field()
    author_level = scrapy.Field()
    author_ip = scrapy.Field()
    author_device = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    floor = scrapy.Field()
    reply_num = scrapy.Field()
    thread_id = scrapy.Field()


class ReplyItem(scrapy.Item):
    item_name = 'Reply'
    author_id = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    post_id = scrapy.Field()


class UserItem(scrapy.Item):
    item_name = 'User'
    id = scrapy.Field()
    username = scrapy.Field()
    ip = scrapy.Field()
    age = scrapy.Field()
    gender = scrapy.Field()
    post_num = scrapy.Field()
    follower_num = scrapy.Field()
    following_num = scrapy.Field()
    gift_num = scrapy.Field()


class ProxyItem(scrapy.Item):
    item_name = 'Proxy'
    ip = scrapy.Field()
    port = scrapy.Field()
    type = scrapy.Field()
    username = scrapy.Field()
    password = scrapy.Field()
