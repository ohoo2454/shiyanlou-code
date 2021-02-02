#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.v1 import (StarkHandler, StarkModelForm, get_m2m_text, 
                              get_choice_text)
from web.models import Customer


# 私户表单类
class PrivateCustomerModelForm(StarkModelForm):
    """
    私户表单类
    """
    
    class Meta:
        model = Customer
        exclude = ['consultant',]


# 私人用户相关视图函数处理类
class PrivateCustomerHandler(StarkHandler):
    """
    私人用户相关视图函数处理类
    """

    # 页面显示跟进记录
    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        页面显示跟进记录
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '跟进记录'
        record_url = reverse('stark:web-consultrecord-list', 
                             kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">查看跟进记录</a>' % \
                         record_url)

    # 页面显示缴费记录
    def display_pay_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        页面显示缴费记录
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '缴费记录'
        record_url = reverse('stark:web-paymentrecord-list', 
                             kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">查看缴费记录</a>' % \
                         record_url)

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            current_user_id = request.session['user_info']['id']
            form.instance.consultant_id = current_user_id
        form.save()

    # 批量移除到公户
    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量移除到公户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        Customer.objects.filter(id__in=pk_list, 
                                consultant_id=current_user_id
                                ).update(consultant=None)

    action_multi_remove.text = '移除到公户'

    display_list = [
        StarkHandler.display_checkbox, 
        'name', 'qq', 
        get_m2m_text('咨询课程', 'course'), 
        get_choice_text('状态', 'status'), 
        display_record, 
        display_pay_record, 
    ]
    model_form_class = PrivateCustomerModelForm
    action_list = [action_multi_remove,]
