from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sqlite3

def main():
    dbConn = sqlite3.connect('tieba.db')
    process = CrawlerProcess(get_project_settings())
    #process.crawl('TiebaSpider', tieba_name='乌克兰', dbConn=dbConn)
    process.crawl('ThreadSpider', tieba_name="乌克兰", dbConn=dbConn, end_page=50)
    #process.crawl('TestSpider', tieba_name="抗压背锅", dbConn=dbConn)
    #process.crawl('IpSpider', dbConn=dbConn)
    process.start()





    dbConn.commit()
    dbConn.close()

if __name__ == '__main__':
    main()
