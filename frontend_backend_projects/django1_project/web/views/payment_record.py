#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.conf.urls import url
from django.shortcuts import HttpResponse

from stark.service.v1 import StarkHandler, StarkModelForm, get_choice_text
from web.models import PaymentRecord, Student, Customer


# 缴费记录模型表单类
class PaymentRecordModelForm(StarkModelForm):
    """
    缴费记录模型表单类
    """

    class Meta:
        model = PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'note']


# 学员缴费记录模型表单类
class StudentPaymentRecordModelForm(StarkModelForm):
    """
    学员缴费记录模型表单类
    """
    qq = forms.CharField(label='QQ号', max_length=32)
    mobile = forms.CharField(label='手机号', max_length=32)
    emergency_contract = forms.CharField(label='紧急联系人手机号码', 
                                         max_length=32)

    class Meta:
        model = PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'qq', 'mobile', 
                  'emergency_contract', 'note']


# 缴费记录相关视图函数处理类
class PaymentRecordHandler(StarkHandler):
    """
    缴费记录相关视图函数处理类
    """
    display_list = [get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 
                    'consultant', 
                    get_choice_text('缴费状态', 'confirm_status')]

    def get_display_list(self):
        value = []
        if self.display_list:
            value.extend(self.display_list)
        return value

    def get_urls(self):
        patterns = [
            url(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), 
                name=self.get_list_url_name),
            url(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), 
                name=self.get_add_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns
    
    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, 
                customer__consultant_id=current_user_id)

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        # 如果当前客户有学员信息，则使用PaymentRecordModelForm；
        # 否则使用StudentPaymentRecordModelForm
        customer_id = kwargs.get('customer_id')
        student_exists = Student.objects.filter(
                customer_id=customer_id).exists()
        if student_exists:
            return PaymentRecordModelForm
        return StudentPaymentRecordModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        obj_exists = Customer.objects.filter(id=customer_id, 
                consultant_id=current_user_id).exists()
        if not obj_exists:
            return HttpResponse('非法操作')
        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_user_id
        # 创建缴费记录信息
        form.save()
        # 创建学员信息
        class_list = form.cleaned_data['class_list']
        fetch_student_obj = Student.objects.filter(
                customer_id=customer_id).first()
        if not fetch_student_obj:
            qq = form.cleaned_data['qq']
            mobile = form.cleaned_data['mobile']
            emergency_contract = form.cleaned_data['emergency_contract']
            student_obj = Student.objects.create(
                customer_id=customer_id, qq=qq, mobile=mobile, 
                emergency_contract=emergency_contract)
            student_obj.class_list.add(class_list.id)
        else:
            fetch_student_obj.class_list.add(class_list.id)
