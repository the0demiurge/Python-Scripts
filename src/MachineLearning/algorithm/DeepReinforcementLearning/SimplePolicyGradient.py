#!/usr/bin/env python3
import gym
import tensorflow as tf
import numpy as np
from tensorflow.contrib import slim
from ReplayBuffer import ReplayBuffer

env = gym.make('CartPole-v0')
env.reset()

buf = ReplayBuffer(5000)
x = tf.placeholder(tf.float32, [None, 4], name='x')
a = tf.placeholder(tf.float32, [None, 2], name='a')
r = tf.placeholder(tf.float32, [None, 1], name='r')


def build_net(x, a, r):
    h1 = slim.layers.fully_connected(x, 20)
    h2 = slim.layers.fully_connected(h1, 12)
    h3 = slim.layers.fully_connected(h2, 2, activation_fn=tf.identity)
    y = tf.nn.softmax(h3)
    logp = tf.log(y)

    # good_probabilities = tf.reduce_sum(tf.multiply(y, a), reduction_indices=[1])
    # # maximize the log probability
    # log_probabilities = tf.log(good_probabilities)
    # loss = -tf.reduce_sum(log_probabilities)

    loss = -tf.reduce_sum(
        tf.reduce_sum(
            tf.multiply(tf.multiply(r, logp), a),
            reduction_indices=[1]))
    return y, logp, h3, loss


y, logp, h, loss = build_net(x, a, r)

optimizer = tf.train.RMSPropOptimizer(0.001).minimize(loss)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
buf.clear()


def get_act(feed_dict):
    act = sess.run(y, feed_dict=feed_dict)
    if np.random.uniform() <= act[0][0]:
        return np.array([1, 0])
    else:
        return np.array([0, 1])


render_close = True
for i in range(40000):
    if i > 4000:
        render_close = False
    s = env.reset()
    total_reward = 0
    done = False

    bbuf = list()
    while not done:
        # 重复试验收集数据
        act = get_act({x: np.reshape(s, [1, 4])})
        s_next, reward, done, _ = env.step(act[1])
        total_reward += reward
        bbuf.append([s, act, total_reward, s_next])
        env.render(close=render_close)
        s = s_next
    else:
        for j in bbuf:
            j[2] = total_reward
        buf.extend(bbuf)
    if i % 150 == 140:
        for i in range(4000):
            # 使用收集到的数据训练网络
            st, at, rt, sn = zip(*buf.sample())
            rt = np.reshape(np.array(rt), [-1, 1])
            # rt 中心标准化
            rt_norm = (rt - min(rt)) / (np.sqrt(np.var(rt)) + 1)
            feed_dict = {
                x: np.array(st),
                a: np.array(at),
                r: rt_norm
            }
            loss_runned, y_runned, _ = sess.run([loss, y, optimizer], feed_dict=feed_dict)
            print('loss: ', loss_runned, 'y', y_runned[0])

