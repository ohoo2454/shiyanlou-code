#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from stark.service.v1 import StarkHandler, StarkModelForm
from web.models import ScoreRecord


# 积分记录表单类
class ScoreRecordModelForm(StarkModelForm):
    """
    积分记录表单类
    """
    
    class Meta:
        model = ScoreRecord
        fields = ['content', 'score']


# 积分记录相关视图函数处理类
class ScoreRecordHandler(StarkHandler):
    """
    积分记录相关视图函数处理类
    """

    def get_display_list(self):
        value = []
        if self.display_list:
            value.extend(self.display_list)
        return value

    def get_queryset(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        return self.model_class.objects.filter(student_id=student_id)

    def save(self, request, form, is_update, *args, **kwargs):
        student_id = kwargs.get('student_id')
        current_user_id = request.session['user_info']['id']
        form.instance.student_id = student_id
        form.instance.user_id = current_user_id
        form.save()
        score = form.instance.score
        if score > 0:
            form.instance.student.score += abs(score)
        else:
            form.instance.student.score -= abs(score)
        form.instance.student.save()

    def get_urls(self):
        patterns = [
            url(r'^list/(?P<student_id>\d+)/$', self.wrapper(self.list_view), 
                name=self.get_list_url_name), 
            url(r'^add/(?P<student_id>\d+)/$', self.wrapper(self.add_view), 
                name=self.get_add_url_name), 
        ]
        patterns.extend(self.extra_urls())
        return patterns

    display_list = ['content', 'score', 'user']
    model_form_class = ScoreRecordModelForm
