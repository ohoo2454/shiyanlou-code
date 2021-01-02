#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from django import template
from django.conf import settings

from rbac.service import urls

register = template.Library()


# 动态生成一级菜单
@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    动态生成一级菜单
    :param request:
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


# 动态生成二级菜单
@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    动态生成二级菜单
    :param request:
    :return:
    """
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    key_list = sorted(menu_dict)
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            if per['id'] == request.current_permission_pid:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    return {'menu_dict': ordered_dict}


# 生成路径导航
@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    生成路径导航
    :param request:
    :return:
    """
    return {'breadcrumb_list': request.current_breadcrumb_list}


# 权限粒度控制到按钮级别
@register.filter
def has_permission(request, name):
    """
    自定义过滤器，将权限粒度控制到按钮级别
    :param request:
    :param name: 按钮名称
    :return:
    """
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True


# 生成带有原搜索条件的URL
@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name: url别名
    :param args: url位置参数
    :param kwargs: url关键字参数
    :return: url
    """
    return urls.memory_url(request, name, *args, **kwargs)
