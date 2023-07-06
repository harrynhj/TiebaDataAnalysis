from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sqlite3
from tieba import datatier
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy import signals

completed_spiders = 0
dbConn = sqlite3.connect('tieba.db')
process = CrawlerProcess(get_project_settings())
crawl_list = ['禾野', '乌克兰', '抗压背锅',
                  '中国人口', '动漫', '图拉丁',
                  'ps', '土木工程', '地理',
                  '数学', 'bilibili', '显卡',
                  '地狱笑话', '天堂鸡汤', '汽车',
                  '手机', 'mihoyo', 'v', '原神内鬼',
                  '2ch', '四川大学', '4soul', '印度',
                  '病毒', 'steam', '以太比特',
                  '航空母舰', 'ff14', '化学', '核战避难所',
                  '碧蓝档案', '碧蓝航线', 'fate', '剑网3',
                  '王者荣耀', '肖战', '艾欧尼亚', '黑色玫瑰',
                  'dota2', '弱智', '明日方舟', '孙笑川',
                  '桌饺', '明日方舟脚臭', '崩坏星穹铁道',
                  'csgo', 'csgo饰品交易', '半壁江山雪之下',
                  '钓鱼', '放生', '树疗', '素食', '迷你世界',
                  'minecraft', 'ps5', 'xbox', 'ps4', 'ns',
                  '笔记本', '我推的孩子', '吊图', '沙井',
                  '国产动画', '生个女孩', '新孙笑川', 'lolid', 'lol半价',
                  'apex英雄', 'lck', 'lpl', 'edg', 'rng', 'blg', 'jdg',
                  'uzi', '北京国安', '高达', '汪峰在', '孙吧福利区', '杨超越',
                  '高考', '反原神', '电锯人', '约稿', '女性向游戏吐槽', 'lol淋价',
                  '杰克马原神', '追寻繁星的少年', 'galgame', '公务员', '萌战', '考研',
                  '快乐雪花', '真夏夜的银梦', '地下城与勇士', 'cookie', '河南', '浙江', '北京',
                  '福建', '新冠病毒', '米浴', '助手', '毛利兰', '灰原哀', '名侦探柯南', 'eva', '火影忍者',
                  '海贼王', '死神', '进击的巨人', '兵长', '反二次元', '二次元', 'rimworld', '东方', '渚薰',
                  '碇真嗣', 'intel', 'amd', '名作之壁', '那年那兔那些事儿']

def spider_closed(spider, reason):
    print(f'Spider closed: {reason}')
    dbConn.commit()
    global completed_spiders
    completed_spiders += 1
    if completed_spiders == 2:
        completed_spiders = 0
        if crawl_list:
            t = crawl_list.pop(0)
            process.crawl('TiebaSpider', tieba_name=t, dbConn=dbConn)
            process.crawl('ThreadSpider', tieba_name=t, dbConn=dbConn, end_page=500)

def main():
    datatier.perform_action(dbConn, 'DELETE FROM Proxies;')
    dbConn.commit()
    process.crawl('IpSpider', dbConn=dbConn)

    if crawl_list:
        t = crawl_list.pop(0)
        process.crawl('TiebaSpider', tieba_name=t, dbConn=dbConn)
        process.crawl('ThreadSpider', tieba_name=t, dbConn=dbConn, end_page=500)
    for p in process.crawlers:
        p.signals.connect(spider_closed, signal=signals.spider_closed)
    process.start()

    dbConn.commit()
    dbConn.close()


if __name__ == '__main__':
    main()
