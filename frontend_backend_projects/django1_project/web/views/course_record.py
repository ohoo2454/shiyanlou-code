#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse, render
from django.forms.models import modelformset_factory
from django.urls import reverse

from stark.service.v1 import StarkHandler, StarkModelForm, get_datetime_text
from web.models import CourseRecord, ClassList, StudyRecord


# 上课记录表单类
class CourseRecordModelForm(StarkModelForm):
    """
    上课记录表单类
    """

    class Meta:
        model = CourseRecord
        fields = ['day_num', 'teacher']


# 考勤记录表单类
class StudyRecordModelForm(StarkModelForm):
    """
    考勤记录表单类
    """

    class Meta:
        model = StudyRecord
        fields = ['record', ]


# 上课记录相关视图函数处理类
class CourseRecordHandler(StarkHandler):
    """
    上课记录相关视图函数处理类
    """
    
    # 批量初始化考勤记录
    def action_multi_init(self, request, *args, **kwargs):
        """
        批量初始化考勤记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course_record_id_list = request.POST.getlist('pk')
        class_id = kwargs.get('class_id')
        class_object = ClassList.objects.filter(id=class_id).first()
        if not class_object:
            return HttpResponse('班级不存在')
        student_object_list = class_object.student_set.all()
        for course_record_id in course_record_id_list:
            # 判断上课记录是否合法
            course_record_object = CourseRecord.objects.filter(
                id=course_record_id, 
                class_object_id=class_id
            ).first()
            if not course_record_object:
                continue
            # 判断此上课记录对应的考勤记录是否存在
            study_record_exists = StudyRecord.objects.filter(
                    course_record=course_record_object).exists()
            if study_record_exists:
                continue
            # 为每个学员创建此上课记录对应的考勤记录
            study_record_object_list = [
                StudyRecord(student_id=stu.id, 
                course_record_id=course_record_id) 
                for stu in student_object_list
            ]
            StudyRecord.objects.bulk_create(study_record_object_list, 
                                            batch_size=50)
    
    action_multi_init.text = '批量初始化考勤记录'
    
    # 页面显示考勤
    def display_attendance(self, obj=None, is_header=None, *args, **kwargs):
        """
        页面显示考勤
        """
        if is_header:
            return '考勤'
        name = '%s:%s' % (self.site.namespace, self.get_url_name('attendance'))
        attendance_url = reverse(name, kwargs={'course_record_id': obj.pk})
        tpl = '<a target="_blank" href="%s">考勤</a>' % attendance_url
        return mark_safe(tpl)

    # 考勤记录管理视图函数
    def attendance_view(self, request, course_record_id, *args, **kwargs):
        """
        考勤记录管理视图函数
        :param request:
        :param course_record_id:
        :param args:
        :param kwargs:
        :return:
        """
        study_record_object_list = StudyRecord.objects.filter(
                course_record_id=course_record_id)
        study_model_formset = modelformset_factory(StudyRecord, extra=0, 
                                                   form=StudyRecordModelForm)
        if request.method == 'POST':
            formset = study_model_formset(queryset=study_record_object_list, 
                                          data=request.POST)
            if formset.is_valid():
                formset.save()
            return render(request, 'attendance.html', {'formset': formset})
        formset = study_model_formset(queryset=study_record_object_list)
        return render(request, 'attendance.html', {'formset': formset})
    
    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        class_id = kwargs.get('class_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(pk=obj.pk, class_id=class_id), 
            self.reverse_del_url(pk=obj.pk, class_id=class_id)
        )
        return mark_safe(tpl)

    def get_queryset(self, request, *args, **kwargs):
        class_id = kwargs.get('class_id')
        return self.model_class.objects.filter(class_object_id=class_id)

    def save(self, request, form, is_update, *args, **kwargs):
        class_id = kwargs.get('class_id')
        if not is_update:
            form.instance.class_object_id = class_id
        form.save()
    
    def get_urls(self):
        patterns = [
            url(r'^list/(?P<class_id>\d+)/$', self.wrapper(self.list_view), 
                name=self.get_list_url_name), 
            url(r'^add/(?P<class_id>\d+)/$', self.wrapper(self.add_view), 
                name=self.get_add_url_name), 
            url(r'^edit/(?P<class_id>\d+)/(?P<pk>\d+)/$', 
                self.wrapper(self.edit_view), name=self.get_edit_url_name), 
            url(r'^del/(?P<class_id>\d+)/(?P<pk>\d+)/$', 
                self.wrapper(self.del_view), name=self.get_del_url_name), 
            
            url(r'^attendance/(?P<course_record_id>\d+)/$', 
                self.wrapper(self.attendance_view), 
                name=self.get_url_name('attendance')), 
        ]
        patterns.extend(self.extra_urls())
        return patterns
    
    display_list = [StarkHandler.display_checkbox, 'class_object', 'day_num', 
                    'teacher', get_datetime_text('上课日期', 'date'), 
                    display_attendance, ]
    model_form_class = CourseRecordModelForm
    action_list = [action_multi_init, ]
