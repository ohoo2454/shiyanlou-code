#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms

from rbac.models import Role


# 角色表单
class RoleModelForm(forms.ModelForm):
    """
    角色表单
    """
    
    class Meta:
        model = Role
        fields = ['title',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
