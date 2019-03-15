# encoding: utf-8
import random
import json
import logging
from scrapy import signals
import requests
import pymongo
from sina.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, DB_NAME


class CookieMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']

    def process_request(self, request, spider):
        all_count = self.account_collection.find({'status': 'success'}).count()
        if all_count == 0:
            raise Exception('当前账号池为空')
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({'status': 'success'})[random_index]
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account
        spider.logger.error('使用cookie,账号:{}'.format(random_account['_id']))


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                request.meta['proxy'] = uri
                spider.logger.error('使用ip代理 ' + proxy)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class RedirectMiddleware(object):
    """
    检测账号是否正常
    302 / 403,说明账号cookie失效/账号被封，状态标记为error
    418,偶尔产生,需要再次请求
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']

    def process_response(self, request, response, spider):
        request.meta['retry_times'] = 0
        http_code = response.status
        if http_code == 302 or http_code == 403:
            self.account_collection.find_one_and_update({'_id': request.meta['account']['_id']},
                                                        {'$set': {'status': 'error'}}, )
            spider.logger.error('cookie被封了!!!正在更换cookie重试...')
            return request
        elif http_code == 418:
            request.meta['retry_times'] += 1
            spider.logger.error('[418]ip 被封了!!!请更换ip,或者停止程序...')
            return request
        elif http_code == 414:
            request.meta['retry_times'] += 1
            spider.logger.error('[414]ip 被封了!!!请更换ip,或者停止程序...')
            return request
        elif http_code in [401, 408, 500, 502, 503, 504]:
            request.meta['retry_times'] += 1
            spider.logger.error('[{}]http状态码异常!!!正在重试...'.format(http_code))
            return request
        else:
            return response
