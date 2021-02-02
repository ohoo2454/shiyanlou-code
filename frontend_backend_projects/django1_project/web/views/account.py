#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

from web.models import UserInfo
from web.utils.md5 import gen_md5
from rbac.service.init_permission import init_permission


# 登录视图函数
def login(request):
    """
    登录视图函数
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = gen_md5(request.POST.get('pwd', ''))
    user = UserInfo.objects.filter(name=user, password=pwd).first()
    if not user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})
    request.session['user_info'] = {'id': user.id, 'nickname': user.nickname}
    init_permission(user, request)
    return redirect('index')


# 注销视图函数
def logout(request):
    """
    注销视图函数
    :param request:
    :return:
    """
    request.session.delete()
    return redirect('login')


# 网站首页
def index(request):
    """
    网站首页
    :param request:
    :return:
    """
    return render(request, 'index.html')
