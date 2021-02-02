from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, 
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 
                                   'placeholder': 'Username', 
                                   'autofocus': ''
                               }))
    password = forms.CharField(label='密码', max_length=256, 
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control', 
                                   'placeholder': 'Password'
                               }))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, 
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 
                                   'placeholder': 'Username', 
                                   'autofocus': ''
                               }))
    password = forms.CharField(label='密码', max_length=256, 
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control', 
                                   'placeholder': 'Password'
                               }))
    confirm_password = forms.CharField(label='确认密码', max_length=256, 
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control', 
                                           'placeholder': 'Confirm Password'
                                       }))
    email = forms.EmailField(label='邮箱', 
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control', 
                                 'placeholder': 'Email'
                             }))
    gender_choices = (
        (1, '男'), 
        (2, '女')
    )
    gender = forms.fields.ChoiceField(label='性别', choices=gender_choices, 
                                      widget=forms.widgets.RadioSelect())
    captcha = CaptchaField(label='验证码')
    