#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

from django.utils.module_loading import import_string
from django.conf import settings
from django.urls import RegexURLResolver, RegexURLPattern


# 排除一些特定的url
def check_url_excluce(url):
    """
    排除一些特定的url
    :param url: 需要检测的url
    :return: bool
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


# 递归获取url
def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取url
    :param pre_namespace: 名称前缀，用于拼接name
    :param pre_url: url前缀，用于拼接url
    :param urlpatterns: url模式列表
    :param url_ordered_dict: 保存递归获取的所有路由
    :return:
    """
    for item in urlpatterns:
        # 非路由分发，将路由添加到 url_ordered_dict
        if isinstance(item, RegexURLPattern):
            if not item.name:
                continue
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + item._regex
            url = url.replace('^', '').replace('$', '')
            if check_url_excluce(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        # 路由分发，递归操作
        elif isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.regex.pattern, 
                           item.url_patterns, url_ordered_dict)


# 获取项目中所有的URL（必须有name别名）
def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return: dict 项目中所有的URL
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)
    return url_ordered_dict
