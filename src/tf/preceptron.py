#!/usr/bin/python3
import numpy as np
import tensorflow as tf
from pylab import *

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

W1 = tf.Variable(tf.random_normal([784, 200]))
b1 = tf.Variable(tf.zeros([200]))

W2 = tf.Variable(tf.random_normal([200, 10]))
b2 = tf.Variable(tf.zeros([10]))

y1 = tf.nn.sigmoid(tf.matmul(x, W1) + b1)
y = tf.nn.softmax(tf.matmul(y1, W2) + b2)

cost = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y, 1e-6, 1.0)))

train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    for i in range(5000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    print(sess.run(W1))
    print(sess.run(W2))
    print(sess.run(b1))
    print(sess.run(b2))

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

