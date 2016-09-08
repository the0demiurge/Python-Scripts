# -*- coding: utf-8 -*-
#利用自编码将180维数据压缩至90维

import tensorflow as tf
import numpy as np

all_samples = np.load('npyfile/hidden_layer_out_save1.npy')
train_samples = all_samples


#以下为tensorflow模型
#定义placeholder
x_ph = tf.placeholder(tf.float32, [None, 180])
y_ph = tf.placeholder(tf.float32, [None, 180])

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
hidden_layer_out, i2h_weights, i2h_thresholds = calc_layer_out(x_ph, 180, 90,  activation_function = tf.tanh)

#输出层输出
output_layer_out, h2o_weights, h2o_thresholds = calc_layer_out(hidden_layer_out, 90, 180,  activation_function = tf.tanh)

#代价函数
cost = tf.reduce_mean(tf.reduce_sum(tf.square(y_ph - output_layer_out), reduction_indices = [1]))
#学习率0.5
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cost)

#初始化所有变量
sess.run(tf.initialize_all_variables())

#训练1000轮
for i in range(1000):
    sess.run(train_step, feed_dict = {x_ph: train_samples, y_ph: train_samples})
    if i % 10 == 0:
        print(calc_error(train_samples, train_samples))


#保存数据用于事后比较
np.save('npyfile/output_layer_out_save2.npy', sess.run(output_layer_out, feed_dict = {x_ph: train_samples, y_ph: train_samples}))

#保存隐藏层输出作为训练分类网络的输入数据
np.save('npyfile/hidden_layer_out_save2.npy', sess.run(hidden_layer_out, feed_dict = {x_ph: train_samples, y_ph: train_samples}))

#保存训练后的权值和阈值矩阵
#输入层到隐藏层
np.save('npyfile/i2h_weights_save2.npy', sess.run(i2h_weights))
np.save('npyfile/i2h_thresholds_save2.npy', sess.run(i2h_thresholds))
#隐藏层到输出层
np.save('npyfile/h2o_weights_save2.npy', sess.run(h2o_weights))
np.save('npyfile/h2o_thresholds_save2.npy', sess.run(h2o_thresholds))
