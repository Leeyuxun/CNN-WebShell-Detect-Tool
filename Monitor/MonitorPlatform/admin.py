from django.contrib import admin

from MonitorPlatform import models

# Register your models here.

admin.site.register(models.userInfo)
admin.site.register(models.loginRecord)
admin.site.register(models.session)
