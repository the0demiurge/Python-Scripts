#!/bin/python3.5
'''
tensorflow autoencoder
for MNIST data
xcc
'''
import numpy as np
import tensorflow as tf
#import sklearn
#from sklearn import preprocessing as pss
import matplotlib.pyplot as plt
import matplotlib
#preprocessing
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets('/home/ash/Downloads/MNIST_data',one_hot=True)
#Parameters
learning_rate = 0.01
training_epochs=20
batch_size=256
examples_to_show=10
strut_net=[784,256,128]
n=len(strut_net)

def layer(x,w,b):
    lay=tf.nn.sigmoid(tf.add(tf.matmul(x,w),b))
    return lay
    
w1=[tf.Variable('float',[strut_net[i],strut_net[i+1]]) for i in range(n-1)]


    




