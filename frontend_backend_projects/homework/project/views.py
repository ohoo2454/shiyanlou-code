from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Teacher, Student, Role
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm


# Create your views here.
def index(request):
    '''
    首页
    '''
    return render(request, 'project/index.html')
    # return HttpResponse('在线作业管理系统！')


def register(request):
    '''
    注册
    '''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            role = form.cleaned_data['role']
            user = User.objects.create_user(username=username, 
                    password=password)
            role_profile = Role(role=int(role), user=user)
            role_profile.save()
            if int(role) == 0:
                user_profile = Student(user=role_profile)
                user_profile.save()
            else:
                user_profile = Teacher(user=role_profile)
                user_profile.save()
            return HttpResponseRedirect(reverse('project:login'))
    else:
        form = RegistrationForm()
    return render(request, 'project/register.html', {'form': form})


def login(request):
    '''
    登录
    '''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('project:index'))
            else:
                return render(request, 'project/login.html', 
                        {'form': form, 'message': '密码错误，请重试！'})
    else:
        form = LoginForm()
    return render(request, 'project/login.html', {'form': form})


def logout(request):
    '''
    退出登录
    '''
    auth.logout(request)
    return HttpResponseRedirect(reverse('project:login'))
    

def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'project/profile.html', {'user': user})


def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            if request.user.role.role == 0:
                user.role.student.name = form.cleaned_data['name']
                user.role.student.gender = form.cleaned_data['gender']
                user.role.student.save()
                return HttpResponseRedirect(reverse('project:profile', 
                        args=[user.id]))
            else:
                user.role.teacher.name = form.cleaned_data['name']
                user.role.teacher.gender = form.cleaned_data['gender']
                user.role.teacher.save()
                return HttpResponseRedirect(reverse('project:profile',
                        args=[user.id]))
    else:
        if request.user.role.role == 0:
            default_data = {
                'name': user.role.student.name, 
                'gender': user.role.student.gender,
            }
        else:
            default_data = {
                'name': user.role.teacher.name,
                'gender': user.role.teacher.gender,
            }
        form = ProfileForm(default_data)
    return render(request, 'project/profile_update.html', 
            {'form': form, 'user': user})


def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('project:login'))
            else:
                return render(request, 'project/pwd_change.html', 
                        {'form': form, 'user': user, 
                            'messages': '原密码错误，请重新输入!'})
    else:
        form = PwdChangeForm()
    return render(request, 'project/pwd_change.html', 
            {'form': form, 'user': user})
