#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stark.service.v1 import StarkHandler


# 课程视图函数处理类
class CourseHandler(StarkHandler):
    """
    课程视图函数处理类
    """
    display_list = ['name',]
    