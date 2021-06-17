"""Monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from MonitorPlatform.views import *
from captcha.views import captcha_refresh  # 验证码刷新功能，captcha_refresh为captcha.views内置方法，不需要我们单独写

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('MonitorPlatform.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('captcha/', include('captcha.urls')),       # 图片验证码 路由
    path('refresh/', captcha_refresh),      # 点击可以刷新验证码
]
