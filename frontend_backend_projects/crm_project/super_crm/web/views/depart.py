#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stark.service.v1 import StarkHandler


# 部门视图函数处理类
class DepartmentHandler(StarkHandler):
    """
    部门视图函数处理类
    """
    display_list = ['title',]
    