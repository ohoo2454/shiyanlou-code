# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-12-18 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, help_text='是菜单才设置图标', max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AddField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=False, verbose_name='是否是菜单'),
        ),
    ]
