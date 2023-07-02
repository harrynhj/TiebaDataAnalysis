import scrapy
from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem, UserItem
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import re
import sqlite3


def user_parse(response):
    gender = 'm'
    follower_num = 0
    following_num = 0
    name = response.xpath('//span[@class="userinfo_username "]/text()').extract_first().strip()
    is_male = response.xpath('//span[@class="userinfo_sex userinfo_sex_male"]').extract_first()
    age = float(response.xpath('//span[contains(text(),"吧龄")]/text()').extract_first().strip()[3:][:-1])
    post_str = response.xpath('//span[contains(text(),"发贴")]/text()').extract_first().strip()[3:]
    ip = response.xpath('//span[contains(text(),"IP属地")]/text()').extract_first().strip()[5:]
    follower_str = response.xpath('//h1[contains(text(), "关注他的人")]/span/a/text()').extract_first()
    following_str = response.xpath('//h1[contains(text(), "他关注的人")]/span/a/text()').extract_first()
    gift_num = int(response.xpath('//span[@class="gift-num"]/i/text()').extract_first())
    if is_male is None:
        gender = 'f'
    if post_str[-1] == '万':
        post_num = int(float(post_str[:-1]) * 10000)
    else:
        post_num = float(post_str)
    if follower_str is not None:
        follower_num = int(follower_str)
    if following_str is not None:
        following_num = int(following_str)

    item = UserItem({
        'id': response.meta['id'],
        'username': name,
        'ip': ip,
        'age': age,
        'gender': gender,
        'post_num': post_num,
        'follower_num': follower_num,
        'following_num': following_num,
        'gift_num': gift_num,
    })
    yield item


