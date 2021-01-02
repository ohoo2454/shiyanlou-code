#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import url

from stark.service.v1 import (StarkHandler, get_choice_text, 
        StarkModelForm, StarkForm, Option)
from web.models import UserInfo
from web.utils.md5 import gen_md5


# 添加员工表单类
class UserInfoAddModelForm(StarkModelForm):
    """
    添加员工表单类
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 
                'gender', 'phone', 'email', 'depart', 'roles']
    
    # 密码校验
    def clean_confirm_password(self):
        """
        密码校验
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码输入不一致！')
        return confirm_password

    # 密码加密
    def clean(self):
        """
        密码加密
        """
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


# 编辑员工信息表单类
class UserInfoChangeModelForm(StarkModelForm):
    """
    编辑员工信息表单类
    """

    class Meta:
        model = UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 
                'roles']


# 重置密码表单
class ResetPasswordForm(StarkForm):
    """
    重置密码表单
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', 
            widget=forms.PasswordInput)
    
    # 密码校验
    def clean_confirm_password(self):
        """
        密码校验
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码输入不一致')
        return confirm_password

    # 密码加密
    def clean(self):
        """
        密码加密
        """
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


# 员工视图函数处理类
class UserInfoHandler(StarkHandler):
    """
    员工视图函数处理类
    """
    
    # 页面显示重置密码按钮
    def display_reset_pwd(self, obj=None, is_header=None):
        """
        页面显示重置密码按钮
        :param obj: 记录对象
        :param is_header: 是否为表头
        :return:
        """
        if is_header:
            return '重置密码'
        reset_url = self.reverse_common_url(self.get_url_name('reset-pwd'), 
                pk=obj.pk)
        return mark_safe('<a href="%s">重置密码</a>' % reset_url)

    # 重置密码的视图函数
    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_obj = UserInfo.objects.filter(id=pk).first()
        if not userinfo_obj:
            return HttpResponse('用户不存在，无法重置密码！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/edit.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_obj.password = form.cleaned_data['password']
            userinfo_obj.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/edit.html', {'form': form})
    
    display_list = ['nickname', get_choice_text('性别', 'gender'), 'phone', 
            'email', 'depart', display_reset_pwd]
    search_list = ['nickname__contains', 'name__contains']
    search_group = [
        Option(field='gender'),
        Option(field='depart'),
    ]

    # 获取模型表单类
    def get_model_form_class(self, is_add=False):
        """
        获取模型表单类
        :param is_add: 是否添加新员工
        :return:
        """
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    # 额外的url
    def extra_urls(self):
        """
        额外的url
        """
        patterns = [
            url(r'^reset/password/(?P<pk>\d+)/$', 
                self.wrapper(self.reset_password), 
                name=self.get_url_name('reset-pwd')
            ),
        ]
        return patterns
