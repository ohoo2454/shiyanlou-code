from django.contrib import admin

from rbac.models import Permission, Role, UserInfo, Menu


# 自定义权限管理页面
class PermissionAdmin(admin.ModelAdmin):
    """
    自定义权限管理页面
    """
    list_display = ['title', 'url', 'name']
    list_editable = ['url', 'name']


# Register your models here.
admin.site.register(Permission, PermissionAdmin)
admin.site.register([Role, UserInfo, Menu])
