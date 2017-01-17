#!/usr/bin/env python3
import tensorflow as tf
from tensorflow.examples.tutorials import mnist

data = mnist.input_data.read_data_sets('MNIST_data/', one_hot=True)
# making layers
"we finally reached the goal that talk with each other with English.. . haha"


def relu_layer(bef, size):
    w = tf.Variable(tf.random_normal(size, stddev=.1, dtype=tf.float16))
    b = tf.Variable(.1 * tf.ones(size[-1], dtype=tf.float16))
    return tf.nn.relu(tf.add(tf.matmul(bef, w), b))


def linear_layer(bef, size):
    w = tf.Variable(tf.random_normal(size, stddev=.1, dtype=tf.float16))
    b = tf.Variable(tf.zeros(size[-1], dtype=tf.float16))
    return tf.add(tf.matmul(bef, w), b)


graph = tf.Graph()
graph.as_default()

# defining layers including weights and biases, and assigning it to cpus, gpus
with tf.device('/cpu:0'):
    x = tf.placeholder(tf.float16, [None, 784])
    y_ = tf.placeholder(tf.float16, [None, 10])

# first layer uses most calculating resources
with tf.device('/gpu:0'):
    l1 = relu_layer(x, [784, 500])

# assigning gpu:0 and gpu:1 to one network, cuz they can communite with each other, and DO NOT USE /gpu:1 and /gpu:2
with tf.device('/gpu:1'):
    # l2 = relu_layer(l1, [500, 800])
    l3 = relu_layer(l1, [500, 200])
    l4 = linear_layer(l3, [200, 10])
    y = tf.nn.softmax(l4)

    cost = tf.nn.softmax_cross_entropy_with_logits(l4, y_)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float16))

step = tf.train.RMSPropOptimizer(7e-6).minimize(cost)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

for i in range(20000):
    batch = data.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1]})
        print("step %d, training accuracy %g" % (i, train_accuracy))
    step.run(feed_dict={x: batch[0], y_: batch[1]})

print("test accuracy %g" % accuracy.eval(feed_dict={x: data.test.images, y_: mnist.test.labels}))
