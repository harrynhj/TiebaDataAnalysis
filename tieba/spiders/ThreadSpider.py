from math import ceil

import scrapy
import json

import tieba.datatier
from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem, UserItem
from urllib.parse import urlparse, parse_qs
from . import helper
from bs4 import BeautifulSoup, NavigableString
import re
import sqlite3
from lxml import html


class ThreadspiderSpider(scrapy.Spider):
    name = 'ThreadSpider'
    tieba_name = ''
    start_page = 0
    current_page = 0 + start_page
    end_page = 1000000
    url = 'https://tieba.baidu.com/f?kw='
    emoji_table = []
    visited = set()

    def start_requests(self):
        self.url += self.tieba_name + '&pn='
        yield scrapy.Request(url=self.url + str(self.current_page), callback=self.parse)

    def parse(self, response):
        for t in response.xpath('//li[contains(@class, "j_thread_list")]'):
            data = json.loads(t.xpath('@data-field').extract_first())
            if data['id'] == 1:
                continue
            item = ThreadItem()
            item['thread_id'] = data['id']
            if data['id'] in self.visited:
                continue
            item['thread_title'] = t.xpath('.//div[contains(@class, "threadlist_title")]/a/@title').extract_first()
            item['author_id'] = data['author_portrait']
            if not item['author_id']:
                item['author_id'] = 'ip'
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
        if 'item' in response.meta:
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
            thread_item['sub_name'] = self.tieba_name
            yield thread_item

        for p in response.xpath("//div[contains(@class, 'l_post')]"):
            if helper.get_post_info(p, thread_id):
                p_item, img_urls, is_anonym = helper.get_post_info(p, thread_id)
            else:
                continue
            if img_urls:
                yield {'image_urls': img_urls, 'tieba_name': self.tieba_name}
            yield p_item

            if p_item['reply_num'] != 0:
                pages = ceil(p_item['reply_num'] / 10.0)
                for i in range(1, pages):
                    url = "https://tieba.baidu.com/p/comment?tid=%d&pid=%d&pn=%d" \
                          % (thread_id, p_item['post_id'], i)
                    yield scrapy.Request(url, callback=self.reply_parse, meta={'post_id': p_item['post_id']})

            url = 'https://tieba.baidu.com/home/main/?id=' + p_item['author_id']
            if not is_anonym:
                if p_item['author_id'] not in self.visited:
                    self.visited.add(p_item['author_id'])
                    yield scrapy.Request(url=url, callback=helper.user_parse, meta={'id': p_item['author_id']})

        next_page = response.xpath(u".//ul[@class='l_posts_num']//a[text()='下一页']/@href")
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url=url, callback=self.thread_parse, meta={'thread_id': thread_id})

    def reply_parse(self, response):
        reply_list = response.xpath('body/li')[:-1]
        for r in reply_list:
            data = json.loads(r.attrib['data-field'])
            reply_id = data['spid']
            author_id = data['portrait']
            c = r.xpath('.//span[@class = "lzl_content_main"]').extract_first()
            content = self.reply_content(c)
            reply_to = self.extract_portrait(c)
            time = r.css('.lzl_time').xpath('./text()').get()
            post_id = response.meta['post_id']
            item = ReplyItem({'reply_id': reply_id,
                              'author_id': author_id,
                              'content': content,
                              'time': time,
                              'reply_to': reply_to,
                              'post_id': post_id})
            yield item


    def reply_content(self, reply):
        soup = BeautifulSoup(reply, 'html.parser')
        result = ''

        def traverse(node):
            nonlocal result
            if isinstance(node, NavigableString):
                result += node
            elif node.name == 'img':
                result += helper.process_emoji(node)
            else:
                for child in node.children:
                    traverse(child)
        traverse(soup)
        return result.strip()

    def extract_portrait(self, reply):
        tree = html.fromstring(reply)
        portrait = tree.xpath('.//a[@class="at"]/@portrait')
        return portrait[0] if portrait else None
