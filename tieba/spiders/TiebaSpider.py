import json
import scrapy
from tieba.items import SubTiebaItem, ThreadItem, PostItem, ReplyItem, UserItem
from urllib.parse import urlparse, parse_qs
from . import helper







class TiebaSpider(scrapy.Spider):
    name = 'TiebaSpider'
    tieba_url = 'https://tieba.baidu.com'
    visited = {}

    def start_requests(self):
        url = 'https://tieba.baidu.com/f?kw=' + self.tieba_name
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open('test.html', 'wb') as f:
            f.write(response.body)
        # Obtain tieba name
        sub_name = self.tieba_name
        sub_title = response.xpath('//p[@class="card_slogan"]/text()').extract_first()
        follower_num = int(response.xpath('//span[@class="card_menNum"]/text()').extract_first().replace(',', ''))
        thread_num = int(response.xpath('//span[@class="card_infoNum"]/text()').extract_first().replace(',', ''))
        has_mod = response.xpath('//div[@id="tbManagerApply" and @class="alwaysShow"]')
        mod_id = None
        mod_num = 0
        parse_user = True
        if not has_mod:
            mod_url = response.xpath('//a[@class="media_top manager_media"]/@href').extract_first()
            mod_id = parse_qs(urlparse(mod_url).query)
            if mod_id:
                mod_id = mod_id['id'][0]
            else:
                mod_id = response.xpath('substring-before(substring-after(//a[@class="thumbnail media_left"]/@href, '
                                        '"un="), "&")').extract_first()
                parse_user = False
            mod_cnt = len(response.xpath('//li[@class="media_vertical "]'))
            has_co_mod = response.xpath('//p[@class="forum_info_desc"]/em/text()').extract_first()
            co_mod_cnt = 0
            if has_co_mod is not None:
                co_mod_cnt = int(has_co_mod)
            mod_num = mod_cnt + co_mod_cnt
            if parse_user:
                yield scrapy.Request(url=self.tieba_url + mod_url, callback=helper.user_parse, meta={'id': mod_id})

        item = SubTiebaItem({
            'sub_name': sub_name[:-1],
            'sub_title': sub_title,
            'follower_num': follower_num,
            'thread_num': thread_num,
            'mod_num': mod_num,
            'mod_id': mod_id
        })
        yield item
        # while True:
        #
        #     for t in response.xpath('//li[contains(@class, "j_thread_list")]'):
        #         data = json.loads(t.xpath('@data-field').extract_first())
        #         print(data)






# xpath for deleted post
# //iframe[@id='error_404_iframe']
