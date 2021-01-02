from django.db import models


# Create your models here.
# 菜单表
class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '菜单管理'
        verbose_name_plural = '菜单管理'


# 权限表
class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='权限名称', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    name = models.CharField(verbose_name='URL别名', max_length=64, null=True, 
            blank=True)
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', 
            related_name='ps', null=True, blank=True, 
            help_text='对于无法作为菜单的URL，可以为其选择一个可以作为菜单\
            的权限，那么访问时，则默认选中此权限', 
            limit_choices_to={'menu__isnull': False})
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True,
            blank=True, help_text='null 表示非菜单')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限管理'
        verbose_name_plural = '权限管理'


# 角色表
class Role(models.Model):
    """
    身份表
    """
    title = models.CharField(verbose_name='身份名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '身份管理'
        verbose_name_plural = '身份管理'


# 用户信息表
class UserInfo(models.Model):
    """
    用户信息表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱')
    roles = models.ManyToManyField(verbose_name='拥有的所有身份', to=Role, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = '用户管理'
        # verbose_name_plural = '用户管理'
        # django以后再做数据库迁移时，不再为UserInfo类创建相关的表以及表结构了
        # 此类可以当做"父类"，被其他Model类继承
        abstract = True
