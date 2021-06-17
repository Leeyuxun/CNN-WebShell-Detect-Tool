# --*-- coding=utf-8 --*--

import pyinotify
import time
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render

from MonitorPlatform import models
from MonitorPlatform.forms import *

import hashlib
import json

import subprocess
import os
import sys

# 正则表达式
import re
import random


"""
--IN_ACCESS，即文件被访问 
--IN_MODIFY，文件被write 
--IN_ATTRIB，文件属性被修改，如chmod、chown、touch等 
--IN_CLOSE_WRITE，可写文件被close 
--IN_CLOSE_NOWRITE，不可写文件被close 
--IN_OPEN，文件被open 
--IN_MOVED_FROM，文件被移走,如mv 
--IN_MOVED_TO，文件被移来，如mv、cp 
--IN_CREATE，创建新文件 
--IN_DELETE，文件被删除，如rm 
--IN_DELETE_SELF，自删除，即一个可执行文件在执行时删除自己 
--IN_MOVE_SELF，自移动，即一个可执行文件在执行时移动自己 
--IN_UNMOUNT，宿主文件系统被umount 
--IN_CLOSE，文件被关闭，等同于(IN_CLOSE_WRITE | IN_CLOSE_NOWRITE) 
--IN_MOVE，文件被移动，等同于(IN_MOVED_FROM | IN_MOVED_TO
"""

# 本地权限监控目录
authority_list = [
    "/etc/passwd",
    "/etc/group",
    "/etc/shadow",
    "/etc/gshadow",
    "/etc/login.defs",
    "/etc/default/useradd",
    "/etc/skel"
]


# file event
class MyFileEventHandler(pyinotify.ProcessEvent):

    # def process_IN_ACCESS(self, event):
    #     """
    #     文件被访问
    #     :param event:
    #    :return:
    #     """
    #     for i in authority_list:
    #         if i in event.pathname:
    #             print('%s :Access file %s' % (time.time(), event.pathname))
    #             with open('authority_log.csv', 'a+') as f:
    #                 f.write('%s,Access,%s\n' % (time.time(), event.pathname))

    def process_IN_MODIFY(self, event):
        """
        文件被修改
        :param event:
        :return:
        """
        for i in authority_list:
            if i in event.pathname and (i+'~') not in event.pathname:
                print('%s :Modify file %s' % (time.time(), event.pathname))
                authorityMonitorLog.objects.create(
                    authorityFilename=event.pathname,
                    event="编辑文件"
                )

    def process_IN_ATTRIB(self, event):
        """
        文件属性被修改，如chmod、chown、touch等
        :param event:
        :return:
        """
        for i in authority_list:
            if i in event.pathname and (i+'~') not in event.pathname:
                print('%s :Attribute file %s' % (time.time(), event.pathname))
                authorityMonitorLog.objects.create(
                    authorityFilename=event.pathname,
                    event="修改属性"
                )

    def process_IN_DELETE(self, event):
        """
        文件被删除
        :param event:
        :return:
        """
        for i in authority_list:
            if i in event.pathname and (i+'~') not in event.pathname:
                print('%s :Delete file %s' % (time.time(), event.pathname))
                authorityMonitorLog.objects.create(
                    authorityFilename=event.pathname,
                    event="删除文件"
                )

    # def process_IN_DELETE_SELF(self, event):
    #     """
    #      文件自删除
    #     :param event:
    #     :return:
    #     """
    #     print('%s : Delete self file %s' % (time(), event.pathname))


def authority_file_monitor():
    monitor_obj = pyinotify.WatchManager()

    # path监控的目录
    path = "/etc/"
    monitor_obj.add_watch(path, pyinotify.ALL_EVENTS, rec=True)

    # event handler
    event_handler = MyFileEventHandler()

    # notifier
    monitor_loop = pyinotify.Notifier(monitor_obj, event_handler)
    monitor_loop.loop()


if __name__ == '__main__':
    authority_file_monitor()
