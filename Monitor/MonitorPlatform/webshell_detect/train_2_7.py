# coding=utf-8
import commands
import multiprocessing
import os
import re
import sys

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

from php_get_all_opcode import get_all_php_file_opcode, get_php_opcode
from php_word2vec import get_php_opcode_feature_model_by_word2vec, get_php_vectors_by_word2vec
from php_cnn_model import get_php_cnn_model, test_php_cnn_model, php_cnn_model

from jsp_get_all_bytecode import get_all_jsp_file_bytecode
from jsp_word2vec import get_jsp_bytecode_feature_model_by_word2vec
from jsp_cnn_model import get_jsp_cnn_model, test_jsp_cnn_model

from detect_webshell import detect_php_webshell, detect_jsp_webshell


# Sample path
black_php_train_dir = "data/black/php/train/"
black_php_test_dir = "data/black/php/test/"
white_php_train_dir = "data/white/php/train/"
white_php_test_dir = "data/white/php/test/"
black_jsp_train_dir = "data/black/jsp/train/"
black_jsp_test_dir = "data/black/jsp/test/"
white_jsp_train_dir = "data/white/jsp/train/"
white_jsp_test_dir = "data/white/jsp/test/"

# Sample count
black_php_train_count = 0
black_php_test_count = 0
white_php_train_count = 0
white_php_test_count = 0

# PHP path
php_bin = "/usr/bin/php"

# Word2Vec model path
word2vec_model = "Word2Vec.model"

# PHP opcode
php_opcode = 'php-opcode.txt'
all_php_train_opcode = 'php_opcode_tags/all-php-train-opcode.txt'
all_php_test_opcode = 'php_opcode_tags/all-php-test-opcode.txt'
all_php_train_tags = 'php_opcode_tags/all-php-train-tags.txt'
all_php_test_tags = 'php_opcode_tags/all-php-test-tags.txt'


# main func
if __name__ == '__main__':

    if sys.argv[1] == "--train-php":
        print("Train PHP: ")
        max_features = 128
        max_document_length = 160
        print ("max_features=%d max_document_length=%d" % (max_features, max_document_length))

        all_php_train_files_opcode_list, all_php_train_tags_list, all_php_test_files_opcode_list, all_php_test_tags_list = get_all_php_file_opcode()
        all_train_opcode_vector, all_test_opcode_vector = get_php_opcode_feature_model_by_word2vec(all_php_train_files_opcode_list, all_php_test_files_opcode_list)
        get_php_cnn_model(all_train_opcode_vector, all_php_train_tags_list)
        test_php_cnn_model(all_test_opcode_vector, all_php_test_tags_list)

    elif sys.argv[1] == "--train-jsp":
        print("Train JSP: ")
        max_features = 448
        max_document_length = 192
        print ("max_features=%d max_document_length=%d" % (max_features, max_document_length))

        all_jsp_train_files_bytecode_list, all_jsp_train_tags_list, all_jsp_test_files_bytecode_list, all_jsp_test_tags_list = get_all_jsp_file_bytecode()
        all_train_bytecode_vector, all_test_bytecode_vector = get_jsp_bytecode_feature_model_by_word2vec(all_jsp_train_files_bytecode_list, all_jsp_test_files_bytecode_list)
        get_jsp_cnn_model(all_train_bytecode_vector, all_jsp_train_tags_list)
        test_jsp_cnn_model(all_test_bytecode_vector, all_jsp_test_tags_list)

    elif sys.argv[1] == "--detect-php":
        print("Detect php file ", sys.argv[2])
        os.system("cp " + sys.argv[2] + " /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/data/detect_php/")
        path_php = "data/detect_php/"
        detect_php_webshell(path_php)
        os.system("rm /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/data/detect_php/*")

    elif sys.argv[1] == "--detect-jsp":
        print("Detect jsp file " + sys.argv[2])
        os.system("cp " + sys.argv[2] + " /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/data/detect_jsp/")
        path_jsp = "data/detect_jsp/"
        detect_jsp_webshell(path_jsp)
        os.system("rm /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/data/detect_jsp/*")

    else:
        print("Input Error!!!")

    # detect
    # path_php = "data/detect_php/"
    # detect_php_webshell(path_php)


    # all_jsp_train_files_bytecode_list, all_jsp_train_tags_list, all_jsp_test_files_bytecode_list, all_jsp_test_tags_list = get_all_jsp_file_bytecode()
    # all_train_bytecode_vector, all_test_bytecode_vector = get_jsp_bytecode_feature_model_by_word2vec(all_jsp_train_files_bytecode_list,all_jsp_test_files_bytecode_list)
    # get_jsp_cnn_model(all_train_bytecode_vector, all_jsp_train_tags_list)
    # test_jsp_cnn_model(all_test_bytecode_vector, all_jsp_test_tags_list)
    #
    # detect
    # path_jsp = "detect/upload_file/"
    # path_jsp = "data/detect_jsp/"
    # detect_jsp_webshell(path_jsp)
