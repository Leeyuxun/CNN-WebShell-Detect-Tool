# coding=utf-8
import commands
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

max_features = 128  #
max_document_length = 160  # The opcode/bytecode length of the sample file
min_code_count = 0  # The min opcode/bytecode length of sample file

# Sample path
black_php_train_dir = "data/black/php/train/"
black_php_test_dir = "data/black/php/test/"
white_php_train_dir = "data/white/php/train/"
white_php_test_dir = "data/white/php/test/"

# PHP opcode
php_opcode = 'php-opcode.txt'
all_php_train_opcode = 'php_opcode_tags/all-php-train-opcode.txt'
all_php_test_opcode = 'php_opcode_tags/all-php-test-opcode.txt'
all_php_train_tags = 'php_opcode_tags/all-php-train-tags.txt'
all_php_test_tags = 'php_opcode_tags/all-php-test-tags.txt'

# Sample count
black_php_train_count = 0
black_php_test_count = 0
white_php_train_count = 0
white_php_test_count = 0

# PHP path
php_bin = "/usr/bin/php"

# Word2Vec model path
word2vec_model = "Word2Vec.model"


# Extract opcode through regular expression
def extract_php_opcode_re(php_file_path):
    global php_bin
    # Use vld plugin to extract opcode
    cmd = php_bin + " -d vld.active=1 -d vld.execute=0 " + php_file_path
    output = commands.getoutput(cmd)
    opcode_list = re.findall(r'\s(\b[A-Z_][A-Z_]+\b)\s', output)
    # print(tokens)
    # print(type(tokens))
    print("    opcode count %d" % len(opcode_list))
    return opcode_list  # Return the opcode of a sample file, type=list


# Get opcode of php file
def get_php_opcode(php_dir):
    global min_code_count
    all_files_opcode_list = []  # A list to store all opcodes
    i = 1  # Auxiliary parameter, counter
    # Traverse all PHP files to extract opcode
    print(php_dir)
    for path, dirs, fileList in os.walk(php_dir):
        for file_name in fileList:
            if file_name.endswith('.php'):
                file_path = os.path.join(path, file_name)
                print("%d: Load %s opcode" % (i, file_path))
                # Call extract_opcode_re to extract the opcode of each sample file
                php_file_opcode_list = extract_php_opcode_re(file_path)
                # Determine whether it is less than the minimum opcode length
                if len(php_file_opcode_list) > min_code_count:
                    i += 1
                    # php_file_opcode_str = " ".join(php_file_opcode_list)  # Convert opcode list to str
                    # Add the opcode of each sample to the list and become one element
                    all_files_opcode_list.append(php_file_opcode_list)
                else:
                    # if it is less than the min length, remove it, and delete the sample file
                    print("    Can't load %s opcode, its opcode less than min_opcode_count!!!" % file_name)
                    os.remove(file_path)
    # print(all_files_opcode_list)
    return all_files_opcode_list


# Get all opcode/bytecode of all sample files
def get_all_php_file_opcode():
    global white_php_train_count
    global white_php_test_count
    global black_php_train_count
    global black_php_test_count
    global black_php_train_dir
    global white_php_test_dir

    # PHP webshell train
    black_php_train_files_opcode_list = get_php_opcode(
        black_php_train_dir)  # black php files opcode, Two-dimensional list
    black_php_train_tags_list = [1] * len(black_php_train_files_opcode_list)  # black php tags
    black_php_train_count = len(black_php_train_files_opcode_list)  # black php count

    # PHP webshell test
    black_php_test_files_opcode_list = get_php_opcode(
        black_php_test_dir)  # black php files opcode, Two-dimensional list
    black_php_test_tags_list = [1] * len(black_php_test_files_opcode_list)  # black php tags
    black_php_test_count = len(black_php_test_files_opcode_list)  # black php count

    # PHP normal sample train
    white_php_train_files_opcode_list = get_php_opcode(
        white_php_train_dir)  # white php files opcode, Two-dimensional list
    white_php_train_tags_list = [0] * len(white_php_train_files_opcode_list)  # white php tags
    white_php_train_count = len(white_php_train_files_opcode_list)  # white php count

    # PHP normal sample test
    white_php_test_files_opcode_list = get_php_opcode(
        white_php_test_dir)  # white php files opcode, Two-dimensional list
    white_php_test_tags_list = [0] * len(white_php_test_files_opcode_list)  # white php tags
    white_php_test_count = len(white_php_test_files_opcode_list)  # white php count

    # Combine positive and negative samples
    # train
    all_php_train_files_opcode_list = black_php_train_files_opcode_list + white_php_train_files_opcode_list  # Store all opcodes of all sample
    all_php_train_tags_list = black_php_train_tags_list + white_php_train_tags_list  # Sample tag, 1 means webshell, 0 means normal sample
    # train
    all_php_test_files_opcode_list = black_php_test_files_opcode_list + white_php_test_files_opcode_list  # Store all opcodes of all sample
    all_php_test_tags_list = black_php_test_tags_list + white_php_test_tags_list  # Sample tag, 1 means webshell, 0 means normal sample

    # Write opcode to txt file
    # train opcode
    f = open(all_php_train_opcode, 'a')
    for one_php_train_file_opcode_list in all_php_train_files_opcode_list:
        one_php_train_file_opcode_str = " ".join(one_php_train_file_opcode_list)
        f.write(one_php_train_file_opcode_str)
        f.write('\n')
    f.close()
    # test opcode
    f = open(all_php_test_opcode, 'a')
    for one_php_test_file_opcode_list in all_php_test_files_opcode_list:
        one_php_test_file_opcode_str = " ".join(one_php_test_file_opcode_list)
        f.write(one_php_test_file_opcode_str)
        f.write('\n')
    f.close()
    # train tags
    f = open(all_php_train_tags, 'a')
    for php_train_tag in all_php_train_tags_list:
        f.write(str(php_train_tag))
        f.write("\n")
    f.close()
    # test tags
    f = open(all_php_test_tags, 'a')
    for php_test_tag in all_php_test_tags_list:
        f.write(str(php_test_tag))
        f.write("\n")
    f.close()

    return all_php_train_files_opcode_list, all_php_train_tags_list, all_php_test_files_opcode_list, all_php_test_tags_list
