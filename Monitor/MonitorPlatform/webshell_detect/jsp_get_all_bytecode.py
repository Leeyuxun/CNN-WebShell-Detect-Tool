# coding=utf-8
import commands
import requests
import multiprocessing
import os
import re

import gensim
import numpy as np
import tensorflow as tf
import tflearn
from sklearn import metrics
from tflearn.data_utils import to_categorical
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.merge_ops import merge

min_code_count = 0  # The min bytecode/bytecode length of sample file

# Sample path
black_jsp_train_dir = "data/black/jsp/train/"
black_jsp_test_dir = "data/black/jsp/test/"
white_jsp_train_dir = "data/white/jsp/train/"
white_jsp_test_dir = "data/white/jsp/test/"

# jsp bytecode
jsp_bytecode = '/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/jsp-bytecode.txt'
all_jsp_train_bytecode = 'jsp_bytecode_tags/all-jsp-train-bytecode.txt'
all_jsp_test_bytecode = 'jsp_bytecode_tags/all-jsp-test-bytecode.txt'
all_jsp_train_tags = 'jsp_bytecode_tags/all-jsp-train-tags.txt'
all_jsp_test_tags = 'jsp_bytecode_tags/all-jsp-test-tags.txt'

# Sample count
black_jsp_train_count = 0
black_jsp_test_count = 0
white_jsp_train_count = 0
white_jsp_test_count = 0

jsp_detect_class = '/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class'


# Extract bytecode through regular expression
def extract_jsp_bytecode_re(php_file_path):
    opcode_list = []
    bytecode_sample_list = open(jsp_bytecode, 'r').read().splitlines()
    # Use vld plugin to extract opcode
    cmd ="javap -c " + php_file_path
    output = commands.getoutput(cmd)
    output_list = output.split(' ')
    for i in output_list:
        if i in bytecode_sample_list:
            opcode_list.append(i)
    print("    opcode count %d" % len(opcode_list))
    # print opcode_list
    return opcode_list  # Return the opcode of a sample file, type=list


# Get bytecode of jsp file
def get_jsp_bytecode(jsp_dir):
    global min_code_count
    all_files_bytecode_list = []  # A list to store all bytecodes
    i = 1  # Auxiliary parameter, counter
    # Traverse all jsp files to extract bytecode
    for path, dirs, fileList in os.walk(jsp_dir):
        for file_name in fileList:
            if file_name.endswith('.class') and str(file_name).find("$") == -1:
                file_path = os.path.join(path, file_name)
                print("%d: Load %s bytecode" % (i, file_path))
                # Call extract_bytecode_re to extract the bytecode of each sample file
                jsp_file_bytecode_list = extract_jsp_bytecode_re(file_path)
                # Determine whether it is less than the minimum bytecode length
                if len(jsp_file_bytecode_list) > min_code_count:
                    i += 1
                    # jsp_file_bytecode_str = " ".join(jsp_file_bytecode_list)  # Convert bytecode list to str
                    # Add the bytecode of each sample to the list and become one element
                    all_files_bytecode_list.append(jsp_file_bytecode_list)
                else:
                    # if it is less than the min length, remove it, and delete the sample file
                    print("    Can't load %s bytecode, its bytecode less than min_bytecode_count!!!" % file_name)
                    # os.remove(file_path)
    # print(all_files_bytecode_list)
    return all_files_bytecode_list


