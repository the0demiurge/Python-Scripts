#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""capsulate of tensorflow, to realize autoencoder

1. load_examples(name) - load example datasets from tensorflow
2. Interferce() - build the graph including encoder and decoder
@author: xcc
@email: the0demiurge@gmail.com
"""
import tensorflow as tf
#from pylab import *
 

def load_examples(name)
"""load example datasets from tensorflow
Args:
    name: the dataset name

Returns:
    dataset
"""
    if name is 'mnist':
        from tensorflow.examples.tutorials.mnist import input_data
        return input_data.read_data_sets("MNIST_data/", one_hot=True)


class Interferece():
"""build the graph including encoder and decoder

"""
    def coding(net_size, name='layer', activition_function=tf.nn.sigmoid):
    """
    """
        with tf.name_scope('encoder ' + name) as scope:
            W = tf.Variable(tf.truncated_normal(net_size, 
            stddev=1.0 / math.sqrt(float(net_size[0])), 
            name='weights')
