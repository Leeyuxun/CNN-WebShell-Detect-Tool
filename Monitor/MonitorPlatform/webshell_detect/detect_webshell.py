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

from php_get_all_opcode import get_all_php_file_opcode, get_php_opcode
from php_word2vec import get_php_opcode_feature_model_by_word2vec, get_php_vectors_by_word2vec
from php_cnn_model import get_php_cnn_model, test_php_cnn_model, php_cnn_model

from jsp_get_all_bytecode import get_all_jsp_file_bytecode, get_jsp_bytecode, compile_jsp_to_class
from jsp_word2vec import get_jsp_bytecode_feature_model_by_word2vec, get_jsp_vectors_by_word2vec
from jsp_cnn_model import get_jsp_cnn_model, test_jsp_cnn_model, jsp_cnn_model

class_file_dir = "/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class/"
php_word2vec_mode = "/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/word2vec_mode/PHP_Word2Vec.model"
php_webshell_detect_cnn_model = "/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/webshell_detect_cnn_model/php_cnn_model/php-webshell-detect-cnn-model"
jsp_word2vec_mode = "/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/word2vec_mode/JSP_Word2Vec.model"
jsp_webshell_detect_cnn_model = "/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/webshell_detect_cnn_model/jsp_cnn_model/jsp-webshell-detect-cnn-model"


# PHP
def detect_php_webshell(filepath):

    opcode_list = get_php_opcode(filepath)
    model = gensim.models.Word2Vec.load(php_word2vec_mode)
    opcode_vectors = get_php_vectors_by_word2vec(model, opcode_list)
    # print(opcode_vectors)
    with tf.Graph().as_default():
        new_model = php_cnn_model()
        new_model.load(php_webshell_detect_cnn_model)
        model1 = new_model

    predict_tags_list = model1.predict(opcode_vectors)
    for i in predict_tags_list:
        if i[0] > 0.5:
            print(i, "white")
            return 1
        else:
            print(i, "black")
            return 0


# JSP
def detect_jsp_webshell(filepath):
    # compile jsp to class file
    compile_jsp_to_class(filepath)
    # get jsp bytecode
    bytecode_list = get_jsp_bytecode(class_file_dir)
    for path, dirs, fileList in os.walk(class_file_dir):
        for file_name in fileList:
            file_path = os.path.join(path, file_name)
            cmd = "rm " + file_path
            os.system(cmd)

    model = gensim.models.Word2Vec.load(jsp_word2vec_mode)
    bytecode_vectors = get_jsp_vectors_by_word2vec(model, bytecode_list)
    with tf.Graph().as_default():
        new_model = jsp_cnn_model()
        new_model.load(jsp_webshell_detect_cnn_model)
        jsp_model = new_model

    predict_tags_list = jsp_model.predict(bytecode_vectors)
    for i in predict_tags_list:
        if i[0] > 0.5:
            print(i, "white")
            return 1
        else:
            print(i, "black")
            return 0


if __name__ == '__main__':
    filepath = '/home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/upload_file/'
    os.system('rm -rf /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class/')
    os.system('mkdir /home/gp/Desktop/Monitor/MonitorPlatform/webshell_detect/detect/jsp_class/')
    for path, dirs, fileList in os.walk(filepath):
        for file_name in fileList:
            if file_name.endswith('.php'):
                result = detect_php_webshell(filepath)
            elif file_name.endswith('.jsp'):
                result = detect_jsp_webshell(filepath)
    print(result)
