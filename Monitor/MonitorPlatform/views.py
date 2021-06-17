from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render

from MonitorPlatform import models
from MonitorPlatform.forms import *
from MonitorPlatform.authority_monitor import *
from MonitorPlatform.sensitive_file_monitor import *
from MonitorPlatform.webshell_monitor import *

import hashlib
import json

import subprocess
import os
import sys

# 正则表达式
import re
import random
import time
import threading


# Create your views here.
def webshell_detect(request):
    if request.method == "GET":
        # 判断session
        if not session_check(request):
            return render(request, 'error/session_error.html')
        else:
            detect_result = webshellDetectResult.objects.all().order_by('-ID')
            return render(request, 'webshell_detect.html', {'webshell_detect_results': detect_result})
    else:   # POST
        file_obj = request.FILES.get('file')  # 拿到from获取到的file数据
        if (file_obj.name.split(".")[1]).lower() not in ['php', 'jsp']:
            stcode = 0
            message = '文件格式错误！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')
        else:
            os.system('rm -rf /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/upload_file/')
            os.system('mkdir /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/upload_file/')
            os.system('rm -rf /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class/')
            os.system('mkdir /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class/')
            f = open('MonitorPlatform/webshell_detect/detect/upload_file/' + file_obj.name + "", 'wb')  # 服务器创建上传同名的文件
            for line in file_obj.chunks():  # 分块拿上传数据
                f.write(line)  # 循环写入拿到的数据块到服务器
            f.close()
            p = subprocess.Popen(['python2', '/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect_webshell.py'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            output, error = p.communicate()
            output = output.decode('utf-8')
            output = output.replace('\n', '')
            detect_result = output[-1]
            print('detect result:'+detect_result)
            if detect_result != '1':
                webshellDetectResult.objects.create(
                    filename=file_obj.name,
                    detectResult="WebShell"
                )
            elif detect_result == '1':
                webshellDetectResult.objects.create(
                    filename=file_obj.name,
                    detectResult="Normal"
                )
            else:
                webshellDetectResult.objects.create(
                    filename=file_obj.name,
                    detectResult="Unknown"
                )
            stcode = '1'
            message = '文件上传成功,正在检测...'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')


def webshell_monitor(request):
    threading.Thread(target=webpath_monitor).start()
    if request.method == "GET":
        # 判断session
        if not session_check(request):
            return render(request, 'error/session_error.html')
        else:
            webshellMonitorResult = webshellMonitorLog.objects.all().order_by('-ID')
            return render(request, 'webshell_monitor.html', {'webshellMonitorLog': webshellMonitorResult})


def sensitive_file_monitor(request):
    threading.Thread(target=sens_file_monitor).start()
    if request.method == "GET":
        # 判断session
        if not session_check(request):
            return render(request, 'error/session_error.html')
        else:
            sensitiveFileEvents = sensitiveFileMonitorLog.objects.all().order_by('-ID')
            return render(request, 'sensitive_file_monitor.html', {'sensitiveFileEvents': sensitiveFileEvents})


def sensitive_file_list(request):
    if request.method == "POST":
        pathUploadForm = request.POST
        pathInput = pathUploadForm.get('pathInput')
        if pathInput[0:1] != '/' or pathInput[-1] == '/':
            stcode = 0
            message = "请输入正确路径!!!"
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')
        else:
            with open('MonitorPlatform/sensitive_file_list.txt', 'a') as f:
                f.write('\n')
                f.write(pathInput)
            stcode = 1
            message = "成功添加敏感文件至检测列表!"
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')
    else:
        # 判断session
        if not session_check(request):
            return render(request, 'error/session_error.html')
        else:
            path_list = []
            with open('MonitorPlatform/sensitive_file_list.txt', 'r') as f:
                for line in f:
                    path_list.extend(line.strip('\n').split(','))
            return render(request, 'sensitive_file_list.html', {'sensitive_file_path_list': path_list})


def local_authority_monitor(request):
    threading.Thread(target=authority_file_monitor).start()
    if request.method == "GET":
        # 判断session
        if not session_check(request):
            return render(request, 'error/session_error.html')
        else:
            authorityMonitorEvents = authorityMonitorLog.objects.all().order_by('-ID')
            return render(request, 'local_authority_monitor.html', {'authorityMonitorEvents': authorityMonitorEvents})


def user_profile_description(request):
    # 判断session
    if not session_check(request):
        return render(request, 'error/session_error.html')
    else:
        return render(request, 'user_profile_description.html')


# 注册
def register(request):
    # 验证码生成
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)

    stcode = 1

    if request.method == "POST":
        registerform = request.POST
        print(registerform)
        username = registerform.get('username')
        email = registerform.get('email')
        passwd = registerform.get('passwd')
        repasswd = registerform.get('repasswd')
        hash_key = registerform.get('hash_key')
        vcode = registerform.get('vcode')

        # 判断输入信息
        # 验证码
        check_vcode = str(CaptchaStore.objects.get(hashkey=hash_key))
        vcode = vcode.upper()
        if vcode != check_vcode:
            stcode = 0
            message = '验证码错误！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # username长度
        if len(username) < 6 or len(username) > 32:
            stcode = 0
            message = '用户名要求6～32位！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # email格式是否正确
        re_email = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if re.match(re_email, email) is None:
            stcode = 0
            message = '邮箱格式不正确！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')
        # passwd是否相同，passwd长度
        if passwd != repasswd:
            stcode = 0
            message = '两次输入的密码不同！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')
        if len(passwd) < 8 or len(passwd) > 32:
            stcode = 0
            message = '密码要求8～32位字母、数字、字符组合！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # username是否已经存在
        check_user = userInfo.objects.filter(username=username)
        if check_user:
            stcode = 0
            message = '用户名已存在！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # email是否已经存在
        check_email = userInfo.objects.filter(email=email)
        if check_email:
            stcode = 0
            message = '邮箱已注册！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # 向数据库写入用户信息
        if stcode == 1:
            userInfo.objects.create(
                username=username,
                email=email,
                passwd=hashlib.md5(passwd.encode(encoding='UTF-8')).hexdigest()
            )
            message = ''
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

    else:
        registerForm = RegisterForm()
        return render(request, 'register.html',
                      {'registerform': registerForm, 'hashkey': hashkey, 'image_url': image_url})


