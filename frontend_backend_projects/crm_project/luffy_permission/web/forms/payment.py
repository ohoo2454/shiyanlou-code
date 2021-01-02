#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form

from web.models import Payment


# 所有客户付费记录表单
class PaymentForm(ModelForm):
    """
    所有客户付费记录表单
    """

    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['customer'].empty_label = '请选择客户'


# 已付费客户付费记录表单
class PaymentUserForm(ModelForm):
    """
    已付费客户付费记录表单
    """

    class Meta:
        model = Payment
        exclude = ['customer',]

    def __init__(self, *args, **kwargs):
        super(PaymentUserForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
