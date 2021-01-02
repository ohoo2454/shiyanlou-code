from django.db import models


# Create your models here.
# 部门表
class Depart(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


# 用户信息表
class UserInfo(models.Model):
    """
    用户信息表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, 
            default=1)
    class_choices = (
        (11, '全栈1期'),
        (21, '全栈3期'),
    )
    classes = models.IntegerField(verbose_name='班级', choices=class_choices,
            default=11)
    age = models.IntegerField(verbose_name='年龄')
    email = models.EmailField(verbose_name='邮箱')
    depart = models.ForeignKey(verbose_name='部门', to='Depart')

    def __str__(self):
        return self.name
    

# 用户在线状态表单
class Deploy(models.Model):
    """
    用户在线状态表单
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    status_choices = (
        (1, '在线'), 
        (2, '离线'),
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choices)

    def __str__(self):
        return self.title
