import hashlib
import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .models import User, ConfirmString
from .forms import UserForm, RegisterForm


def hash_code(s, salt='mysite'):

    s += salt
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def make_confirm_string(user):

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="https://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('309ef68529c7-service.simplelab.cn', code, 
                               settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, 
                                 settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# Create your views here.
def index(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))
    if request.method == 'POST':
        login_form = UserForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            message = '请检查填写的内容'
            if username.strip() and password:
                try:
                    user = User.objects.get(name=username)
                except:
                    message = '用户不存在'
                    return render(request, 'login/login.html', locals())
                if not user.has_confirmed:
                    message = '该用户还未经过邮件确认！'
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('index'))
                else:
                    message = '密码不正确'
                    return render(request, 'login/login.html', locals())
            else:
                return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_password = register_form.cleaned_data.get(
                    'confirm_password')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('gender')
            if confirm_password != password:
                message = '两次输入的密码不一致！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username).first()
                if same_name_user:
                    message = '用户名已存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email).first()
                if same_email_user:
                    message = '邮箱已被注册'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password)
                new_user.email = email
                new_user.gender = gender
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    request.session.flush()
    return redirect(reverse('login'))


def user_confirm(request):

    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
