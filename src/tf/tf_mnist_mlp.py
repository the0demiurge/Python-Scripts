#!/usr/bin/python3
import numpy as np
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
tmp = []
costss = []
net_size = [784, 500, 200, 10]
x = tf.placeholder(tf.float32, [None, net_size[0]])
y_ = tf.placeholder(tf.float32, [None, net_size[3]])

W1 = tf.Variable(tf.truncated_normal([net_size[0], net_size[1]]))
b1 = tf.Variable(tf.zeros([net_size[1]]))
y1 = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

W2 = tf.Variable(tf.truncated_normal([net_size[1], net_size[2]]))
b2 = tf.Variable(tf.zeros([net_size[2]]))
y2 = tf.nn.sigmoid(tf.matmul(y1, W2) + b2)

W3 = tf.Variable(tf.truncated_normal([net_size[2], net_size[3]]))
b3 = tf.Variable(tf.zeros([net_size[3]]))
y = tf.nn.softmax(tf.matmul(y2, W3) + b3)

cost = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y, 1e-6, 1.0)))
#cost = tf.nn.softmax_cross_entropy_with_logits(y, y_)
#cost = tf.nn.sigmoid_cross_entropy_with_logits(y, y_)

train_step = tf.train.AdamOptimizer(0.0011).minimize(cost)

tf.scalar_summary('cost', cost)

init = tf.initialize_all_variables()

summary_op = tf.merge_all_summaries()


with tf.Session() as sess:
    sess.run(init)
    summary_writer = tf.train.SummaryWriter('.', graph_def = sess.graph)
    for i in range(5000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        _, cost_ = sess.run([train_step, cost], feed_dict={x: batch_xs, y_: batch_ys})
        if i % 10 == 0:
            summary_str = sess.run(summary_op, feed_dict={x: batch_xs, y_: batch_ys})
            summary_writer.add_summary(summary_str, i)

            correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
            tmp.append(accuracy)
            costss.append(cost_)
#    print(sess.run(W1))
#    print(sess.run(W2))
#    print(sess.run(b1))
#    print(sess.run(b2))
