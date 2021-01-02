#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from stark.service.v1 import StarkHandler


# 私人用户相关视图函数处理类
class PrivateCustomerHandler(StarkHandler):
    """
    私人用户相关视图函数处理类
    """
    list_display = ['name']
