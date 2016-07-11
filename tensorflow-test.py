#!/bin/python3.5
'''
tensorflow autoencoder
for CSI data
xcc
'''
import numpy as np
import tensorflow as tf
#import sklearn
from sklearn import preprocessing as pss
#preprocessing
sample=np.load('/home/ash/Downloads/proj/allsample.npy')
target=np.load('/home/ash/Downloads/proj/alltarget.npy')
input=pss.scale(sample)

