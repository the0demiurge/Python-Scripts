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
        self.mem = men
        self.phi = phi
        self.skip_frame = skip_frame
        self.state = self.env.reset()
        self.sess = tf.InteractiveSession()
        self.experience_pool = deque()
        self.n_state = self.env.observation_shape.shape[0]
        self.n_act = self.env.action_space.n

    def _create_net(self):
        self._x = tf.placeholder(tf.float16, shape=[None, self.n_state], name='x')
        self._y_ = tf.placeholder(tf.float16, shape=[None, self.n_act])
        self._weights = [tf.Variable(tf.random_normal)]


def main():
    env = gym.make(ENV_NAME)
    agent = DQN(env)

    for episode in range(EPISODE):
        pass

if __name__ == '__main__':
    main()
