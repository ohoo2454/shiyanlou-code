# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2021-01-04 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='理由')),
                ('score', models.IntegerField(help_text='违纪扣分写负值，表现优秀加分写正值', verbose_name='分值')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='score',
            field=models.IntegerField(default=100, verbose_name='积分'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='qq',
            field=models.CharField(help_text='QQ/微信/手机', max_length=64, unique=True, verbose_name='QQ'),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_list',
            field=models.ManyToManyField(blank=True, to='web.ClassList', verbose_name='已报班级'),
        ),
        migrations.AddField(
            model_name='scorerecord',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student', verbose_name='学员'),
        ),
        migrations.AddField(
            model_name='scorerecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='执行人'),
        ),
    ]