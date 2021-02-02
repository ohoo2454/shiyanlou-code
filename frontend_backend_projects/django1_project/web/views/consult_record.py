#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse

from stark.service.v1 import StarkHandler, StarkModelForm
from web.models import ConsultRecord, Customer


# 跟进记录表单类
class ConsultRecordModelForm(StarkModelForm):
    """
    跟进记录表单类
    """

    class Meta:
        model = ConsultRecord
        fields = ['note', ]


# 私户跟进记录相关视图函数处理类
class ConsultRecordHandler(StarkHandler):
    """
    私户跟进记录相关视图函数处理类
    """
    list_template = 'consult_record.html'
    model_form_class = ConsultRecordModelForm
    display_list = ['note', 'consultant', 'date']
    
    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(pk=obj.pk, customer_id=customer_id), 
            self.reverse_del_url(pk=obj.pk, customer_id=customer_id)
        )
        return mark_safe(tpl)

    def get_urls(self):
        patterns = [
            url(r'^list/(?P<customer_id>\d+)/$', 
                self.wrapper(self.list_view), 
                name=self.get_list_url_name),
            url(r'^add/(?P<customer_id>\d+)/$', 
                self.wrapper(self.add_view), 
                name=self.get_add_url_name),
            url(r'^edit/(?P<customer_id>\d+)/(?P<pk>\d+)/$', 
                self.wrapper(self.edit_view), 
                name=self.get_edit_url_name),
            url(r'^del/(?P<customer_id>\d+)/(?P<pk>\d+)/$', 
                self.wrapper(self.del_view), 
                name=self.get_del_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, 
                customer__consultant_id=current_user_id)
    
    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        obj_exists = Customer.objects.filter(id=customer_id, 
                consultant_id=current_user_id).first()
        if not obj_exists:
            return HttpResponse('非法操作')
        if not is_update:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_user_id
        form.save()
    
    def get_edit_obj(self, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return ConsultRecord.objects.filter(id=pk, customer_id=customer_id, 
                customer__consultant_id=current_user_id).first()

    def del_obj(self, request, pk, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        record_queryset = ConsultRecord.objects.filter(
            id=pk, customer_id=customer_id, 
            customer__consultant_id=current_user_id
        )
        if not record_queryset.exists():
            return HttpResponse('要删除的数据不存在，请重新选择')
        record_queryset.delete()
