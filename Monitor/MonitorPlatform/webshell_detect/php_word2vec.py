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
max_document_length = 160  # The opcode/opcode length of the sample file
min_code_count = 0  # The min opcode/opcode length of sample file

# Word2Vec model path
word2vec_model = "word2vec_mode/PHP_Word2Vec.model"


# get opcode vectors by word2vec
def get_php_vectors_by_word2vec(model, corpus):
    global max_document_length

    all_vectors = []
    embedding_dim = model.vector_size  # 模型维度
    embedding_unknown = [0. for i in range(embedding_dim)]
    # 逐句
    """
    for i in model.wv.vocab:
        print(i)
    for text in corpus:
        text = text[:5]
        print(text)
        print(type(text))
        """
    for text in corpus:
        this_vector = []
        # 切除掉最大文档长度后的词
        text = text[:max_document_length]
        # 逐词
        for i, word in enumerate(text):  # 遍历text
            if word in model.wv.vocab:  # model.wv.vocab 训练后model中的所有词
                this_vector.append(model[word])  # 向列表this_vector[]中添加词向量
            else:
                this_vector.append(embedding_unknown)  # 若不存在则补0向量
        dim = np.shape(this_vector)  # 获取矩阵维度(a,b)
        # 不足长度的填充至一致长度
        if dim[0] < max_document_length:
            pad_length = max_document_length - i - 1
            for n in range(0, pad_length):
                this_vector.append(embedding_unknown)
        all_vectors.append(this_vector)
    # print(model.wv.vocab)
    # print(all_vectors)

    opcode_vector = np.array(all_vectors)
    return opcode_vector


# Train word2vec model
def get_php_opcode_feature_model_by_word2vec(all_php_train_files_opcode_list, all_php_test_files_opcode_list):
    global max_document_length

    # x, y = get_all_file_opcode()
    cores = multiprocessing.cpu_count()
    print("CPU cores: %d." % cores)
    print("Start train Word2vec model:")
    # List the php opcodes that need to be word vectorized
    """
    opcode = []
    f = open(php_opcode)
    for line in f:
        opcode.append(line.strip('\n'))
    f.close()
    # print(opcode)
    """
    # Create and train the word2vec model
    if os.path.exists(word2vec_model):
        print("Find %s!" % word2vec_model)
        model = gensim.models.Word2Vec.load(word2vec_model)
    else:
        model = gensim.models.Word2Vec(sg=0, size=max_features, window=5, min_count=5, iter=10, workers=cores)
        # all_php_files_opcode_list = all_php_train_files_opcode_list + all_php_test_files_opcode_list
        model.build_vocab(all_php_train_files_opcode_list)
        model.train(all_php_train_files_opcode_list, total_examples=model.corpus_count, epochs=model.iter)
        model.save(word2vec_model)
        print("%s generated successfully!" % word2vec_model)
        # print(all_files_opcode_list)

    train_opcode_vector = get_php_vectors_by_word2vec(model, all_php_train_files_opcode_list)
    test_opcode_vector = get_php_vectors_by_word2vec(model, all_php_test_files_opcode_list)
    return train_opcode_vector, test_opcode_vector