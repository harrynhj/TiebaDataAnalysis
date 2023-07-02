import scrapy
from tieba.items import ProxyItem


class TestSpiderSpider(scrapy.Spider):
    name = "TestSpider"
    start_url = "https://tieba.baidu.com/p/8465387023"
    cnt = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        self.cnt += 1
        print(response.url)
        print(self.cnt)
        if response.url == self.start_url:
            yield scrapy.Request(url=self.start_url, callback=self.parse)

