#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf import settings


# 初始化用户访问权限
def init_permission(current_user, request):
    """
    根据当前用户信息获取此用户所拥有的所有权限，并放入 session
    获取菜单信息并放入 session
    :param current_user: 当前用户
    :param request: 所有请求相关数据
    :return:
    """
    permission_list = current_user.roles.filter(
        permissions__id__isnull=False).values('permissions__id', 
                                              'permissions__title', 
                                              'permissions__url',
                                              'permissions__name',
                                              'permissions__pid_id',
                                              'permissions__pid__name',
                                              'permissions__pid__url',
                                              'permissions__menu_id',
                                              'permissions__menu__title',
                                              'permissions__menu__icon',
                                              ).distinct()
    permission_dict = {}
    menu_dict = {}
    for item in permission_list:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'pid_url': item['permissions__pid__url'],
            'pid_name': item['permissions__pid__name'],
        }
        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        node = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
        }
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node],
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
