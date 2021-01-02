#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf.urls import url

from stark.service.v1 import (site, StarkHandler, get_choice_text, 
        StarkModelForm, Option)
from app01.models import UserInfo, Depart, Deploy


# 部门相关视图函数处理类
class DepartHandler(StarkHandler):
    """
    部门相关视图函数处理类
    """
    display_list = [
        StarkHandler.display_checkbox, 
        'id', 'title', 
        StarkHandler.display_edit, 
        StarkHandler.display_del,
    ]
    has_add_btn = True
    order_list = ['id']
    search_list = ['title__contains']
    action_list = [StarkHandler.action_multi_delete,]

    # 额外增加url
    def extra_urls(self):
        """
        额外增加url
        :return: [url]
        """
        return [
            url(r'^detail/(\d+)/$', self.detail_view),
        ]

    # 详细信息页面
    def detail_view(self, request, pk):
        """
        详细信息页面
        :return:
        """
        return HttpResponse('详细信息')


# 添加额外的组合搜索可选项
class MyOption(Option):
    """
    添加额外的组合搜索可选项
    """

    def get_db_condition(self, request, *args, **kwargs):
        return {}


# 用户信息表单类
class UserInfoModelForm(StarkModelForm):
    """
    用户信息表单类
    """
    class Meta:
        model = UserInfo
        fields = ['name', 'gender', 'classes', 'age', 'email']


# 用户相关视图函数处理类
class UserInfoHandler(StarkHandler):
    """
    用户相关视图函数处理类
    """
    # 自定义页面显示列
    display_list = [
        StarkHandler.display_checkbox,
        'name',
        get_choice_text('性别', 'gender'),
        get_choice_text('班级', 'classes'),
        'age', 'email', 'depart',
        StarkHandler.display_edit,
        StarkHandler.display_del,
    ]
    # 自定义每页显示条目数量
    per_page_count = 10
    # 自定义页面是否显示添加按钮
    has_add_btn = True
    # 自定义页面表单模型
    # model_form_class = UserInfoModelForm
    # 自定义排序关键字列表
    order_list = ['id']
    # 自定义搜索关键词列表
    search_list = ['name__contains', 'email__contains']
    # 自定义页面可批量操作功能列表
    action_list = [StarkHandler.action_multi_delete,]
    # 自定义页面组合搜索可选项组合
    search_group = [
        Option('gender', is_multi=True),
        # MyOption('depart', {'id__gt': 2}),
        Option('depart', db_condition={'id__gt': 0}),
        # Option('gender', text_func=lambda field_obj: field_obj[1] + '666'),
    ]

    # 自定义页面表单保存
    # def save(self, form, is_update=False):
    #     form.instance.depart_id = 1
    #     form.save()

    # 获取应该显示的列
    # def get_display_list(self):
    #     """
    #     获取应该显示的列
    #     :return:
    #     """
    #     return ['name', 'age']
    
    # 修改url
    # def get_urls(self):
    #     """
    #     修改url
    #     :return:
    #     """
    #     patterns = [
    #         url(r'^list/$', self.list_view),
    #         url(r'^add/$', self.add_view),
    #     ]
    #     return patterns


# 用户在线状态处理类
class DeployHandler(StarkHandler):
    """
    用户在线状态处理类
    """
    display_list = [
        'title', 
        get_choice_text('状态', 'status'), 
        StarkHandler.display_edit, 
        StarkHandler.display_del, 
    ]


# 模型类和相关处理类注册
site.register(Depart, DepartHandler)
site.register(UserInfo, UserInfoHandler)
site.register(Deploy, DeployHandler)
