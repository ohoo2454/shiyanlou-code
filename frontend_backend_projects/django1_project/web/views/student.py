#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.service.v1 import (StarkModelForm, StarkHandler, Option, 
                              get_choice_text, get_m2m_text)
from web.models import Student


# 学员表单
class StudentModelForm(StarkModelForm):
    """
    学员表单
    """

    class Meta:
        model = Student
        fields = ['qq', 'mobile', 'emergency_contract', 'memo']


# 学员相关视图函数处理类
class StudentHandler(StarkHandler):
    """
    学员相关视图函数处理类
    """

    # 页面显示积分记录
    def display_score_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        页面显示积分记录
        :param obj:
        :param is_header:
        :parma args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '积分管理'
        score_url = reverse('stark:web-scorerecord-list', 
                            kwargs={'student_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (
                         score_url, obj.score))
    
    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_display_list(self):
        value = []
        if self.display_list:
            value.extend(self.display_list)
            value.append(type(self).display_edit)
        return value

    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.list_view), 
                name=self.get_list_url_name), 
            # url(r'^add/$', self.wrapper(self.add_view), 
            #     name=self.get_add_url_name), 
            url(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), 
                name=self.get_edit_url_name), 
            # url(r'^del/(?P<pk>\d+)/$', self.wrapper(self.del_view), 
            #     name=self.get_del_url_name), 
        ]
        patterns.extend(self.extra_urls())
        return patterns

    display_list = ['customer', 'qq', 'mobile', 'emergency_contract', 
                    get_m2m_text('已报班级', 'class_list'),
                    display_score_record, 
                    get_choice_text('状态', 'student_status')]
    model_form_class = StudentModelForm
    search_list = ['customer__name', 'qq', 'mobile']
    search_group = [
        Option('class_list', 
               text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    ]
