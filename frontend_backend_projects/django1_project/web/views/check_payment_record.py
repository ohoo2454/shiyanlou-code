#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from stark.service.v1 import StarkHandler, get_choice_text, get_datetime_text


# 缴费申请审批相关视图函数处理类
class CheckPaymentRecordHandler(StarkHandler):
    """
    缴费申请审批相关视图函数处理类
    """
    
    def get_display_list(self):
        value = []
        if self.display_list:
            value.extend(self.display_list)
        return value
    
    def get_add_btn(self, request, *args, **kwargs):
        return None
    
    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.list_view), 
                name=self.get_list_url_name), 
            # url(r'^add/$', self.wrapper(self.add_view), 
            #     name=self.get_add_url_name), 
            # url(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), 
            #     name=self.get_edit_url_name), 
            # url(r'^del/(?P<pk>\d+)/$', self.wrapper(self.del_view), 
            #     name=self.get_del_url_name), 
        ]
        patterns.extend(self.extra_urls())
        return patterns

    # 批量确认缴费申请
    def action_multi_confirm(self, request, *args, **kwargs):
        """
        批量确认缴费申请
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 确认缴费申请
        # 确认客户
        # 确认学员
        for pk in pk_list:
            payment_obj = self.model_class.objects.filter(
                    id=pk, confirm_status=1).first()
            if not payment_obj:
                continue
            payment_obj.confirm_status = 2
            payment_obj.save()

            payment_obj.customer.status = 1
            payment_obj.customer.save()
            
            payment_obj.customer.student.status = 2
            payment_obj.customer.student.save()

    action_multi_confirm.text = '批量确认'

    # 批量驳回缴费申请
    def action_multi_cancel(self, request, *args, **kwargs):
        """
        批量驳回缴费申请
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(
                id__in=pk_list, confirm_status=1).update(confirm_status=3)

    action_multi_cancel.text = '批量驳回'
    
    order_list = ['-id', 'confirm_status']
    display_list = [
        StarkHandler.display_checkbox, 'customer', 
        get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 'class_list', 
        get_datetime_text('申请日期', 'apply_date'), 
        get_choice_text('缴费状态', 'confirm_status'), 'consultant', 
    ]
    action_list = [action_multi_confirm, action_multi_cancel]
