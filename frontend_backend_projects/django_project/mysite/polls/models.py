import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(verbose_name='问题描述', max_length=200)
    pub_date = models.DateTimeField(verbose_name='发布日期')

    class Meta:
        verbose_name = '问题管理'
        verbose_name_plural = '问题管理'

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= \
               timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是否近期发布'


class Choice(models.Model):
    question = models.ForeignKey(verbose_name='问题', to='Question', 
                                 on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name='选择描述', max_length=200)
    votes = models.IntegerField(verbose_name='投票', default=0)

    class Meta:
        verbose_name = '选项管理'
        verbose_name_plural = '选项管理'
    
    def __str__(self):
        return self.choice_text
