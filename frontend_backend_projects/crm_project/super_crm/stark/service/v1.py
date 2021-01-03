#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
from types import FunctionType

from django.conf.urls import url
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms
from django.db.models import Q, ForeignKey, ManyToManyField

from stark.utils.pagination import Pagination


# Stark 组件定义choice列显示中文信息
def get_choice_text(title, field):
    """
    对于Stark组件中定义列时，choice如果想要显示中文信息，调用此方法即可。
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """
    
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = 'get_%s_display' % field
        return getattr(obj, method)()
    return inner


# Stark 组件定义日期字段显示格式
def get_datetime_text(title, field, time_format='%Y-%m-%d'):
    """
    Stark 组件定义日期字段显示格式
    :param title: 字段表头名称
    :parma field: 字段
    :param time_format: 日期显示格式
    :return:
    """
    
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        datetime_value = getattr(obj, field)
        return datetime_value.strftime(time_format)
    return inner


# Stark 组件显示m2m字段
def get_m2m_text(title, field):
    """
    Stark 组件显示m2m字段
    :param title:
    :param field:
    :return:
    """
    
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        queryset = getattr(obj, field).all()
        text_list = [str(row) for row in queryset]
        return ','.join(text_list)
    return inner


# 组合搜索按钮生成类
class SearchGroupRow(object):
    """
    组合搜索按钮生成类
    """

    def __init__(self, title, queryset_or_tuple, option, query_dict):
        """
        :param title: 组合搜索的列名称
        :param queryset_or_tuple: 组合搜索关联获取到的数据
        :param option: 配置
        """
        self.title = title
        self.queryset_or_tuple = queryset_or_tuple
        self.option = option
        self.query_dict = query_dict

    def __iter__(self):
        yield '<div class="whole">'
        yield self.title
        yield '</div>'
        yield '<div class="others">'
        total_query_dict = self.query_dict.copy()
        total_query_dict._mutable = True

        origin_value_list = self.query_dict.getlist(self.option.field)
        if not origin_value_list:
            yield '<a class="active" href="?%s">全部</a>' % (
                    total_query_dict.urlencode())
        else:
            total_query_dict.pop(self.option.field)
            yield '<a href="?%s">全部</a>' % total_query_dict.urlencode()
        for item in self.queryset_or_tuple:
            text = self.option.get_text(item)
            value = str(self.option.get_value(item))
            query_dict = self.query_dict.copy()
            query_dict._mutable = True
            if not self.option.is_multi:
                query_dict[self.option.field] = value
                if value in origin_value_list:
                    query_dict.pop(self.option.field)
                    yield '<a class="active" href="?%s">%s</a>' % (
                            query_dict.urlencode(), text)
                else:
                    yield '<a href="?%s">%s</a>' % (
                            query_dict.urlencode(), text)
            else:
                multi_value_list = query_dict.getlist(self.option.field)
                if value in multi_value_list:
                    multi_value_list.remove(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield '<a class="active" href="?%s">%s</a>' % (
                            query_dict.urlencode(), text)
                else:
                    multi_value_list.append(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield '<a href="?%s">%s</a>' % (
                            query_dict.urlencode(), text)
        yield '</div>'


# 组合搜索可选项类
class Option(object):
    """
    组合搜索可选项类
    """

    def __init__(self, field, is_multi=False, db_condition=None, text_func=None, 
            value_func=None):
        """
        :param field: 组合搜索关联的字段
        :param is_multi: 可选项是否支持多选
        :param db_condition: 数据库关联查询时的条件
        :param text_func: 此函数用于显示组合搜索按钮页面文本
        """
        self.field = field
        self.is_multi = is_multi
        if not db_condition:
            db_condition = {}
        self.db_condition = db_condition
        self.text_func = text_func
        self.value_func = value_func
        self.is_choice = False

    # 获取数据库关联查询时的条件
    def get_db_condition(self, request, *args, **kwargs):
        """
        获取数据库关联查询时的条件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.db_condition

    # 根据字段获取数据库关联的字段
    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        根据字段获取数据库关联的字段
        :model_class:
        :request:
        :args:
        :kwargs:
        :return:
        """
        # 根据gender或depart字符串，去自己对应的Model类中找到 字段对象
        field_obj = model_class._meta.get_field(self.field)
        title = field_obj.verbose_name
        # 获取关联数据
        if isinstance(field_obj, ForeignKey) or \
                isinstance(field_obj, ManyToManyField):
            # FK 或 M2M，获取其关联表中的数据：Queryset
            db_condition = self.get_db_condition(request, *args, **kwargs)
            # print(self.field, 
            #         field_obj.rel.model.objects.filter(**db_condition))
            return SearchGroupRow(title, 
                    field_obj.rel.model.objects.filter(**db_condition), 
                    self, request.GET)
        else:
            # 获取choices中的数据：元组
            # print(self.field, field_obj.choices)
            self.is_choice = True
            return SearchGroupRow(title, field_obj.choices, self, request.GET)

    # 获取快速筛选按钮文本
    def get_text(self, field_obj):
        """
        获取快速筛选按钮文本
        :param field_obj:
        :return:
        """
        if self.text_func:
            return self.text_func(field_obj)
        if self.is_choice:
            return field_obj[1]
        return str(field_obj)

    # 获取快速筛选按钮对应值
    def get_value(self, field_obj):
        """
        获取快速筛选按钮对应值
        :param field_obj:
        :return:
        """
        if self.value_func:
            return self.value_func(field_obj)
        if self.is_choice:
            return field_obj[0]
        return field_obj.pk


# ModelForm表单格式化基类
class StarkModelForm(forms.ModelForm):
    """
    Modelform表单格式化基类
    """
    
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# 重置密码表单格式化基类
class StarkForm(forms.Form):
    """
    重置密码表单格式化基类
    """

    def __init__(self, *args, **kwargs):
        super(StarkForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# 视图函数处理基类
class StarkHandler(object):
    """
    视图函数处理基类
    """
    display_list = []          # 自定义页面显示列
    per_page_count = 10        # 每页显示条目数量
    has_add_btn = True         # 页面是否显示添加按钮
    model_form_class = None    # 页面表单模型
    order_list = []            # 排序关键字列表
    search_list = []           # 搜索关键词列表
    action_list = []           # 可批量操作功能列表
    search_group = []          # 组合搜索关键词列表
    list_template = None       # 列表视图对应HTML模板
    add_template = None        # 添加视图对应HTML模板
    edit_template = None       # 编辑视图对应HTML模板
    del_template = None        # 删除视图对应HTML模板

    def __init__(self, site, model_class, prev):
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None

    # 获取页面上应该显示的列
    def get_display_list(self):
        """
        获取页面上应该显示的列
        预留的自定义扩展，例如：以后根据用户的不同显示不同的列
        :return: []
        """
        value = []
        value.extend(self.display_list)
        value.append(type(self).display_edit_del)
        return value
    
    # 生成添加按钮
    def get_add_btn(self, request, *args, **kwargs):
        """
        生成添加按钮
        :return:
        """
        if self.has_add_btn:
            return '<a class="btn btn-primary" href="%s">添加</a>' % \
                    self.reverse_add_url(*args, **kwargs)
        return None

    # 获取页面表单模型
    def get_model_form_class(self, is_add=False):
        """
        获取页面表单模型
        :return:
        """
        if self.model_form_class:
            return self.model_form_class
        
        # 动态生成表单类
        class DynamicModelForm(StarkModelForm):
            """
            动态生成表单类
            """

            class Meta:
                model = self.model_class
                fields = '__all__'

        return DynamicModelForm

    # 获取排序关键字列表
    def get_order_list(self):
        """
        获取排序关键字列表
        :return:
        """
        return self.order_list or ['-id',]

    # 获取搜索关键词列表
    def get_search_list(self):
        """
        获取搜索关键词列表
        :return:
        """
        return self.search_list

    # 获取可批量操作功能列表
    def get_action_list(self):
        """
        获取可批量操作功能列表
        :return:
        """
        return self.action_list
    
    # 获取组合搜索关键词列表
    def get_search_group(self):
        """
        获取组合搜索关键词列表
        :return:
        """
        return self.search_group

    # 获取组合搜索条件
    def get_search_group_condition(self, request):
        """
        获取组合搜索条件
        :return:
        """
        condition = {}
        search_group = self.get_search_group()
        for option in search_group:
            values_list = request.GET.getlist(option.field)
            if not values_list:
                continue
            condition['%s__in' % option.field] = values_list
        return condition

    # 获取所有记录对象
    def get_queryset(self, request, *args, **kwargs):
        """
        获取所有记录对象
        :param request:
        :param args:
        :param kwargs:
        :return: queryset
        """
        return self.model_class.objects

    # 批量删除
    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除
        如果想要定制执行成功后的返回值，那么就为action函数设置返回值即可
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    action_multi_delete.text = '批量删除'

    # 页面显示多选框
    def display_checkbox(self, obj=None, is_header=None):
        """
        页面显示多选框
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' % \
                obj.pk)
    
    # 页面显示编辑图标
    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义页面显示的编辑列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '编辑'
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_edit_url(
                pk=obj.pk))
    
    # 页面显示删除图标
    def display_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义页面显示的删除列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>' % self.reverse_del_url(
                pk=obj.pk))

    # 页面显示编辑和删除图标
    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义页面显示的删除列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '操作'
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(pk=obj.pk), self.reverse_del_url(pk=obj.pk)
        )
        return mark_safe(tpl)
    
    # 列表页面
    def list_view(self, request, *args, **kwargs):
        """
        列表页面
        :param request:
        :return:
        """
        # 处理批量操作
        action_list = self.get_action_list()
        action_dict = {func.__name__: func.text for func in action_list}
        # {'multi_delete':'批量删除','multi_init':'批量初始化'}
        if request.method == 'POST':
            action_func_name = request.POST.get('action')
            if action_func_name and action_func_name in action_dict:
                action_response = getattr(self, action_func_name)(request, 
                        *args, **kwargs)
                if action_response:
                    return action_response

        # 获取搜索关键词列表
        search_list = self.get_search_list()
        search_value = request.GET.get('q', '')
        conn = Q()
        conn.connector = 'OR'
        if search_value:
            for item in search_list:
                conn.children.append((item, search_value))

        # 获取排序结果
        order_list = self.get_order_list()
        # 获取组合搜索条件
        search_group_condition = self.get_search_group_condition(request)
        prev_queryset = self.get_queryset(request, *args, **kwargs)
        queryset = prev_queryset.filter(conn).filter(
                **search_group_condition).order_by(*order_list)

        # 处理分页
        all_count = queryset.count()
        query_params = request.GET.copy()
        query_params._mutable = True
        pager = Pagination(
            current_page=request.GET.get('page'),
            base_url=request.path_info,
            all_count=all_count,
            query_params=query_params,
            per_page=self.per_page_count,
        )
        data_list = queryset[pager.start:pager.end]
        
        # 处理表格的表头
        display_list = self.get_display_list()
        header_list = []
        if display_list:
            for key_or_func in display_list:
                if isinstance(key_or_func, FunctionType):
                    verbose_name = key_or_func(self, obj=None, is_header=True, 
                            *args, **kwargs)
                else:
                    tmp_field = self.model_class._meta.get_field(key_or_func)
                    verbose_name = tmp_field.verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)
        
        # 处理表格的内容
        body_list = []
        for row in data_list:
            tr_list = []
            if display_list:
                for key_or_func in display_list:
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, False, 
                                *args, **kwargs))
                    else:
                        tr_list.append(getattr(row, key_or_func))
            else:
                tr_list.append(row)
            body_list.append(tr_list)

        # 生成添加按钮
        add_btn = self.get_add_btn(request, *args, **kwargs)

        # 处理组合搜索
        search_group_row_list = []
        search_group = self.get_search_group()  # ['depart', 'gender']
        for option_obj in search_group:
            row = option_obj.get_queryset_or_tuple(self.model_class, request, 
                    *args, **kwargs)
            search_group_row_list.append(row)

        return render(
            request, 
            self.list_template or 'stark/list.html', 
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn,
                'search_list': search_list,
                'search_value': search_value,
                'action_dict': action_dict,
                'search_group_row_list': search_group_row_list,
            }
        )

    # 在使用ModelForm保存数据之前预留的钩子方法
    def save(self, request, form, is_update, *args, **kwargs):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param form: 表单
        :param is_update: 是否更新
        :args:
        :kwargs:
        :return:
        """
        form.save()

    # 添加数据页面
    def add_view(self, request, *args, **kwargs):
        """
        添加数据页面
        :param request:
        :return:
        """
        model_form_class = self.get_model_form_class(is_add=True)
        if request.method == 'GET':
            form = model_form_class()
            return render(request, self.add_template or 'stark/edit.html', 
                    {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            response = self.save(request, form, False, *args, **kwargs)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.add_template or 'stark/edit.html', 
                {'form': form})

    # 获取要编辑的对象
    def get_edit_obj(self, request, pk, *args, **kwargs):
        """
        获取要编辑的对象
        :param request:
        :param pk:
        :parma args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects.filter(id=pk).first()
    
    # 编辑数据页面
    def edit_view(self, request, pk, *args, **kwargs):
        """
        编辑数据页面
        :param request:
        :param pk: 需要编辑数据的id
        :return:
        """
        current_edit_obj = self.get_edit_obj(request, pk, *args, **kwargs)
        if not current_edit_obj:
            return HttpResponse('要编辑的数据不存在')
        model_form_class = self.get_model_form_class(is_add=False)
        if request.method == 'GET':
            form = model_form_class(instance=current_edit_obj)
            return render(request, self.edit_template or 'stark/edit.html', 
                    {'form': form})
        form = model_form_class(instance=current_edit_obj, data=request.POST)
        if form.is_valid():
            response = self.save(request, form, True, *args, **kwargs)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.edit_template or 'stark/edit.html', 
                {'form': form})

    # 删除对象
    def del_obj(self, request, pk, *args, **kwargs):
        """
        删除对象
        :param request:
        :param pk:
        :parma args:
        :param kwargs:
        :return:
        """
        self.model_class.objects.filter(id=pk).delete()
    
    # 删除数据页面
    def del_view(self, request, pk, *args, **kwargs):
        """
        删除数据页面
        :param request:
        :param pk: 需要删除数据的id
        :return:
        """
        origin_list_url = self.reverse_list_url(*args, **kwargs)
        if request.method == 'GET':
            return render(request, self.del_template or 'stark/delete.html', 
                    {'cancel': origin_list_url})
        response = self.del_obj(request, pk, *args, **kwargs)
        return response or redirect(origin_list_url)

    # 动态生成url别名
    def get_url_name(self, param):
        """
        动态生成url别名
        :param param: url类型
        :return: url别名
        """
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        if self.prev:
            return '%s-%s-%s-%s' % (app_label, model_name, self.prev, param)
        return '%s-%s-%s' % (app_label, model_name, param)

    # 动态生成列表页面url别名
    @property
    def get_list_url_name(self):
        """
        动态生成列表页面url别名
        """
        return self.get_url_name('list')

    # 动态生成添加页面url别名
    @property
    def get_add_url_name(self):
        """
        动态生成添加页面url别名
        """
        return self.get_url_name('add')

    # 动态生成编辑页面url别名
    @property
    def get_edit_url_name(self):
        """
        动态生成编辑页面url别名
        """
        return self.get_url_name('edit')

    # 动态生成删除页面url别名
    @property
    def get_del_url_name(self):
        """
        动态生成删除页面url别名
        """
        return self.get_url_name('del')

    # 反向解析生成带有原搜索条件的url
    def reverse_common_url(self, name, *args, **kwargs):
        """
        反向解析生成带有原搜索条件的url
        :param name: url别名
        :param args: url位置参数
        :param kwargs: url关键字参数
        :return:
        """
        name = '%s:%s' % (self.site.namespace, name,)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            common_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_querydict = QueryDict(mutable=True)
            new_querydict['_filter'] = param
            common_url = '%s?%s' % (base_url, new_querydict.urlencode())
        return common_url

    # 反向解析生成带有原搜索条件列表页面url
    def reverse_list_url(self, *args, **kwargs):
        """
        反向解析生成带有原搜索条件列表页面url
        """
        name = '%s:%s' % (self.site.namespace, self.get_list_url_name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return '%s?%s' % (base_url, param)

    # 反向解析生成带有原搜索条件添加页面url
    def reverse_add_url(self, *args, **kwargs):
        """
        反向解析生成带有原搜索条件添加页面url
        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_add_url_name, *args, **kwargs)

    # 反向解析生成带有原搜索条件编辑页面url
    def reverse_edit_url(self, *args, **kwargs):
        """
        反向解析生成带有原搜索条件编辑页面url
        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_edit_url_name, *args, **kwargs)

    # 反向解析生成带有原搜索条件删除页面url
    def reverse_del_url(self, *args, **kwargs):
        """
        反向解析生成带有原搜索条件删除页面url
        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_del_url_name, *args, **kwargs)

    # 包装函数，为self.request赋值
    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)
        return inner
    
    # 动态生成app的url
    def get_urls(self):
        """
        动态生成app的url
        :return: patterns
        """
        patterns = [
            url(r'^list/$', self.wrapper(self.list_view), 
                    name=self.get_list_url_name),
            url(r'^add/$', self.wrapper(self.add_view), 
                    name=self.get_add_url_name),
            url(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), 
                    name=self.get_edit_url_name),
            url(r'^del/(?P<pk>\d+)/$', self.wrapper(self.del_view), 
                    name=self.get_del_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    # 预留增加额外url接口
    def extra_urls(self):
        """
        预留增加额外url接口
        :return:
        """
        return []


# stark组件类
class StarkSite(object):
    """
    stark组件类
    """

    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    # 模型类和视图函数处理类注册
    def register(self, model_class, handler_class=None, prev=None):
        """
        模型类和视图函数处理类注册
        :param model_class: models里的模型类
        :param handler_class: 处理请求的视图函数所在的类
        :param prev: 生成url的前缀
        :return:
        """
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append({
            'model_class': model_class, 
            'handler': handler_class(self, model_class, prev),
            'prev': prev
        })
        """
        self._registry = [
            {'prev':None, 'model_class':models.Depart,'handler': DepartHandler(models.Depart,prev)对象中有一个model_class=models.Depart   },
            {'prev':'private', 'model_class':models.UserInfo,'handler':  StarkHandler(models.UserInfo,prev)对象中有一个model_class=models.UserInfo   }
            {'prev':None, 'model_class':models.Host,'handler':  HostHandler(models.Host,prev)对象中有一个model_class=models.Host   }
        ]
        """
    
    # 动态进行url分发
    def get_urls(self):
        """
        动态进行url分发
        :return: patterns
        """
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            if prev:
                patterns.append(url(r'^%s/%s/%s/' % (app_label, model_name, 
                        prev), (handler.get_urls(), None, None)))
            else:
                patterns.append(url(r'^%s/%s/' % (app_label, model_name),
                        (handler.get_urls(), None, None)))
        return patterns

    # 获取生成的url
    @property
    def urls(self):
        """
        获取生成的url
        :return:
        """
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
