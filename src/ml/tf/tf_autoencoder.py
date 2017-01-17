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


def placeholders(x_size, y_size):
    x = tf.placeholder(tf.float32, shape=[None, x_size], name='input')
    y = tf.placeholder(tf.float32, shape=[None, y_size], name='target')
    return x, y


class Interferece:
    """build the graph including encoder and decoder



    """
    @staticmethod
    def full_connect(inputs, net_size, name='',
                     activition_function=tf.nn.tanh):
        """build a layer with variables

        Args:
            inputs: tensor, this layer input
            net_size: 2-dim list, [first, last], indicates layer size
            name: name to show in graph
            activition_function: activition function to use

        Returns:
            layer: a tensor, the result

        """
        with tf.name_scope('full_connect ' + name) as scope:
            W = tf.Variable(tf.truncated_normal(
                net_size, stddev=1.0 / math.sqrt(float(net_size[0]))),
                name='weights')
            b = tf.Variable(tf.zeros([net_size[1]]), name='biases')
            layer = activition_function(tf.matmul(inputs, W) + b)
        return layer

    def encoder_decoder(self, inputs, net_shape, name='',
                        activition_function=tf.nn.tanh):
        """builds encoder and decoder layer

        Args:
            inputs: tensor, this layer input
            net_shape: 2-dim list, [first, last], indicates layer size
            name: name to show in graph
            activition_function: activition function to use

        Returns:
            encoder: a tensor, the result
            decoder: a tensor, to train the network unsupervisedly

        """
        encoder = self.full_connect(inputs, net_shape, name='encoder '+name,
                                    activition_function=activition_function)
        net_shape.reverse()
        decoder = self.full_connect(encoder, net_shape,
                                    name='decoder '+name,
                                    activition_function=activition_function)
        return encoder, decoder


class cost:
    @staticmethod
    def cross_entropy(logits, labels):
        return -tf.reduce_sum(labels * tf.log(
               tf.clip_by_value(logits, 1e-6, 1.0)))

    @staticmethod
    def squared_error(target, predict):
        return tf.reduce_mean(tf.pow(target - predict, 2))


def training(loss, learning_rate, method=tf.train.AdamOptimizer,
             name='loss'):
    """sets up the training ops
    """
    tf.scalar_summary(name, loss)
    optimizer = method(learning_rate)
    # Create a variable to track the global step.
    global_step = tf.Variable(0, name='global_step', trainable=False)
    # Use the optimizer to apply the gradients that minimize the loss
    # (and also increment the global step counter) as a single training step.
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op


def show_activition_functions(function, border=5.0,
                              is_tensorflow_function=True):
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