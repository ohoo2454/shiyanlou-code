#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from rbac.models import UserInfo
from rbac.forms.user import (UserModelForm, UpdateUserModelForm, 
                             ResetPasswordUserModelForm)


# 获取用户列表
def user_list(request):
    """
    获取用户列表
    :param request:
    :return:
    """
    users = UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', {'users': users})


# 添加用户
def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 编辑用户
def user_edit(request, uid):
    """
    编辑用户
    :param request:
    :param uid: 用户id
    :return:
    """
    user = UserInfo.objects.filter(id=uid).first()
    if not user:
        return HttpResponse('数据不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=user)
        return render(request, 'rbac/change.html', {'form': form})
    form = UpdateUserModelForm(instance=user, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 删除用户
def user_del(request, uid):
    """
    删除用户
    :param request:
    :param uid: 用户id
    :return:
    """
    origin_url = reverse('rbac:user-list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    user = UserInfo.objects.filter(id=uid).delete()
    return redirect(origin_url)


# 重置用户密码
def user_reset_pwd(request, uid):
    """
    重置用户密码
    :param request:
    :param uid: 用户id
    :return:
    """
    user = UserInfo.objects.filter(id=uid).first()
    if not user:
        return HttpResponse('数据不存在')
    if request.method == 'GET':
        form = ResetPasswordUserModelForm(instance=user)
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetPasswordUserModelForm(instance=user, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user-list'))
    return render(request, 'rbac/change.html', {'form': form})
    