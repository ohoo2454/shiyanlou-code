#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from rbac.models import UserInfo


# 新增用户表单
class UserModelForm(forms.ModelForm):
    """
    新增用户表单
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        校验密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次输入密码不一致！')
        return confirm_password


# 用户信息更新表单
class UpdateUserModelForm(forms.ModelForm):
    """
    用户信息更新表单
    """
    
    class Meta:
        model = UserInfo
        fields = ['name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# 用户密码重置表单
class ResetPasswordUserModelForm(forms.ModelForm):
    """
    用户密码重置表单
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = UserInfo
        fields = ['password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        校验密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次输入密码不一致')
        return confirm_password
