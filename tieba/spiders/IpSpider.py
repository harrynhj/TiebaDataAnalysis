import scrapy
from tieba.items import ProxyItem


class IpspiderSpider(scrapy.Spider):
    name = "IpSpider"
    start_url = "https://proxy.webshare.io/api/v2/proxy/list/download/pmztphlzmezrujtaoeorouugvvfozdbmgyopafeg/-/any/username/direct/-/"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        with open('test1.html', 'wb') as f:
            f.write(response.body)
        proxy_list = response.body.decode('utf-8')
        for line in proxy_list.strip().split('\n'):
            ip, port, username, password = line.split(':')
            item = ProxyItem({
                'ip': ip,
                'port': port,
                'type': 'http',
                'username': username,
                'password': password
            })
            yield item
