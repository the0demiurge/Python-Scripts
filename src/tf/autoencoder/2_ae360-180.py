# -*- coding: utf-8 -*-
#利用自编码将360维数据压缩至180维

import tensorflow as tf
import numpy as np
import random
from sklearn import preprocessing

import scipy.io as sio
matfile1 = sio.loadmat('matfile/all_fuzhi_xiangwei_samples.mat')
matfile2 = sio.loadmat('matfile/all_fuzhi_xiangwei_targets.mat')
all_fuzhi_xiangwei_samples = matfile1['all_fuzhi_xiangwei_samples']
all_fuzhi_xiangwei_targets = matfile2['all_fuzhi_xiangwei_targets']
all_samples = all_fuzhi_xiangwei_samples
all_targets = all_fuzhi_xiangwei_targets

#all_samples = np.load('npyfile/all_samples.npy')
#all_targets = np.load('npyfile/all_targets.npy')


#取前1000个点的数据
#train_samples = all_samples[0:1000]
#随机取1000个样本
#random_slice = random.sample(all_samples, 1000)
#train_samples = np.vstack(random_slice)
#将所有样本顺序随机打乱并取前1000对样本
index = range(0, len(all_samples))
random.shuffle(index)
train_samples = []
train_targets = []
for i in range(1000):
    train_samples.append(all_samples[index[i]])
    train_targets.append(all_targets[index[i]])


#用去均值和方差类处理所有数据
scaler = preprocessing.StandardScaler().fit(train_samples)
samples_scaled = scaler.transform(train_samples)
#用缩放类将所有数据缩放到+-1之间
min_max_scaler = preprocessing.MinMaxScaler((-1.0, 1.0))
train_samples_regularized = min_max_scaler.fit_transform(samples_scaled)

#取后1000个样本作为后续的测试集
test_samples = []
test_targets = []
for i in range(len(all_samples) - 1000, len(all_samples)):
    test_samples.append(all_samples[index[i]])
    test_targets.append(all_targets[index[i]])


#以下为tensorflow模型
#定义placeholder
x_ph = tf.placeholder(tf.float32, [None, 360])
y_ph = tf.placeholder(tf.float32, [None, 360])

#定义session
sess = tf.Session()

#计算除输入层外各层的输出
def calc_layer_out(inputs, in_size, out_size, activation_function = None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    thresholds  = tf.Variable(tf.random_normal([1, out_size]))
    #为了让tensorflow默认的tanh函数中exp(-2.0 * x)变为exp(-0.1 * x)的形式，将输入先除以20.0
    wx_minus_t = tf.matmul(inputs / 20.0, weights) - thresholds
    if activation_function is None:
        outputs = wx_minus_t
    else:
        outputs = activation_function(wx_minus_t)
    return outputs, weights, thresholds


#计算输出误差
def calc_error(x, y):
    y_pre = sess.run(output_layer_out, feed_dict = {x_ph: x})
    error = tf.reduce_mean(tf.reduce_sum(tf.abs(y_pre - y), reduction_indices = [1]))
    result = sess.run(error, feed_dict={x_ph: x, y_ph: y})
    return result



#隐藏层输出
hidden_layer_out, i2h_weights, i2h_thresholds = calc_layer_out(x_ph, 360, 180,  activation_function = tf.tanh)

#输出层输出
output_layer_out, h2o_weights, h2o_thresholds = calc_layer_out(hidden_layer_out, 180, 360,  activation_function = tf.tanh)

#代价函数
cost = tf.reduce_mean(tf.reduce_sum(tf.square(y_ph - output_layer_out), reduction_indices = [1]))
#学习率0.5
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cost)

#初始化所有变量
sess.run(tf.initialize_all_variables())

#训练1000轮
for i in range(1000):
    sess.run(train_step, feed_dict = {x_ph: train_samples_regularized, y_ph: train_samples_regularized})
    if i % 10 == 0:
        print(calc_error(train_samples_regularized, train_samples_regularized))


#保存数据用于事后比较
np.save('npyfile/train_samples.npy', train_samples)
np.save('npyfile/output_layer_out_save1.npy', sess.run(output_layer_out, feed_dict = {x_ph: train_samples_regularized, y_ph: train_samples_regularized}))
#与train_samples顺序一一对应为后续训练bp分类使用
np.save('npyfile/train_targets.npy', train_targets)

#保存隐藏层输出作为第二次降维的输入数据
np.save('npyfile/hidden_layer_out_save1.npy', sess.run(hidden_layer_out, feed_dict = {x_ph: train_samples_regularized, y_ph: train_samples_regularized}))

#保存归一化处理和缩放处理的各个因子
np.save('npyfile/scaler_mean.npy', scaler.mean_)
np.save('npyfile/scaler_std.npy', scaler.std_)
#np.save('npyfile/scaler_scale.npy', scaler.scale_)
np.save('npyfile/min_max_scaler_min.npy', min_max_scaler.min_)
np.save('npyfile/min_max_scaler_scale.npy', min_max_scaler.scale_)

#保存训练后的权值和阈值矩阵
#输入层到隐藏层
np.save('npyfile/i2h_weights_save1.npy', sess.run(i2h_weights))
np.save('npyfile/i2h_thresholds_save1.npy', sess.run(i2h_thresholds))
#隐藏层到输出层
np.save('npyfile/h2o_weights_save1.npy', sess.run(h2o_weights))
np.save('npyfile/h2o_thresholds_save1.npy', sess.run(h2o_thresholds))

#保存数据用于后续测试
np.save('npyfile/test_samples.npy', test_samples)
np.save('npyfile/test_targets.npy', test_targets)