# Get all bytecode/bytecode of all sample files
def get_all_jsp_file_bytecode():
    global white_jsp_train_count
    global white_jsp_test_count
    global black_jsp_train_count
    global black_jsp_test_count
    global black_jsp_train_dir
    global white_jsp_test_dir

    # jsp webshell train
    black_jsp_train_files_bytecode_list = get_jsp_bytecode(black_jsp_train_dir)  # black jsp files bytecode, Two-dimensional list
    black_jsp_train_tags_list = [1] * len(black_jsp_train_files_bytecode_list)  # black jsp tags
    black_jsp_train_count = len(black_jsp_train_files_bytecode_list)  # black jsp count

    # jsp webshell test
    black_jsp_test_files_bytecode_list = get_jsp_bytecode(black_jsp_test_dir)  # black jsp files bytecode, Two-dimensional list
    black_jsp_test_tags_list = [1] * len(black_jsp_test_files_bytecode_list)  # black jsp tags
    black_jsp_test_count = len(black_jsp_test_files_bytecode_list)  # black jsp count

    # jsp normal sample train
    white_jsp_train_files_bytecode_list = get_jsp_bytecode(white_jsp_train_dir)  # white jsp files bytecode, Two-dimensional list
    white_jsp_train_tags_list = [0] * len(white_jsp_train_files_bytecode_list)  # white jsp tags
    white_jsp_train_count = len(white_jsp_train_files_bytecode_list)  # white jsp count

    # jsp normal sample test
    white_jsp_test_files_bytecode_list = get_jsp_bytecode(white_jsp_test_dir)  # white jsp files bytecode, Two-dimensional list
    white_jsp_test_tags_list = [0] * len(white_jsp_test_files_bytecode_list)  # white jsp tags
    white_jsp_test_count = len(white_jsp_test_files_bytecode_list)  # white jsp count

    # Combine positive and negative samples
    # train
    all_jsp_train_files_bytecode_list = black_jsp_train_files_bytecode_list + white_jsp_train_files_bytecode_list  # Store all bytecodes of all sample
    all_jsp_train_tags_list = black_jsp_train_tags_list + white_jsp_train_tags_list  # Sample tag, 1 means webshell, 0 means normal sample
    # train
    all_jsp_test_files_bytecode_list = black_jsp_test_files_bytecode_list + white_jsp_test_files_bytecode_list  # Store all bytecodes of all sample
    all_jsp_test_tags_list = black_jsp_test_tags_list + white_jsp_test_tags_list  # Sample tag, 1 means webshell, 0 means normal sample

    # Write bytecode to txt file
    # train bytecode
    f = open(all_jsp_train_bytecode, 'a')
    for one_jsp_train_file_bytecode_list in all_jsp_train_files_bytecode_list:
        one_jsp_train_file_bytecode_str = " ".join(one_jsp_train_file_bytecode_list)
        f.write(one_jsp_train_file_bytecode_str)
        f.write('\n')
    f.close()
    # test bytecode
    f = open(all_jsp_test_bytecode, 'a')
    for one_jsp_test_file_bytecode_list in all_jsp_test_files_bytecode_list:
        one_jsp_test_file_bytecode_str = " ".join(one_jsp_test_file_bytecode_list)
        f.write(one_jsp_test_file_bytecode_str)
        f.write('\n')
    f.close()
    # train tags
    f = open(all_jsp_train_tags, 'a')
    for jsp_train_tag in all_jsp_train_tags_list:
        f.write(str(jsp_train_tag))
        f.write("\n")
    f.close()
    # test tags
    f = open(all_jsp_test_tags, 'a')
    for jsp_test_tag in all_jsp_test_tags_list:
        f.write(str(jsp_test_tag))
        f.write("\n")
    f.close()

    return all_jsp_train_files_bytecode_list, all_jsp_train_tags_list, all_jsp_test_files_bytecode_list, all_jsp_test_tags_list


# compile jsp to class
def compile_jsp_to_class(jsp_dir):
    global min_code_count
    all_files_opcode_list = []  # A list to store all opcodes
    i = 1  # Auxiliary parameter, counter
    # Traverse all PHP files to extract opcode
    for path, dirs, fileList in os.walk(jsp_dir):
        for jsp_file_name in fileList:
            jsp_file_path = os.path.join(path, jsp_file_name)
            print("Path: %s" % (jsp_file_path))
            # move jsp file to tomcat web path
            cmd = "cp " + jsp_file_path + " /opt/tomcat/apache-tomcat-9.0.45/webapps/ROOT/"
            os.system(cmd)
            # Visit the jsp page through python request
            url = "http://localhost:8080/"
            requests.get(url + jsp_file_name)
            # judge whether to generate class files
            prefix_jsp = os.path.splitext(jsp_file_name)[0]         # jsp file prefix
            suffix_jsp = os.path.splitext(jsp_file_name)[-1][1:]    # jsp file suffix
            class_file_name = '_' + prefix_jsp + '_' + suffix_jsp +'.class'        # class file name
            java_file_name = '_' + prefix_jsp + '_' + suffix_jsp +'.java'           # java file name
            print(class_file_name)
            class_file_path = "/opt/tomcat/apache-tomcat-9.0.45/work/Catalina/localhost/ROOT/org/apache/jsp/" + class_file_name
            java_file_path = "/opt/tomcat/apache-tomcat-9.0.45/work/Catalina/localhost/ROOT/org/apache/jsp/" + java_file_name
            if os.path.exists(class_file_path):
                print("Compile jsp to class successfully!")
                class_file_name = '_' + prefix_jsp + '_*.class'  # class file name
                java_file_name = '_' + prefix_jsp + '_*.java'  # java file name
                class_file_path = "/opt/tomcat/apache-tomcat-9.0.45/work/Catalina/localhost/ROOT/org/apache/jsp/" + class_file_name
                java_file_path = "/opt/tomcat/apache-tomcat-9.0.45/work/Catalina/localhost/ROOT/org/apache/jsp/" + java_file_name
                mv_class_file = "mv " + class_file_path + ' ' + jsp_detect_class
                rm_java_file = "rm " + java_file_path
                rm_jsp_file = "rm /opt/tomcat/apache-tomcat-9.0.45/webapps/ROOT/" + jsp_file_name
                os.system(mv_class_file)
                print mv_class_file
                os.system(rm_java_file)
                os.system(rm_jsp_file)
            else:
                print("Error: Can't compile jsp file %s to class file!!!" % jsp_file_name)
