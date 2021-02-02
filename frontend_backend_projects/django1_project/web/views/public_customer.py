#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from django.shortcuts import render, HttpResponse
from django.conf.urls import url
from django.db import transaction

from stark.service.v1 import (StarkHandler, get_m2m_text, get_choice_text, 
                              StarkModelForm)
from web.models import Customer, ConsultRecord


# 公共用户表单类
class PublicCustomerModelForm(StarkModelForm):
    """
    公共用户表单类
    """

    class Meta:
        model = Customer
        exclude = ['consultant',]


# 公共用户相关视图函数处理类
class PublicCustomerHandler(StarkHandler):
    """
    公共用户相关视图函数处理类
    """
    
    # 页面显示跟进记录
    def display_record(self, obj=None, is_header=None):
        """
        页面显示跟进记录
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '跟进记录'
        record_url = self.reverse_common_url(self.get_url_name('record_view'), 
                                             pk=obj.pk)
        return mark_safe('<a href="%s">查看跟进记录</a>' % record_url)
    
    # 跟进记录处理视图函数
    def record_view(self, request, pk):
        """
        跟进记录处理视图函数
        :param request:
        :param pk:
        :return:
        """
        record_list = ConsultRecord.objects.filter(customer_id=pk)
        return render(
            request, 
            'record_view.html', 
            {'record_list': record_list}
        )
    
    # 批量申请到私户
    def action_multi_apply(self, request, *args, **kwargs):
        """
        批量申请到私户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        private_customer_count = Customer.objects.filter(
                consultant_id=current_user_id, status=2).count()
        
        # 私户数量限制
        if (private_customer_count + len(pk_list)) > \
                Customer.MAX_PRIVATE_CUSTOMER_COUNT:
            res = '做人不要太贪心，私户中已有%s个客户，最多可申请%s' %s (
                private_customer_count, 
                Customer.MAX_PRIVATE_CUSTOMER_COUNT - private_customer_count
            )
            return HttpResponse(res)
        
        # 数据库中加锁
        flag = False
        # 事务
        with transaction.atomic():
            # 数据库中加锁
            origin_queryset = Customer.objects.filter(
                id__in=pk_list, 
                status=2, 
                consultant__isnull=True
            ).select_for_update()
            if len(origin_queryset) == len(pk_list):
                Customer.objects.filter(
                    id__in=pk_list, 
                    status=2, 
                    consultant__isnull=True
                ).update(consultant_id=current_user_id)
                flag = True
        if not flag:
            res = '手速太慢了，选中的客户已被其他人申请，请重新选择'
            return HttpResponse(res)
    action_multi_apply.text = '申请到我的私户'
    
    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=True)

    def extra_urls(self):
        patterns = [
            url(r'record/(?P<pk>\d+)/$', self.wrapper(self.record_view), 
                name=self.get_url_name('record_view')),
        ]
        return patterns

    display_list = [
        StarkHandler.display_checkbox, 'name', 'qq', 
        get_m2m_text('咨询课程', 'course'), 
        display_record, get_choice_text('状态', 'status')
    ]
    model_form_class = PublicCustomerModelForm
    action_list = [action_multi_apply,]
