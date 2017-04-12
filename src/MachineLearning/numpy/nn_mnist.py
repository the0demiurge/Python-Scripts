"""这个代码还有小问题，不过不想整了
问题1：里面不该用numpy array，而是应该用mat，否则计算结果有些地方会很令人困惑
问题2：反向传播好像有地方写的不对，如果有隐含层就会不收敛
问题3：梯度消失，一直没有解决
"""
import pdb
from pylab import *
from tensorflow.examples.tutorials import mnist

data = mnist.input_data.read_data_sets('MNIST_data', one_hot=True)


def show_pic(image_data, index):
    if len(image_data.shape) == 2:
        imshow(reshape(image_data[index, :], [28, 28]))
    elif len(image_data.shape) == 1:
        imshow(reshape(image_data, [28, 28]))
    elif len(image_data.shape) == 3:
        imshow(image_data[index, :, :])


class mnist_net(object):

    def __init__(self, shape, data):
        self.data = data
        self.shape = shape
        self.weights = [0.1 * randn(a, b) for a, b in zip(shape[:-1], shape[1:])]
        self.biases = [zeros([1, a]) for a in shape[1:]]

    def sigmoid(self, z, derivative=False):
        sig = 1 / (1 + exp(-z))
        if not derivative:
            return sig
        else:
            return sig * (1 - sig)

    def fp(self, inputs):
        ai = inputs
        self.z = []
        self.a = []
        for w, b in zip(self.weights, self.biases):
            self.a.append(ai)
            zi = ai.dot(w) + b
            self.z.append(zi)
            ai = self.sigmoid(zi)
        return ai

    def bp_step(self, batch=1, learning_rate=0.01):
        self.delta = []
        inputs, t = self.data.train.next_batch(batch)
        y = self.fp(inputs)
        d = -(y - t) * self.sigmoid(y, derivative=True)
        d = ones([1, batch]).dot(d) / batch

        for w, b, z, a in zip(self.weights[::-1], self.biases[::-1], self.z[::-1], self.a[::-1]):
            self.delta.insert(0, d)
            d = d.dot(w.T) * self.sigmoid(a, derivative=True)
            d = ones([1, batch]).dot(d) / batch

        self.gradw = []
        self.gradb = []
        for a, d in zip(self.a, self.delta):
            self.gradw.append(ones([1, batch]).dot(a).T.dot(d) / batch)
            self.gradb.append(d)

        for i, (gw, gb) in enumerate(zip(self.gradw, self.gradb)):
            self.weights[i] += learning_rate * gw
            self.biases[i] += learning_rate * gb

    def training(self, times=150, batch=1, learning_rate=0.1):
        correct_prediction = equal(argmax(self.fp(data.test.images), 1), argmax(data.test.labels, 1))
        accuracy = mean(correct_prediction, axis=0)
        print(accuracy)
        for i in range(times):
            self.bp_step(batch, learning_rate)
            if i % 50 == 0:
                correct_prediction = equal(argmax(self.fp(data.test.images), 1), argmax(data.test.labels, 1))
            accuracy_test = mean(correct_prediction, axis=0)
            correct_prediction = equal(argmax(self.fp(data.train.images), 1), argmax(data.train.labels, 1))
            accuracy_train = mean(correct_prediction, axis=0)
            print('%2.1f'%(i*100/times), accuracy_train, accuracy_test)


net = mnist_net([784, 15, 10], data)
net.training()
for i in net.gradw:
    print(i)
    print(i.shape)

def s(data):
    for i in data:
        print(i.shape)
