from django.db import models


# Create your models here.
# 客户信息表
class Customer(models.Model):
    """
    客户信息表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    email = models.EmailField(verbose_name='邮箱')
    company = models.CharField(verbose_name='公司', max_length=32)

    def __str__(self):
        return self.name


# 付费记录
class Payment(models.Model):
    """
    付费记录
    """
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer')
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now_add=True)
