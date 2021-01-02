#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms

from app01.models import Menu, Permission


# 批量添加权限表单
class MultiPermissionForm(forms.Form):
    """
    批量添加权限表单
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(MultiPermissionForm, self).__init__(*args, **kwargs)
        self.fields['menu_id'].choices += Menu.objects.values_list('id', 
                'title')
        self.fields['pid_id'].choices += Permission.objects.filter(
                pid__isnull=True).exclude(
                        menu__isnull=True).values_list('id', 'title')


# 批量编辑权限表单
class MultiUpdatePermissionForm(forms.Form):
    """
    批量编辑权限表单
    """
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(MultiUpdatePermissionForm, self).__init__(*args, **kwargs)
        self.fields['menu_id'].choices += Menu.objects.values_list('id', 
                'title')
        self.fields['pid_id'].choices += Permission.objects.filter(
                pid__isnull=True).exclude(
                        menu__isnull=True).values_list('id', 'title')
