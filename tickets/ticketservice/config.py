# !/usr/bin/python  
# -*- coding:utf-8 -*-
# Author: Yao Tong
# Created Time: 2020-4-18
'''
BEGIN
function:
    config
END
'''
import os

REDIS_NAME = "nameko-redis"
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))


