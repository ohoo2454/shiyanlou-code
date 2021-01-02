#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from stark.service.v1 import (StarkHandler, get_m2m_text, get_choice_text, 
        StarkModelForm)
from web.models import Customer


# 公共用户表单类
class PublicCustomerModelForm(StarkModelForm):
    """
    公共用户表单类
    """

    class Meta:
        model = Customer
        exclude = ['consultant']


# 公共用户相关视图函数处理类
class PublicCustomerHandler(StarkHandler):
    """
    公共用户相关视图函数处理类
    """
    display_list = ['name', 'qq', get_m2m_text('咨询课程', 'course'), 
            get_choice_text('状态', 'status')]
    model_form_class = PublicCustomerModelForm
    
    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=True)
