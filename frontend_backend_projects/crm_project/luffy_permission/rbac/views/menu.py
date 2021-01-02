#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory

from rbac.models import Menu, Permission, UserInfo, Role
from rbac.forms.menu import (MenuModelForm, SecondMenuModelForm, 
                             PermissionModelForm, MultiAddPermissionForm,
                             MultiEditPermissionForm)
from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict


# 菜单信息
def menu_list(request):
    """
    菜单信息
    :param request:
    :return:
    """
    menus = Menu.objects.all()
    menu_id = request.GET.get('mid')  # 选中的一级菜单id
    second_menu_id = request.GET.get('smid')  # 选中的二级菜单id
    # print(menu_id, second_menu_id)
    menu_exists = Menu.objects.filter(id=menu_id).exists()
    if not menu_exists:
        menu_id = None
    if menu_id:
        second_menus = Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []
    second_menu_exists = Permission.objects.filter(
            pid_id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None
    if second_menu_id:
        permissions = Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []
    return render(
        request, 
        'rbac/menu_list.html', 
        {
            'menus': menus, 
            'second_menus': second_menus, 
            'menu_id': menu_id, 
            'second_menu_id': second_menu_id,
            'permissions': permissions
        }
    )


# 添加菜单
def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 编辑菜单
def menu_edit(request, mid):
    """
    菜单信息
    :param request:
    :param mid: 菜单id
    :return:
    """
    menu_obj = Menu.objects.filter(id=mid).first()
    if not menu_obj:
        return HttpResponse('数据不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(instance=menu_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 删除菜单
def menu_del(request, mid):
    """
    删除菜单
    :param request:
    :param mid: 菜单id
    :return:
    """
    origin_url = memory_reverse(request, 'rbac:menu-list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    Menu.objects.filter(id=mid).delete()
    return redirect(origin_url)


# 添加二级菜单
def second_menu_add(request, mid):
    """
    添加二级菜单
    :param request:
    :param mid: 要添加二级菜单的一级菜单id
    :return:
    """
    menu_obj = Menu.objects.filter(id=mid).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 修改二级菜单
def second_menu_edit(request, smid):
    """
    修改二级菜单
    :param request:
    :param smid: 二级菜单id
    :return:
    """
    permission_obj = Permission.objects.filter(id=smid).first()
    if not permission_obj:
        return HttpResponse('数据不存在')
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(instance=permission_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 删除二级菜单
def second_menu_del(request, smid):
    """
    删除二级菜单
    :param request:
    :param smid: 二级菜单id
    :return:
    """
    origin_url = memory_reverse(request, 'rbac:menu-list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    Permission.objects.filter(id=smid).delete()
    return redirect(origin_url)


# 添加三级菜单
def permission_add(request, smid):
    """
    添加三级菜单
    :param request:
    :param smid: 选中的二级菜单id
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        permission_obj = Permission.objects.filter(id=smid).first()
        if not permission_obj:
            return HttpResponse('二级菜单不存在，请重新选择')
        form.instance.pid = permission_obj
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 修改三级菜单
def permission_edit(request, pid):
    """
    修改三级菜单
    :param request:
    :param pid: 选中的三级菜单id
    :return:
    """
    permission_obj = Permission.objects.filter(id=pid).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(instance=permission_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu-list'))
    return render(request, 'rbac/change.html', {'form': form})


# 删除三级菜单
def permission_del(request, pid):
    """
    删除三级菜单
    :param request:
    :param pid: 选中的三级菜单id
    :return:
    """
    origin_url = memory_reverse(request, 'rbac:menu-list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    Permission.objects.filter(id=pid).delete()
    return redirect(origin_url)


# 批量操作权限的显示
def multi_permissions(request):
    """
    批量操作权限的显示
    :return:
    """
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)
    generate_formset = None
    update_formset = None

    # 批量生成
    if request.method == 'POST' and post_type == 'generate':
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset            

    # 批量更新
    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    permission_obj = Permission.objects.filter(
                            id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(permission_obj, k, v)
                        permission_obj.validate_unique()
                        permission_obj.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset
                                    
    # 1.获取项目中所有的url
    all_url_dict = get_all_url_dict()
    """
    {
        'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
        ....
    }
    """
    router_name_set = set(all_url_dict.keys())

    # 2.获取数据库中所有的url
    permissions = Permission.objects.all().values('id', 'title', 'name', 
            'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        """
        {
            'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
            'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
            ...
        }
        """
        permission_name_set.add(row['name'])
    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if router_row_dict['url'] != value['url']:
            value['url'] = '路由和数据库中不一致'

    # 3.分别计算出应该添加、删除和更新的url
    # 计算出应该添加的url
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() \
                if name in generate_name_list]
        )

    # 计算出应该删除的url
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() \
            if name in delete_name_list]

    # 计算出应该更新的url
    if not update_formset:
        update_name_list = router_name_set & permission_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permission_dict.items() \
                if name in update_name_list]
        )
    return render(
        request, 
        'rbac/multi_permissions.html', 
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': update_formset,
        }
    )


# 批量操作页面的删除权限
def multi_permissions_del(request, pid):
    """
    批量操作页面的删除权限
    :param request:
    :param pid: 需要删除权限的id
    :return:
    """
    url = memory_reverse(request, 'rbac:multi-permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    Permission.objects.filter(id=pid).delete()
    return redirect(url)


# 权限分配
def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """
    # 获取用户id和用户对象
    user_id = request.GET.get('uid')
    user_obj = UserInfo.objects.filter(id=user_id).first()
    if not user_obj:
        user_id = None
    
    # 获取身份id和身份对象
    role_id = request.GET.get('rid')
    role_obj = Role.objects.filter(id=role_id).first()
    if not role_obj:
        role_id = None
    
    # 为用户指定身份
    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        if not user_obj:
            return HttpResponse('请先选择用户，然后再分配身份')
        else:
            user_obj.roles.set(role_id_list)
    
    # 为身份分配权限
    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_obj:
            return HttpResponse('请先选择身份，然后再分配权限')
        else:
            role_obj.permissions.set(permission_id_list)
    
    # 获取用户的所有身份
    if user_id:
        user_has_roles = user_obj.roles.all()
    else:
        user_has_roles = []
    user_has_roles_dict = {item.id: None for item in user_has_roles}
    
    # 获取用户的所有权限
    # 选中用户身份，优先显示用户此身份的所有权限
    if role_obj:
        user_has_permissions = role_obj.permissions.all()
        user_has_permissions_dict = {
            item.id: None for item in user_has_permissions
        }
    # 未选中身份，但选中用户，显示此用户所拥有的所有权限
    elif user_obj:
        user_has_permissions = user_obj.roles.filter(
            permissions__id__isnull=False).values('id', 
                                                  'permissions').distinct()
        user_has_permissions_dict = {
            item['permissions']: None for item in user_has_permissions
        }
    else:
        user_has_permissions_dict = {}
    
    # 获取所有用户信息
    all_user_list = UserInfo.objects.all()

    # 获取所有身份信息
    all_role_list = Role.objects.all()

    # 不知道干嘛用的
    menu_permission_list = []

    # 获取所有一级菜单
    all_menu_list = Menu.objects.all().values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item
    """
    {
        1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
        2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
        3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
    }
    """

    # 获取所有二级菜单（可以做菜单的权限）
    all_second_menu_list = Permission.objects.filter(
            menu__isnull=False).values('id', 'title', 'menu_id')
    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """
    all_second_menu_dict = {}
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)
    """
    {
        1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        2:{id:2,title:x1, menu_id:1,children:[] },
        3:{id:3,title:x1, menu_id:2,children:[] },
        4:{id:4,title:x1, menu_id:3,children:[] },
        5:{id:5,title:x1, menu_id:2,children:[] },
    }
    """

    # 获取所有三级菜单（不能做菜单的权限）
    all_permission_list = Permission.objects.filter(
            menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)
    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },
        
    ]
    """
    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        }
    )
