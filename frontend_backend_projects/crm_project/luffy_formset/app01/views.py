from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.forms import formset_factory

from app01.forms import MultiPermissionForm, MultiUpdatePermissionForm
from app01.models import Menu, Permission


# Create your views here.
# 批量添加
def multi_add(request):
    """
    批量添加
    :param request:
    :return:
    """
    form_class = formset_factory(MultiPermissionForm, extra=2)
    if request.method == 'GET':
        formset = form_class()
        return render(request, 'multi-add.html', {'formset': formset})
    formset = form_class(data=request.POST)
    if formset.is_valid():
        flag = True
        post_row_list = formset.cleaned_data
        for i in range(0, formset.total_form_count()):
            row = post_row_list[i]
            if not row:
                continue
            try:
                obj = Permission(**row)
                obj.validate_unique()
                obj.save()
            except Exception as e:
                formset.errors[i].update(e)
                flag = False
        if flag:
            return HttpResponse('提交成功')
        else:
            return render(request, 'multi-add.html', {'formset': formset})
    return render(request, 'multi-add.html', {'formset': formset})


# 批量编辑
def multi_edit(request):
    """
    批量编辑
    :param request:
    :return:
    """
    form_class = formset_factory(MultiUpdatePermissionForm, extra=0)
    if request.method == 'GET':
        formset = form_class(initial=Permission.objects.all().values(
            'id', 'title', 'url', 'name', 'menu_id', 'pid_id'))
        return render(request, 'multi-edit.html', {'formset': formset})
    formset = form_class(data=request.POST)
    if formset.is_valid():
        flag = True
        post_row_list = formset.cleaned_data
        for i in range(0, formset.total_form_count()):
            row = post_row_list[i]
            if not row:
                continue
            permission_id = row.pop('id')
            try:
                permission_obj = Permission.objects.filter(
                        id=permission_id).first()
                for key, value in row.items():
                    setattr(permission_obj, key, value)
                permission_obj.validate_unique()
                permission_obj.save()
            except Exception as e:
                formset.errors[i].update(e)
                flag = False
        if flag:
            return HttpResponse('提交成功')
        else:
            return render(request, 'multi-edit.html', {'formset': formset})
    return render(request, 'multi-edit.html', {'formset': formset})
