import scrapy
from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem, UserItem
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import re
import sqlite3
from tieba import datatier


def user_parse(response):
    gender = 'm'
    follower_num = 0
    following_num = 0
    name = response.xpath('//span[@class="userinfo_username "]/text()').extract_first().strip()
    is_male = response.xpath('//span[@class="userinfo_sex userinfo_sex_male"]').extract_first()
    age = response.xpath('//span[contains(text(),"吧龄")]/text()').extract_first().strip()
    if (char.isdigit() for char in age):
        age = float(age[3:][:-1])
    else:
        age = 0.0
    post_str = response.xpath('//span[contains(text(),"发贴")]/text()').extract_first().strip()[3:]
    ip = response.xpath('//span[contains(text(),"IP属地")]/text()').extract_first().strip()
    if ip:
        ip = ip[5:]
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



def content_parse(content):
    if not content or not content.strip():
        return None
    content = content.replace('\r', '\n')
    s = BeautifulSoup(content, 'lxml')
    if s.html:
        s = s.html
    if s.body:
        s = s.body
    if s.div:
        s = s.div
    if s.p:
        s = s.p
    l = list(s.children)
    img_urls = []
    for i in range(len(l)):
        if l[i].name:
            if l[i].name == 'br':
                l[i] = '\n'
            elif l[i].name == 'img':
                l[i], url = process_image(l[i])
                if url != '':
                    img_urls.append(url)
            elif l[i].name == 'div':
                l[i] = process_div(l[i])
            else:
                l[i] = l[i].text
        else:
            l[i] = process_str(l[i])

    return ''.join(l), img_urls

def process_div(div):
    class_value = div.get('class')[0]
    if class_value == 'video_src_wrapper':
        return '[视频]'
    elif class_value == 'post_bubble_middle':
        return div.text
    elif class_value == 'voice_player':
        return '[语音]'
    else:
        return ''

def process_image(img):
    class_value = img.get('class')[0]
    if class_value == 'BDE_Smiley':
        return process_emoji(img), ''
    return '[图片]', img.get('src')

def process_str(str):
    return str.strip()

def process_emoji(emoji):
    sql = 'SELECT * FROM Emoji'
    dbConn = sqlite3.connect('tieba.db')
    emoji_table = datatier.select_n_rows(dbConn, sql)
    dbConn.close()

    match = re.search(r'i_f(\d+)|image_emoticon(\d+)', emoji.get('src'))
    number = 0
    if match:
        if 1 <= int(match.group(1) or match.group(2)) <= 50:
            number = int(match.group(1) or match.group(2))
    if number == 0:
        return '[表情]'
    return '[' + emoji_table[number-1][1] + ']'
