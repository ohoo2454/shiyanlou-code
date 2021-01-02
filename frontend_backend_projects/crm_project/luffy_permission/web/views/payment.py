#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse

from web.models import Payment
from web.forms.payment import PaymentForm, PaymentUserForm


# 付费记录列表
def payment_list(request):
    """
    付费记录列表
    :return:
    """
    data_list = Payment.objects.all()
    return render(request, 'payment_list.html', {'data_list': data_list})


# 新增付费记录
def payment_add(request):
    """
    新增付费记录
    :return:
    """
    if request.method == 'GET':
        form = PaymentForm()
        return render(request, 'payment_add.html', {'form': form})
    form = PaymentForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('payment-list'))
    return render(request, 'payment_add.html', {'form': form})


# 编辑付费记录
def payment_edit(request, pid):
    """
    编辑付费记录
    :return:
    """
    obj = Payment.objects.get(id=pid)
    if request.method == 'GET':
        form = PaymentForm(instance=obj)
        return render(request, 'payment_edit.html', {'form': form})
    form = PaymentForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse('payment-list'))
    return render(request, 'payment_edit.html', {'form': form})


# 删除付费记录
def payment_del(request, pid):
    """
    删除付费记录
    :return:
    """
    Payment.objects.filter(id=pid).delete()
    return redirect(reverse('payment-list'))
