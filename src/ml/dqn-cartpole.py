import numpy as np
import gym
import tensorflow as tf
from collections import deque


ENV_NAME = 'CartPole-v0'
EPISODE = 10000  # Episode limitation
STEP = 300  # Step limitation in an episode


class DQN(object):

    """A DQN testing and learning class"""

    def __init__(self, env, mem=20, phi=4, skip_frame=0):
        self.env = env
        self.mem = mem
        self.phi = phi
        self.skip_frame = skip_frame
        self.state = self.env.reset()
        self.sess = tf.InteractiveSession()
        self.experience_pool = deque()
        self.n_state = self.env.observation_shape.shape[0]
        self.n_act = self.env.action_space.n
        self._create_net(40)

    def _create_net(self, hidden_size):
        #Creating Q net
        self._xq = tf.placeholder(tf.float16, shape=[None, self.n_state], name='x')
        self._y_q = tf.placeholder(tf.float16, shape=[None, self.n_act])
        self._weightsq = [
            tf.Variable(tf.random_normal([self.n_state, hidden_size], stddev=0.1)),
            tf.Variable(tf.random_normal([hidden_size, self.n_act], stddev=0.1))]
        self._biasesq = [
            tf.Variable(tf.constant(0.1, shape=[hidden_size])),
            tf.Variable(tf.constant(0.1, shape=[self.n_act]))]

        self.lq = tf.nn.relu(tf.add(tf.matmul(self._xq, self._weightsq[0]), self._biasesq[0]))
        self.q = tf.add(tf.matmul(self.lq, self._weightsq[1]), self._biasesq[1])

        #Creating Q* net
        self._x = tf.placeholder(tf.float16, shape=[None, self.n_state], name='x')
        self._y_q_ = tf.placeholder(tf.float16, shape=[None, self.n_act])
        self._weightsq_ = [
            tf.Variable(tf.random_normal([self.n_state, hidden_size], stddev=0.1)),
            tf.Variable(tf.random_normal([hidden_size, self.n_act], stddev=0.1))]
        self._biasesq_ = [
            tf.Variable(tf.constant(0.1, shape=[hidden_size])),
            tf.Variable(tf.constant(0.1, shape=[self.n_act]))]

        self.lq_ = tf.nn.relu(tf.add(tf.matmul(self._x, self._weightsq_[0]), self._biasesq_[0]))
        self.q_ = tf.add(tf.matmul(self.lq_, self._weightsq_[1]), self._biasesq_[1])

        #Initialize
        tf.global_variables_initializer().run()
        self.sync_theta()

    def sync_theta(self):
        for i in range(2):
            self._biasesq_[i] = self._biasesq[i]
            self._weightsq_[i] = self._weightsq[i]

    def play(self, act):
        return self.env.step(act)

    def train(self, EPISODE, STEP):
        for episode in EPISODE:




def main():
    env = gym.make(ENV_NAME)
    agent = DQN(env)

    for episode in range(EPISODE):
        pass


if __name__ == '__main__':
    main()
