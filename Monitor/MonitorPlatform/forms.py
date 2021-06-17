from django import forms

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.forms import EmailField

from .models import *


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '用户名', 'class': 'form-control'}),
                               required=True, max_length=32, min_length=6)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': '邮箱', 'class': 'form-control'}),
                             required=True, max_length=32)
    passwd = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control'}),
                             required=True, max_length=32, min_length=8)
    repasswd = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': '确认密码', 'class': 'form-control'}),
                               required=True, max_length=32, min_length=8)

    class Meta:
        model = userInfo
        fields = ('username', 'passwd')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '账号', 'class': 'form-control'}),
                               required=True, max_length=128)
    passwd = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control'}),
                             required=True, )

    class Meta:
        model = userInfo
        fields = ('username', 'passwd')


class ResetForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': '邮箱', 'class': 'form-control'}),
                             required=True, max_length=128)

    class Meta:
        model = userInfo
        fields = ('email', 'passwd')
