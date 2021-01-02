#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render


# 用户信息
def info(request):
    """
    用户信息
    :param request:
    :return:
    """
    return render(request, 'info.html')
