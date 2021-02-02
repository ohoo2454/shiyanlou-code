from django.conf.urls import url

from rbac.views import role, user, menu

urlpatterns = [
    url(r'^role/list/$', role.role_list, name='role-list'),
    url(r'^role/add/$', role.role_add, name='role-add'),
    url(r'^role/edit/(?P<rid>\d+)/$', role.role_edit, name='role-edit'),
    url(r'^role/del/(?P<rid>\d+)/$', role.role_del, name='role-del'),

    # url(r'^user/list/$', user.user_list, name='user-list'),
    # url(r'^user/add/$', user.user_add, name='user-add'),
    # url(r'^user/edit/(?P<uid>\d+)/$', user.user_edit, name='user-edit'),
    # url(r'^user/del/(?P<uid>\d+)/$', user.user_del, name='user-del'),
    # url(r'^user/reset/password/(?P<uid>\d+)/$', user.user_reset_pwd, 
    #     name='user-reset-pwd'),

    url(r'^menu/list/$', menu.menu_list, name='menu-list'),
    url(r'^menu/add/$', menu.menu_add, name='menu-add'),
    url(r'^menu/edit/(?P<mid>\d+)/$', menu.menu_edit, name='menu-edit'),
    url(r'^menu/del/(?P<mid>\d+)/$', menu.menu_del, name='menu-del'),

    url(r'^second/menu/add/(?P<mid>\d+)/$', menu.second_menu_add, 
        name='second-menu-add'),
    url(r'^second/menu/edit/(?P<smid>\d+)/$', menu.second_menu_edit, 
        name='second-menu-edit'),
    url(r'^second/menu/del/(?P<smid>\d+)/$', menu.second_menu_del, 
        name='second-menu-del'),

    url(r'^permission/add/(?P<smid>\d+)/$', menu.permission_add, 
        name='permission-add'),
    url(r'^permission/edit/(?P<pid>\d+)/$', menu.permission_edit, 
        name='permission-edit'),
    url(r'^permission/del/(?P<pid>\d+)/$', menu.permission_del, 
        name='permission-del'),

    url(r'^multi/permissions/$', menu.multi_permissions, 
        name='multi-permissions'),
    url(r'^multi/permissions/del/(?P<pid>\d+)/$', menu.multi_permissions_del, 
        name='multi-permissions-del'),
    
    url(r'^distribute/permissions/$', menu.distribute_permissions, 
        name='distribute-permissions'),
]
