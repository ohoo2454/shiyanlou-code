#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms


# 表单样式初始化基类
class BootstrapModelForm(forms.ModelForm):
    """
    表单样式初始化基类
    """

    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
