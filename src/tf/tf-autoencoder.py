#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""capsulate of tensorflow, to realize autoencoder

1. load_examples(name) - load example datasets from tensorflow
2. Interferce() - build the graph including encoder and decoder
@author: xcc
@email: the0demiurge@yahoo.com
"""
import math
from pylab import *
import tensorflow as tf


def load_examples(name):
    """load example datasets from tensorflow
    
    Args:
        name: the dataset name
    
    Returns:
        dataset
    """
    if name is 'mnist':
        from tensorflow.examples.tutorials.mnist import input_data
        return input_data.read_data_sets("MNIST_data/", one_hot=True)


class Interferece:
    """build the graph including encoder and decoder
    
    """





    def layer(self, inputs, net_size, name='', 
               activition_function=tf.nn.tanh):
        """build a layer with variables
        
        Args:
            inputs: placeholder, this layer input
            net_size: 2-dim list, [first, last], indicates layer size
            name: name to show in graph
            activition_function: activition function to use
        
        Returns:
            layer: a tensor, the result
        
        """
        #Encoding
        with tf.name_scope('layer ' + name) as scope:
            W = tf.Variable(
                tf.truncated_normal(net_size,
                stddev=1.0 / math.sqrt(float(net_size[0]))), 
                name='weights')
            b = tf.Variable(tf.zeros([net_size[1]]), name='biases')
            layer = activition_function(tf.matmul(inputs, W) + b)
        return layer






def show_activition_functions(function, border=5.0, is_tensorflow_function=True):
    """showing the diagram of an activition function
    
    Args:
        function: function to diagram
        border: border of the graph
        is_tensorflow_function: weather it is a tensorflow function
    """
    x = linspace(-abs(border), abs(border))
    y = function(x)
    if is_tensorflow_function:
        with tf.Session() as sess:
            y = sess.run(y)
    plot(x, y)
    show()




