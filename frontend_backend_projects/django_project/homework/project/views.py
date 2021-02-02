# project/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Teacher, Student, Role
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


""" 首页 """
def index(request):

    return render(request,'project/index.html')


""" 注册 """
def register(request):

    if request.method == 'POST':
        # 验证表单 RegistrationForm 的数据是否有效
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            role = form.cleaned_data['role']
            # 使用内置 User 自带 create_user 方法创建用户，不需要使用 save()
            user = User.objects.create_user(username=username, password=password)
            # 首先创建一个 Role，然后 Student 或 Teacher 一对一绑定该 Role
            role_profile = Role(role=int(role), user=user)
            role_profile.save()
            # 如果直接使用 objects.create() 方法后不需要使用 save()
            if int(role) == 0:
                user_profile = Student(user=role_profile)
                user_profile.save()
            else:
                user_profile = Teacher(user=role_profile)
                user_profile.save()
            # 注册成功，通过 HttpResponseRedirect 方法转到登录页面
            return HttpResponseRedirect("/login/")
    else:
        # 如果用户没有提交表单或不是通过POST方法提交表单，转到登录页面，生成一张空的 RegistrationForm
        form = RegistrationForm()
    return render(request, 'project/register.html', {'form': form})


""" 登录 """
def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 调用 Django 自带的 auth.authenticate() 来验证用户名和密码是否正确，若正确则返回 None
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # 调用 auth.login() 来进行登录
                auth.login(request, user)
                # 登录成功，转到用户个人信息页面
                # [] 是有序的可 reverse，{} 是无序的
                return HttpResponseRedirect(reverse('project:index'))
            else:
                # 登录失败
                return render(request, 'project/login.html',
                        {'form': form, 'message': '密码错误，请重试！'})
    else:
        # 如果用户没有提交表单或不是通过 POST 方法提交表单，转到登录页面，生成一张空的 LoginForm
        form = LoginForm()
    return render(request, 'project/login.html', {'form': form})


# 注销登陆
def logout(request):
    
    auth.logout(request)
    
    return HttpResponseRedirect("/login/")


def profile(request, pk):
    
    user = get_object_or_404(User, pk=pk)
    
    return render(request, 'project/profile.html', {'user': user})
    

# 信息更新
def profile_update(request, pk):
    
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            if request.user.role.role == 0:
                user.role.student.name = form.cleaned_data['name']
                user.role.student.gender = form.cleaned_data['gender']
                user.role.student.save()
                # 请重新复习一遍 URL 重定向的三种方法
                return HttpResponseRedirect(reverse('project:profile',
                                                    args=[user.id]
                                                    ))
            else:
                user.role.teacher.name = form.cleaned_data['name']
                user.role.teacher.gender = form.cleaned_data['gender']
                user.role.teacher.save()
                return HttpResponseRedirect(reverse('project:profile',
                                                    args=[user.id]
                                                    ))
    else:
        # 将用户原信息返回到前端
        if request.user.role.role == 0:
            default_data = {'name': user.role.student.name,
                            'gender': user.role.student.gender,
                        }
        else:
            default_data = {'name': user.role.teacher.name,
                            'gender': user.role.teacher.gender,
                        }
        form = ProfileForm(default_data)
    return render(request,
                  'project/profile_update.html',
                  {'form': form, 'user': user})


# 密码修改
def pwd_change(request, pk):

    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username
            # auth.authenticate 对用户登录的账号密码进行验证，若通过验证，则返回 None
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/login/")
            else:
                return render(request,
                            'project/pwd_change.html',
                            {'form':form,'user':user, 'message':'原密码错误，请重新输入！'})
    else:
        form = PwdChangeForm()
    return render(request, 'project/pwd_change.html', {'form': form, 'user': user})
    