#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 远端接收数据的服务器
Params = {
    "server": "0.0.0.0",
    "port": 8080,
    'url': '/assets/report/',
    'request_timeout': 30,
}

# 日志文件配置
PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')

# 更多配置，请都集中在此文件中