# -*- coding: utf-8 -*-

import numpy as np

train_samples = np.load('npyfile/hidden_layer_out_save2.npy')
train_targets = np.load('npyfile/train_targets.npy')

num_of_samples = len(train_samples)
eta = 0.5
i2h_weights = 2 * np.random.random((90+1, 60)) - 1
h2o_weights = 2 * np.random.random((60+1, 36)) - 1
input_layer_out = np.c_[train_samples, np.array(([1.0] * (train_samples.shape)[0]))]
for k in range(100):
    for i in range(num_of_samples):
        hidden_layer_out = 1 / (1 + np.exp(-(np.dot(input_layer_out[i], i2h_weights))))
        hidden_layer_out_plus1bias = np.r_[np.vstack(hidden_layer_out), np.vstack([1.0])]
        output_layer_out = 1 / (1 + np.exp(-(np.dot(hidden_layer_out_plus1bias.T, h2o_weights))))
        
        output_layer_delta = (train_targets[i] - output_layer_out) * (output_layer_out * (1 - output_layer_out))
        hidden_layer_delta = output_layer_delta.dot(h2o_weights.T) * (hidden_layer_out_plus1bias * (1 - hidden_layer_out_plus1bias)).T
        h2o_weights += eta * hidden_layer_out_plus1bias.dot(output_layer_delta)
        i2h_weights += eta * (np.vstack(input_layer_out[i])).dot((hidden_layer_delta.T[0:60]).T)

    correct_prediction_sum = 0.0
    for i in range(num_of_samples):
        hidden_layer_out = 1 / (1 + np.exp(-(np.dot((np.r_[np.vstack(train_samples[i]), np.vstack([1.0])]).T, i2h_weights))))
        output_layer_out = 1 / (1 + np.exp(-(np.dot(np.c_[hidden_layer_out, np.vstack([1.0])], h2o_weights))))
        result = np.hstack(output_layer_out)
        index1 = np.argmax(result, axis=0)
        index2 = np.argmax(train_targets[i], axis=0)
        correct_prediction_sum += np.equal(index1, index2)

    print k + 1, '--->', correct_prediction_sum / num_of_samples  * 100, '%'
    
#下面这种训练方式不对，在一轮计算完所有样本所需权值修改量后一次性修改权值根本达不到适应所有样本的目的，应该边修改权值边训练下一个样本
#for k in range(10000):
#    hidden_layer_out = 1 / (1 + np.exp(-(np.dot(input_layer_out, i2h_weights))))
#    hidden_layer_out_plus1bias = np.c_[hidden_layer_out, np.array(([1.0] * (train_samples.shape)[0]))]
#    output_layer_out = 1 / (1 + np.exp(-(np.dot(hidden_layer_out_plus1bias, h2o_weights))))
#    
#    output_layer_delta = (train_targets - output_layer_out) * (output_layer_out * (1-output_layer_out))
#    hidden_layer_delta = output_layer_delta.dot(h2o_weights.T) * (hidden_layer_out_plus1bias * (1 - hidden_layer_out_plus1bias))
#    h2o_weights += eta * hidden_layer_out_plus1bias.T.dot(output_layer_delta)
#    i2h_weights += eta * input_layer_out.T.dot((hidden_layer_delta.T[0:60]).T)


correct_prediction_sum = 0.0
for i in range(len(train_samples)):
    inputs = train_samples[i]
    targets = train_targets[i]
    hidden_layer_out = 1/(1+np.exp(-(np.dot((np.r_[np.vstack(train_samples[i]), np.vstack([1.0])]).T, i2h_weights))))
    output_layer_out = 1/(1+np.exp(-(np.dot(np.c_[hidden_layer_out, np.vstack([1.0])], h2o_weights))))

    result = np.hstack(output_layer_out)
    index1 = np.argmax(result, axis=0)
    index2 = np.argmax(targets, axis=0)
    correct_prediction_sum += np.equal(index1, index2)

print correct_prediction_sum / len(train_samples)  * 100, '%'

#保存训练后的权值
#输入层到隐藏层
np.save('npyfile/i2h_weights_save3.npy', i2h_weights)
#隐藏层到输出层
np.save('npyfile/h2o_weights_save3.npy', h2o_weights)
