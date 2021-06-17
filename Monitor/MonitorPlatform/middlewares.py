"""
本想用中间件判断session，但是过程中发现无法显示图片验证码，故放弃，
选择在views页面中定义一个验证函数，使每次request请求都必须通过验证函数验证session
"""

"""
from django.utils.deprecation import MiddlewareMixin
from MonitorPlatform.models import session
from django.shortcuts import redirect
from django.shortcuts import render
from captcha.models import *
from django.http import HttpResponse


class SessionMiddle(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 判断如果是登入或注册页面就直接返回
        if request.path == "/login/" or request.path == "/register/" or request.path == "/":
            return None
        else:
            # 从cookies中取出my_session_id,然后从数据中取出数据进行比对
            my_session_id = request.COOKIES.get("session_id")
            session_obj = session.objects.filter(sessionID=my_session_id)
            # 数据库中没有该session_id就重定向到login页面
            if not session_obj:
                return redirect('/login/')
            else:
                return None


    @staticmethod
    def process_response(request, response):
        if request.path == "/login/" or request.path == "/register/":
            print(type(response))
            print(response.__dict__)
            return response
        else:
"""