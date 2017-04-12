import numpy as np
import random
import gym
import tensorflow as tf
from collections import deque


ENV_NAME = 'CartPole-v0'
EPISODE = 10000  # Episode limitation
STEP = 300  # Step limitation in an episode


class DQN(object):

    """A DQN testing and learning class"""

    def __init__(self, env, mem=1000, phimem=4, skip_frame=0):
        self.env = env
        self.mem = mem
        self.phimem = phimem
        self.phi_state = deque()
        self.skip_frame = skip_frame
        self.state = self.env.reset()
        self.sess = tf.InteractiveSession()
        self.experience_pool = deque()
        self.n_state = self.env.observation_space.shape[0] * self.phimem
        self.n_act = self.env.action_space.n
        self._create_net(40)

    def _create_net(self, hidden_size=20):
        # Creating Q net
        self._xq = tf.placeholder(tf.float32, shape=[None, self.n_state], name='x')
        self._y_q = tf.placeholder(tf.float32, shape=[None, self.n_act])
        self._weightsq = [
            tf.Variable(tf.random_normal([self.n_state, hidden_size], stddev=0.1)),
            tf.Variable(tf.random_normal([hidden_size, self.n_act], stddev=0.1))]
        self._biasesq = [
            tf.Variable(tf.constant(0.1, shape=[hidden_size])),
            tf.Variable(tf.constant(0.1, shape=[self.n_act]))]

        self.lq = tf.nn.relu(tf.add(tf.matmul(self._xq, self._weightsq[0]), self._biasesq[0]))
        self.q = tf.add(tf.matmul(self.lq, self._weightsq[1]), self._biasesq[1])

        # Creating Q* net
        self._x = tf.placeholder(tf.float32, shape=[None, self.n_state], name='x')
        self._y_q_ = tf.placeholder(tf.float32, shape=[None, self.n_act])
        self._weightsq_ = [
            tf.Variable(tf.random_normal([self.n_state, hidden_size], stddev=0.1)),
            tf.Variable(tf.random_normal([hidden_size, self.n_act], stddev=0.1))]
        self._biasesq_ = [
            tf.Variable(tf.constant(0.1, shape=[hidden_size])),
            tf.Variable(tf.constant(0.1, shape=[self.n_act]))]

        self.lq_ = tf.nn.relu(tf.add(tf.matmul(self._x, self._weightsq_[0]), self._biasesq_[0]))
        self.q_ = tf.add(tf.matmul(self.lq_, self._weightsq_[1]), self._biasesq_[1])

        #Loss
        self.y = tf.placeholder(tf.float32, [None, self.n_act])
        self.loss = tf.square(self.y - self.q)
        self.optimizer = tf.train.RMSPropOptimizer(0.01,
                                                   momentum=0.1,
                                                   use_locking=True,
                                                   centered=True).minimize(self.loss)

        # Initialize
        tf.global_variables_initializer().run()
        self.sync_theta()

    def sync_theta(self):
        for i in range(2):
            self._biasesq_[i] = self._biasesq[i]
            self._weightsq_[i] = self._weightsq[i]

    def phi(self, state=None, reset=False):
        if reset:
            self.phi_state = deque()
            return
        if not state:
            state = list(self.state)
        if np.shape(self.phi_state)[0] < self.phimem:
            self.phi_state = deque([state] * (self.phimem - np.shape(self.phi_state)[0]))
        else:
            self.phi_state.appendleft(state)
            self.phi_state.pop()
        ret = []
        for i in self.phi_state:
            ret.extend(i)
        return np.mat(ret)

    def play(self, epsilon=0.05):
        if np.random.rand() <= epsilon:
            act = np.random.randint(0, self.n_act)
        else:
            state = self.phi()
            result = list(self.q.eval(feed_dict={self._xq: state}))
            act = result.index(max(result))
        return self.env.step(act), act

    def train(self, gamma=0.9, EPISODE=5000, STEP=5000, minibatch=32, C=10):
        c = 0
        epsilon = 1
        for episode in range(EPISODE):
            self.state = self.env.reset()
            self.phi(reset=True)
            state = self.phi()
            total_reward = 0
            total_state = []

            for t in range(STEP):
                (self.state, reward, done, _), act = self.play(epsilon)
                #reward = 0 if done else 0.1
                total_reward += reward

                state1 = self.phi()
                total_state.append([state, reward, act, state1])
                print(act, end=' ')
                self.env.render()
                if len(self.experience_pool) > self.mem:
                    epsilon = epsilon - 0.001 if epsilon > 0.95 else 0.05
                while len(self.experience_pool) > self.mem:
                    self.experience_pool.pop()
                state = state1

                if done:
                    for index, content in enumerate(total_state):
                        total_state[index][1] = total_reward
                    total_state[-1][1] = 0
                    self.experience_pool.extendleft(total_state)
                    print(epsilon)
                    for i in range(200):
                        #Replay the experience
                        if len(self.experience_pool) >= self.mem:
                            training_set = random.sample(self.experience_pool, minibatch)
                            phi0 = np.vstack(i[0] for i in training_set)
                            phi1 = np.vstack(i[-1] for i in training_set)
                            r = np.mat([i[1] for i in training_set]).T
                            y = r + gamma * self.q_.eval(feed_dict={self._x: phi1})
                            self.optimizer.run(feed_dict={self._xq: phi0, self.y: y})
                            c += 1
                            if c > C:
                                self.sync_theta()
                    break

def main():
    env = gym.make(ENV_NAME)
    agent = DQN(env)
    print(agent._xq.get_shape())
    agent.train()
    print(len(agent.phi_state))
    print(len(agent.phi()))
    for i in range(1000):
        agent.play(epsilon=0)
    return agent


if __name__ == '__main__':
    agent = main()
