#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse

from rbac.models import UserInfo
from rbac.service.init_permission import init_permission


# 登录
def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    name = request.POST.get('username')
    pwd = request.POST.get('password')
    current_user = UserInfo.objects.filter(name=name, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})
    init_permission(current_user, request)
    return redirect(reverse('customer-list'))


# 注销
def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()
    return redirect(reverse('login'))
