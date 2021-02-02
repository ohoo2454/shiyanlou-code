#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.service.v1 import (StarkHandler, get_datetime_text, get_m2m_text, 
        StarkModelForm, Option)
from stark.forms.widgets import DateTimePickerInput
from web.models import ClassList


# 班级模型表单类
class ClassListModelForm(StarkModelForm):
    """
    班级模型表单类
    """
    
    class Meta:
        model = ClassList
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput,
        }


# 班级模型视图函数处理类
class ClassListHandler(StarkHandler):
    """
    班级模型视图函数处理类
    """
    
    # 页面显示课程信息
    def display_course(self, obj=None, is_header=None):
        """
        页面显示课程信息
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '班级'
        return '%s %s期' % (obj.course.name, obj.semester)

    # 页面显示上课记录
    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        页面显示上课记录
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        """
        if is_header:
            return '上课记录'
        record_url = reverse('stark:web-courserecord-list', 
                             kwargs={'class_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">查看上课记录</a>' % \
                         record_url)

    display_list = [
        'school', display_course, 'price', 
        get_datetime_text('开班日期', 'start_date'),
        'class_teacher',
        get_m2m_text('任课老师', 'tech_teachers'), 
        display_course_record, 
    ]
    model_form_class = ClassListModelForm
    search_group = [
        Option('school'), 
        Option('course'), 
    ]
    