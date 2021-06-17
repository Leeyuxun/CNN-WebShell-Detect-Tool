from django.db import models


# Create your models here.

class userInfo(models.Model):
    """
    userInfo表
    """
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    passwd = models.CharField(max_length=32)
    createTime = models.DateTimeField(auto_now_add=True)

    # userChecked = models.BooleanField(unique=True)

    class Meta:
        db_table = 'userInfo'


class loginRecord(models.Model):
    """
    loginStatus表
    """
    ID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    loginTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loginRecord'


class session(models.Model):
    """
    session表
    """
    ID = models.AutoField(primary_key=True)
    sessionID = models.CharField(max_length=32)
    sessionValue = models.CharField(max_length=128)
    createTime = models.FloatField()

    class Meta:
        db_table = "session"


class webshellDetectResult(models.Model):
    """
    webshellDetectResult表
    """
    ID = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=128)
    detectResult = models.CharField(max_length=128)
    detectTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webshellDetectResult'


class webshellMonitorLog(models.Model):
    """
    webshell监测日志
    """
    ID = models.AutoField(primary_key=True)
    filePath = models.CharField(max_length=256)
    detectResult = models.CharField(max_length=128)
    detectTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webshellMonitorLog'


class authorityMonitorLog(models.Model):
    """
    本地权限监测日志
    """
    ID = models.AutoField(primary_key=True)
    authorityFilename = models.CharField(max_length=128)
    event = models.CharField(max_length=128)
    detectTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authorityMonitorLog'


class sensitiveFileMonitorLog(models.Model):
    """
    敏感文件监测日志
    """
    ID = models.AutoField(primary_key=True)
    sensitiveFilename = models.CharField(max_length=128)
    event = models.CharField(max_length=128)
    detectTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sensitiveFileMonitorLog'
