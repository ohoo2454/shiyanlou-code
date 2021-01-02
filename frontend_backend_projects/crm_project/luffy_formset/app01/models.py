from django.db import models

# Create your models here.
# 菜单表
class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单', max_length=32)
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
    name = models.CharField(verbose_name='代码', max_length=64, null=True, 
            blank=True)
    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', 
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
