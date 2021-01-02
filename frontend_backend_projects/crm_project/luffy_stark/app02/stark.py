#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.http import HttpResponse

from stark.service.v1 import site, StarkHandler
from app02.models import Host, Role, Project


# 主机相关视图函数处理类
class HostHandler(StarkHandler):
    """
    主机相关视图函数处理类
    """
    display_list = ['id', 'host', StarkHandler.display_edit]


site.register(Host, HostHandler)
site.register(Role)
site.register(Project)
# site.register(Project, prev='private')
