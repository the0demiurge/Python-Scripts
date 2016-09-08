# -*- coding: utf-8 -*-

import numpy as np
from sklearn import preprocessing


test_samples = np.load('npyfile/test_samples.npy')
test_targets = np.load('npyfile/test_targets.npy')

scaler_mean = np.load('npyfile/scaler_mean.npy')
scaler_std = np.load('npyfile/scaler_std.npy')
min_max_scaler_min = np.load('npyfile/min_max_scaler_min.npy')
min_max_scaler_scale = np.load('npyfile/min_max_scaler_scale.npy')

i2h_weights_save1 = np.load('npyfile/i2h_weights_save1.npy')
i2h_thresholds_save1 = np.load('npyfile/i2h_thresholds_save1.npy')
h2o_weights_save1 = np.load('npyfile/h2o_weights_save1.npy')
h2o_thresholds_save1 = np.load('npyfile/h2o_thresholds_save1.npy')

i2h_weights_save2 = np.load('npyfile/i2h_weights_save2.npy')
i2h_thresholds_save2 = np.load('npyfile/i2h_thresholds_save2.npy')
h2o_weights_save2 = np.load('npyfile/h2o_weights_save2.npy')
h2o_thresholds_save2 = np.load('npyfile/h2o_thresholds_save2.npy')

i2h_weights_save3 = np.load('npyfile/i2h_weights_save3.npy')
h2o_weights_save3 = np.load('npyfile/h2o_weights_save3.npy')


#用去均值和方差类处理所有数据
scaler = preprocessing.StandardScaler()
scaler.mean_ = scaler_mean
scaler.std_ = scaler_std
samples_scaled = scaler.transform(test_samples)
#用缩放类将所有数据缩放到+-1之间
min_max_scaler = preprocessing.MinMaxScaler((-1.0, 1.0))
min_max_scaler.min_ = min_max_scaler_min
min_max_scaler.scale_ = min_max_scaler_scale
test_samples_regularized = min_max_scaler.fit_transform(samples_scaled)

hidden_out_real1 = []
for i in range(len(test_samples_regularized)):
    one_sample = test_samples_regularized[i]
    one_sample = np.vstack(one_sample)
    temp1 = one_sample / 20.0 * i2h_weights_save1
    temp11 = temp1.sum(axis = 0)
    temp11 = temp11 - i2h_thresholds_save1
    temp11 = np.hstack(temp11)
    hidden_out = np.zeros(temp11.shape)
    for i in range(len(temp11)):
        hidden_out[i] = 2.0 / (1.0 + np.exp(-2.0 * temp11[i])) - 1
    hidden_out_real1.append(hidden_out)

hidden_out_real1 = np.vstack(hidden_out_real1)


hidden_out_real2 = []
for i in range(len(hidden_out_real1)):
    one_sample = hidden_out_real1[i]
    one_sample = np.vstack(one_sample)
    temp1 = one_sample / 20.0 * i2h_weights_save2
    temp11 = temp1.sum(axis = 0)
    temp11 = temp11 - i2h_thresholds_save2
    temp11 = np.hstack(temp11)
    hidden_out = np.zeros(temp11.shape)
    for i in range(len(temp11)):
        hidden_out[i] = 2.0 / (1.0 + np.exp(-2.0 * temp11[i])) - 1
    hidden_out_real2.append(hidden_out)

hidden_out_real2 = np.vstack(hidden_out_real2)


correct_prediction_sum = 0.0
for i in range(len(hidden_out_real2)):
    inputs = hidden_out_real2[i]
    targets = test_targets[i]
    hidden_layer_out = 1/(1+np.exp(-(np.dot((np.r_[np.vstack(hidden_out_real2[i]), np.vstack([1.0])]).T, i2h_weights_save3))))
    output_layer_out = 1/(1+np.exp(-(np.dot(np.c_[hidden_layer_out, np.vstack([1.0])], h2o_weights_save3))))

    result = np.hstack(output_layer_out)
    index1 = np.argmax(result, axis=0)
    index2 = np.argmax(targets, axis=0)
    correct_prediction_sum += np.equal(index1, index2)

print correct_prediction_sum / len(hidden_out_real2)  * 100, '%'
