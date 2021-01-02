#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms


# 日期选择插件
class DateTimePickerInput(forms.TextInput):
    """
    日期选择插件
    """
    template_name = 'stark/forms/widgets/datetime_picker.html'
