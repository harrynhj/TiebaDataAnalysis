import scrapy
import json

import tieba.datatier
from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem, UserItem, ImageItem
from urllib.parse import urlparse, parse_qs
from . import helper
from bs4 import BeautifulSoup
import re
import sqlite3


class ThreadspiderSpider(scrapy.Spider):
    name = 'ThreadSpider'
    tieba_name = ''
    current_page = 0
    start_page = 0
    end_page = 1000000
    url = 'https://tieba.baidu.com/f?kw='
    emoji_table = []

    def start_requests(self):
        self.url += self.tieba_name + '&pn='
        yield scrapy.Request(url=self.url+str(self.current_page), callback=self.parse)
        # yield scrapy.Request(url='https://tieba.baidu.com/p/8414238582', callback=self.thread_parse)

    def parse(self, response):
        for t in response.xpath('//li[contains(@class, "j_thread_list")]'):
            data = json.loads(t.xpath('@data-field').extract_first())
            if data['id'] == 1:
                continue
            item = ThreadItem()
            item['thread_id'] = data['id']
            item['thread_title'] = t.xpath('.//div[contains(@class, "threadlist_title")]/a/@title').extract_first()
            item['author_id'] = data['author_portrait']
            item['is_good'] = data['is_good']
            yield scrapy.Request(url='https://tieba.baidu.com/p/' + str(data['id']) + '?pn=1',
                                 callback=self.thread_parse, meta={'item': item, 'thread_id': data['id']})
        self.current_page += 50
        if response.xpath('//a[@class="last pagination-item "]').extract_first() is not None:
            if self.current_page < self.end_page:
                yield scrapy.Request(url=self.url + str(self.current_page), callback=self.parse)

        pass

    def thread_parse(self, response):
        thread_id = response.meta['thread_id']
        if response.meta['item']:
            thread_item = response.meta['item']
            thread_id = response.meta['item']['thread_id']
            first_floor = response.xpath('//div[contains(@class, "l_post ")]')
            data = json.loads(first_floor.xpath('@data-field').extract_first())
            date = response.xpath('.//span[@class="tail-info"][last()]/text()').extract_first()
            if date is None:
                thread_item['post_time'] = data['content']['date']
            else:
                thread_item['post_time'] = date
            thread_item['post_num'] = int(response.xpath('//span[@class="red"]/text()')[0].get())
            thread_item['page_num'] = int(response.xpath('//span[@class="red"]/text()')[1].get())
            thread_item['sub_name'] = response.xpath('//a[@class="card_title_fname"]/text()').extract_first().strip()[:-1]
            yield thread_item

        for p in response.xpath("//div[contains(@class, 'l_post')]"):
            if p.xpath(u".//span[contains(text(), '广告')]"):
                continue
            data = json.loads(p.xpath("@data-field").extract_first())

            post_id = data['content']['post_id']
            uid = data['author']['portrait'].split('?t=', 1)[0]
            level = p.xpath('.//div[@class="d_badge_lv"]/text()').extract_first()
            ip = p.xpath('.//span[contains(text(),"IP属地")]/text()').extract_first()
            if ip:
                ip = ip[5:]
            device = p.xpath('.//span[@class="tail-info"]/a/text()').extract_first()
            date = p.xpath('.//span[@class="tail-info"][last()]/text()').extract_first()
            if date is None:
                date = data['content']['date']
            floor = data['content']['post_no']
            reply_num = data['content']['comment_num']
            c = p.xpath(".//div[contains(@class,'j_d_post_content')]").extract_first()
            content, img_urls = helper.content_parse(c)
            # for url in img_urls:

            item = PostItem({
                'post_id': int(post_id),
                'author_id': uid,
                'author_level': int(level),
                'author_ip': ip,
                'author_device': device,
                'date': date,
                'content': content,
                'floor': int(floor),
                'reply_num': int(reply_num),
                'thread_id': int(thread_id)
            })
            yield item


            url = 'https://tieba.baidu.com/home/main/?id=' + uid
            yield scrapy.Request(url=url, callback=helper.user_parse, meta={'id': uid})

        next_page = response.xpath(u".//ul[@class='l_posts_num']//a[text()='下一页']/@href")
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url=url, callback=self.thread_parse, meta={'thread_id': thread_id})

        pass