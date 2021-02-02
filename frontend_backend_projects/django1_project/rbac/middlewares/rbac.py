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
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('无权限信息，请重新登录！')
        url_record = [
            {'title': '首页', 'url': '#'},
        ]
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, current_url):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None
        flag = False
        for item in permission_dict.values():
            reg = '^{}$'.format(item['url'])
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 
                                       'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']}, 
                        {'title': item['title'], 'url': item['url'], 
                         'class': 'active'}, 
                    ])
                request.breadcrumb = url_record
                break
        if not flag:
            return HttpResponse('无访问权限！')
        