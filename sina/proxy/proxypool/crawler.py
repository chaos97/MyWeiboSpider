import json
import re
from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies


    def crawl_xdaili(self):
        """
        获取讯代理
        :return:代理
        """
        url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=c6bb9241fba64d7f9a9bda9a1006a42b&orderno=YZ20193156474e5QgWb&returnType=2&count=20'
        html = get_page(url)
        if html:
            result = json.loads(html)
            proxies = result.get('RESULT')
            for proxy in proxies:
                yield proxy.get('ip') + ':' + proxy.get('port')

