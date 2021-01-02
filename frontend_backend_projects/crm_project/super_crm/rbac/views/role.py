#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from rbac.models import Role
from rbac.forms.role import RoleModelForm


# 获取角色列表
def role_list(request):
    """
    获取角色列表
    :param request:
    :return:
    """
    role_queryset = Role.objects.all()
    return render(request, 'rbac/role_list.html', {'role_list': role_queryset})


# 添加角色
def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 编辑角色
def role_edit(request, rid):
    """
    编辑角色
    :param request:
    :param rid: 角色id
    :return:
    """
    role_obj = Role.objects.filter(pk=rid).first()
    if not role_obj:
        return HttpResponse('数据不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=role_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(instance=role_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 删除角色
def role_del(request, rid):
    """
    删除角色
    :param request:
    :param rid: 角色id
    :return:
    """
    origin_url = reverse('rbac:role-list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    Role.objects.filter(id=rid).delete()
    return redirect(origin_url)
