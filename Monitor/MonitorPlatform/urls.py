from django.urls import path

from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('reset/', reset, name='reset'),
    path('webshell_monitor/', webshell_monitor, name='webshell_monitor'),
    path('webshell_detect/', webshell_detect, name='webshell_detect'),
    path('sensitive_file_monitor/', sensitive_file_monitor, name='sensitive_file_monitor'),
    path('sensitive_file_list/', sensitive_file_list, name='sensitive_file_list'),
    path('local_authority_monitor/', local_authority_monitor, name='local_authority_monitor'),
    path('user_profile_description/', user_profile_description, name='user_profile_description'),
]
