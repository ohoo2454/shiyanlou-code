from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(verbose_name='用户名', max_length=128, 
                            unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    gender_choices = (
        (1, '男'), 
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, 
                                 default=1)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    c_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    has_confirmed = models.BooleanField(verbose_name='确认状态', default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(verbose_name='确认码', max_length=256)
    user = models.OneToOneField(verbose_name='用户', to='User', 
                                on_delete=models.CASCADE)
    c_time = models.DateTimeField(verbose_name='确认时间', auto_now_add=True)

    def __str__(self):
        return self.user.name + ': ' + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
