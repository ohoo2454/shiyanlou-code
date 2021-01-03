# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2021-01-02 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('icon', models.CharField(max_length=32, verbose_name='图标')),
            ],
            options={
                'verbose_name_plural': '菜单管理',
                'verbose_name': '菜单管理',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限名称')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='URL别名')),
                ('menu', models.ForeignKey(blank=True, help_text='null 表示非菜单', null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单')),
                ('pid', models.ForeignKey(blank=True, help_text='对于无法作为菜单的URL，可以为其选择一个可以作为菜单            的权限，那么访问时，则默认选中此权限', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ps', to='rbac.Permission', verbose_name='关联的权限')),
            ],
            options={
                'verbose_name_plural': '权限管理',
                'verbose_name': '权限管理',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='身份名称')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='拥有的所有权限')),
            ],
            options={
                'verbose_name_plural': '身份管理',
                'verbose_name': '身份管理',
            },
        ),
    ]
