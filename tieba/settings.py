# Scrapy settings for tieba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'tieba'
#USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/610.3.7 (KHTML, like Gecko) QHBrowser/314 QihooBrowser/4.0.9"
USER_AGENT = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0）'
#USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/610.3.7 (KHTML, like Gecko) QHBrowser/314 QihooBrowser/4.0.9"

SPIDER_MODULES = ['tieba.spiders']
NEWSPIDER_MODULE = 'tieba.spiders'

project_folder = os.path.abspath(os.path.dirname(__file__))

IMAGES_STORE = os.path.join(project_folder, 'images')



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "tieba (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "tieba.middlewares.TiebaSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #"tieba.middlewares.RandomHeaderMiddleware": 400,
    #"tieba.middlewares.TiebaDownloaderMiddleware": 400,
    #"scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    #"scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
   'tieba.middlewares.RandomProxyMiddleware': 200,
   "tieba.middlewares.TiebaDownloaderMiddleware": None
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scrapy.pipelines.images.ImagesPipeline": 200,
   "tieba.pipelines.TiebaPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 2
# DUPEFILTER_CLASS = 'tieba.middlewares.NoFilter'
