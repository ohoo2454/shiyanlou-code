#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form

from web import models


# 客户表单
class CustomerForm(ModelForm):
    """
    客户表单
    """
    
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
