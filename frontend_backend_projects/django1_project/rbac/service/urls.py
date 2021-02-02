#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import reverse
from django.http import QueryDict


# 生成带有原搜索条件的url
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url（替代了模板中的url）
    :param request:
    :param name: url别名
    :param args: url位置参数
    :param kwargs: url关键字参数
    :return: url
    """
    basic_url = reverse(name, args=args, kwargs=kwargs)
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    if not request.GET:
        return basic_url
    url = '%s?%s' % (basic_url, query_dict.urlencode())
    return url


# 反向生成带有原搜索条件的url
def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成带有原搜索条件url
    http://127.0.0.1:8001/rbac/menu/add/?_filter=mid%3D2
        在url中将原来搜索条件，如filter后的值reverse生成原来的URL，
        如：/menu/list/ -> /menu/list/?mid%3D2
    :param request:
    :param name: url别名
    :param args: url位置参数
    :param kwargs: url关键字参数
    :return: url
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = '%s?%s' % (url, origin_params)
    return url
