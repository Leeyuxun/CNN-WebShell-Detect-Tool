from MonitorPlatform.forms import *
import os
import subprocess


def exteate_file(monitor_path):
    detect_file_list = []  # 需要检测的文件
    for home, dirs, files in os.walk(monitor_path):
        for filename in files:
            if os.path.splitext(filename)[-1] in [".php", ".jsp"]:
                detect_file_list.append(os.path.join(home, filename))
    return detect_file_list


def webpath_monitor():
    monitor_path = '/var/www/html/'
    detect_file_list = exteate_file(monitor_path)       # 需要检测的文件列表

    # 循环遍历检测
    for detect_file in detect_file_list:
        if webshellMonitorLog.objects.filter(filePath=detect_file).exists():
            continue
        os.system('rm -rf MonitorPlatform/webshell_detect/detect/upload_file/')
        os.system('mkdir MonitorPlatform/webshell_detect/detect/upload_file/')
        os.system('rm -rf MonitorPlatform/webshell_detect/detect/jsp_class/')
        os.system('mkdir MonitorPlatform/webshell_detect/detect/jsp_class/')

        mv_file = 'cp ' + detect_file + ' MonitorPlatform/webshell_detect/detect/upload_file/'
        os.system(mv_file)

        p = subprocess.Popen(['python2', '/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect_webshell.py'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, error = p.communicate()
        output = output.decode('utf-8')
        output = output.replace('\n', '')
        detect_result = output[-1]
        print('detect result:' + detect_result)
        if detect_result != '1':
            webshellMonitorLog.objects.create(
                filePath=detect_file,
                detectResult="WebShell"
            )
            os.system('mv ' + detect_file + ' MonitorPlatform/webshell_monitor/webshell/')
        elif detect_result == '1':
            webshellMonitorLog.objects.create(
                filePath=detect_file,
                detectResult="Normal"
            )
        else:
            webshellMonitorLog.objects.create(
                filePath=detect_file,
                detectResult="Unknown"
            )
            os.system('mv ' + detect_file + ' MonitorPlatform/webshell_monitor/unknown/')



if __name__ == '__main__':
    webpath_monitor()
