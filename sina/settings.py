# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'OUTFOX_SEARCH_USER_ID_NCOO=1780588551.4011402; browser=d2VpYm9mYXhpYW4%3D; SCF=AsJyCasIxgS59OhHHUWjr9OAw83N3BrFKTpCLz2myUf2_vdK1UFy6Hucn5KaD7mXIoq8G25IMnTUPRRfr3U8ryQ.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFGJINkqaLbAcTzz2isXDTA5JpX5KMhUgL.Foq0e0571hBp1hn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMpe0ec1h5feKMR; SUB=_2A252a4N_DeRhGeBI61EV9CzPyD-IHXVVly03rDV6PUJbkdAKLRakkW1NRqYKs18Yrsf_SKnpgehmxRFUVgzXtwQO; SUHB=0U15b0sZ4CX6O4; _T_WM=0653fb2596917b052152f773a5976ff4; _WEIBO_UID=6603442333; SSOLoginState=1536482073; ALF=1539074073'
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'
