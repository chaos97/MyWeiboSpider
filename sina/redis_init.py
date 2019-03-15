#!/usr/bin/env python
# encoding: utf-8
import redis
import sys
import os

sys.path.append(os.getcwd())
from sina.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT

r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT)

for key in r.scan_iter("weibo_spider*"):
    r.delete(key)

start_uids = [
            '3217179555',  # 回忆专用小马甲
            '5194257804',  # 王可可是个碧池
            '3030975747'  # 韩塞的马达加斯加
            'liuyifeiofficial'  # 刘亦菲
            'crazyhh'  #大锅只是喝醉
            'guosite'  # 郭斯特
]
for uid in start_uids:
    r.lpush('weibo_spider:start_urls', "https://weibo.cn/%s/info" % uid)

print('redis初始化完毕')
