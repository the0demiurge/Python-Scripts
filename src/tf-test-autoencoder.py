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

