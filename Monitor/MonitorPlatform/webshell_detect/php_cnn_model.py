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

PhpCnnModel = "webshell_detect_cnn_model/php_cnn_model/php-webshell-detect-cnn-model"


def do_metrics(y_test, y_pred):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    confusion = metrics.confusion_matrix(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)

    print("metrics.accuracy_score:" + str(accuracy))
    print("metrics.confusion_matrix:")
    print(str(confusion))
    print("metrics.precision_score:" + str(precision))
    print("metrics.recall_score:" + str(recall))
    print("metrics.f1_score:" + str(f1_score))


# cnn model
def php_cnn_model():
    network = input_data(shape=[None, max_document_length, max_features], name='input')
    branch1 = conv_1d(network, 120, 3, padding='valid', activation='relu', regularizer="L2")  # network filters CNN-core
    branch2 = conv_1d(network, 120, 4, padding='valid', activation='relu', regularizer="L2")
    branch3 = conv_1d(network, 120, 5, padding='valid', activation='relu', regularizer="L2")
    network = merge([branch1, branch2, branch3], mode='concat', axis=1)  # 融合层
    network = tf.expand_dims(network, 2)  # 扩展到二维
    network = global_max_pool(network)  # 池化层
    network = dropout(network, 0.8)  # 损失函数
    network = fully_connected(network, 2, activation='softmax')  # 全连接层 输入层中输出单位数量 激活函数
    network = regression(network, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy',
                         name='target')  # 回归函数 指定优化器adam，学习率为0.01，损失函数为交叉熵
    model = tflearn.DNN(network, tensorboard_verbose=0)  #
    return model


# def cnn_word2vec(opcode_vector,all_tags):
def get_php_cnn_model(train_opcode, train_tags):
    global max_document_length
    print("Start train CNN model:")
    """
    f = open('metrics.txt', 'a')
    f.write("CNN: \n")
    f.close()
    """
    # trainX, testX, trainY, testY = train_test_split(x, y, test_size=0.4, random_state=0)
    # y_test = testY

    # Converting labels to binary vectors
    train_tags = to_categorical(train_tags, nb_classes=2)
    # test_tags = to_categorical(test_tags, nb_classes=2)

    # Building convolutional network
    model = php_cnn_model()

    # Train Start

    model.fit(train_opcode, train_tags, n_epoch=10, shuffle=True, validation_set=0.1, show_metric=True, batch_size=100,
              run_id="php-webshell-datect-cnn")  # 训练迭代次数5  shuffle布尔值是否在每轮迭代之前混洗数据   作验证集的训练数据的比例0.1-模型将分出一部分不会被训练的验证数据，并将在每一轮结束时评估这些验证数据的误差和任何其他模型指标   batch_size-每次梯度更新的样本数
    print("CNN training is over!!!")
    model.save(PhpCnnModel)


# test CNN model
def test_php_cnn_model(test_opcode, test_tags):
    print("Start test CNN model:")
    with tf.Graph().as_default():
        new_model = php_cnn_model()
        new_model.load(PhpCnnModel)
        model1 = new_model
    predict_tags_list = model1.predict(test_opcode)
    predict_tags = []
    for i in predict_tags_list:
        if i[0] > 0.5:
            predict_tags.append(0)
            print(i, "white")
        else:
            predict_tags.append(1)
            print(i, "black")
    print("CNN model test is over!")
    do_metrics(test_tags, predict_tags)
