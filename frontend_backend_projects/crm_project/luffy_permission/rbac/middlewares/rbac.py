#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings

# 重写中间件基类
class MiddlewareMixin(object):
    """
    重写中间件基类
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


# 用户权限信息匹配
class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息匹配
    """

    # 用户请求开始时进行权限校验
    def process_request(self, request):
        """
        1. 获取当前用户请求的 url
        2. 获取保存在 session 中当前用户的权限列表
        3. 进行权限匹配
        :return:
        """
        # 如果请求 url 在白名单中，则放行
        for reg in settings.PERMISSION_VALID_URL:
            if re.match(reg, request.path_info):
                return None
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('无权限信息，请重新登录！')
        flag = False
        request.current_breadcrumb_list = [
            {'title': '首页', 'url': '#'},
        ]
        for name, item in permission_dict.items():
            reg = '^{}$'.format(item['url'])
            if re.match(reg, request.path_info):
                flag = True
                pid = item['pid']
                pid_name = item['pid_name']
                pid_url = item['pid_url']
                if pid:
                    request.current_permission_pid = item['pid']
                    request.current_breadcrumb_list.extend([
                        {
                            'title': permission_dict[pid_name]['title'], 
                            'url': pid_url,
                        },
                        {
                            'title': item['title'], 
                            'url': item['url'], 
                            'class': 'active'
                        },
                    ])
                else:
                    request.current_permission_pid = item['id']
                    request.current_breadcrumb_list.append(
                        {
                            'title': item['title'],
                            'url': item['url'],
                            'class': 'active',
                        }
                    )
                break
        if not flag:
            return HttpResponse('无访问权限！')
        