# 登录
def login(request):
    # 刷新所有session，删除无用的session
    now_time = time.time()
    session.objects.filter(createTime__lte=now_time-3600).delete()

    # 验证码生成
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)

    stcode = 1

    if request.method == "POST":
        loginform = request.POST
        username = loginform.get('username')
        passwd = loginform.get('passwd')
        hash_key = loginform.get('hash_key')
        vcode = loginform.get('vcode')

        # 判断输入信息
        # 验证码
        check_vcode = str(CaptchaStore.objects.get(hashkey=hash_key))
        vcode = vcode.upper()
        if vcode != check_vcode:
            stcode = 0
            message = '验证码错误！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # username长度
        if len(username) < 6 or len(username) > 32:
            stcode = 0
            message = '用户名要求6～32位！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # password长度
        if len(passwd) < 8 or len(passwd) > 32:
            stcode = 0
            message = '密码要求8～32位字母、数字、字符组合！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        # 用户是否存在
        if not userInfo.objects.filter(username=username).exists():
            stcode = 0
            message = '用户不存在！'
            ret = {'stcode': stcode, 'message': message}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        else:
            # 密码是否匹配
            passwd = hashlib.md5(passwd.encode(encoding='UTF-8')).hexdigest()
            userInformation = userInfo.objects.get(username=username)
            if userInformation.passwd != passwd:
                stcode = 0
                message = '密码错误，请重新输入！'
                ret = {'stcode': stcode, 'message': message}
                return HttpResponse(json.dumps(ret), content_type='application/json')

        # 验证完成后
        if stcode == 1:
            # 生成自定义session的随机key
            my_session_id = set_session()
            # 生成自定义session的value
            my_session_value = {'name': userInformation.username, 'password': userInformation.passwd}
            my_session_value = json.dumps(my_session_value)
            print(my_session_id)
            print(my_session_value)
            # 将自定义session信息存入数据库session_id对应key,session_value对应value
            now_time = time.time()
            print(now_time)
            if session.objects.filter(sessionValue=my_session_value).exists():     # 判断属否已经登录,session是否已经存在
                session.objects.filter(sessionValue=my_session_value).update(sessionID=my_session_id, createTime=now_time)
            else:
                session.objects.create(sessionID=my_session_id, sessionValue=my_session_value, createTime=now_time)
            # request.session['is_login'] = True
            # 记录用户登录
            loginRecord.objects.create(userID=userInformation.userID)
            message = ''
            ret = {'stcode': stcode, 'message': message}
            response = HttpResponse(json.dumps(ret), content_type='application/json')
            response.set_cookie("session_id", my_session_id, max_age=3600)
            return response

    else:
        loginForm = LoginForm()
        return render(request, 'login.html',
                      {'loginform': loginForm, 'hashkey': hashkey, 'image_url': image_url})


# 忘记密码
def reset(request):
    # 验证码生成
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)

    resetForm = ResetForm()
    if request.method == 'GET':
        return render(request, 'reset.html', {'resetform': resetForm, 'hashkey': hashkey, 'image_url': image_url})
    elif request.method == "POST":
        pass
    return render(request, 'reset.html', {'resetform': resetForm, 'hashkey': hashkey, 'image_url': image_url})


# 登出
def logout(request):
    # 判断session
    if not session_check(request):
        return render(request, 'error/session_error.html')
    else:
        my_session_id = request.COOKIES.get("session_id")
        session.objects.filter(sessionID=my_session_id).delete()
        return render(request, 'logout.html')


# set_session函数
def set_session():
    session_id = ''
    for i in range(32):
        num = str(random.randint(1, 9))
        letter = chr(random.randint(65, 90))
        group = random.choice([num, letter])
        session_id += group
        session_id = session_id.lower()
    return session_id


# session check
def session_check(request):
    # 从cookies中取出my_session_id,然后从数据中取出数据进行比对
    my_session_id = request.COOKIES.get("session_id")
    session_obj = session.objects.filter(sessionID=my_session_id)
    # 数据库中没有该session_id就重定向到login页面
    if session_obj:
        return True
    else:
        return False
