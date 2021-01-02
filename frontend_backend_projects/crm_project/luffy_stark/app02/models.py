from django.db import models


# Create your models here.
# 主机表
class Host(models.Model):
    """
    主机表
    """
    host = models.CharField(verbose_name='主机名称', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP')

    def __str__(self):
        return self.host


# 身份表
class Role(models.Model):
    """
    身份表
    """
    title = models.CharField(verbose_name='身份名称', max_length=32)

    def __str__(self):
        return self.title


# 项目表
class Project(models.Model):
    """
    项目表
    """
    title = models.CharField(verbose_name='项目名称', max_length=32)

    def __str__(self):
        return self.title
