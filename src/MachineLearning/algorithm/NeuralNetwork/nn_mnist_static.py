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
        self.W0 = np.mat(np.random.randn(784, 15) * .1)
        self.W1 = np.mat(np.random.randn(15, 10) * .1)
        self.b0 = np.mat(np.zeros([1, 15]))
        self.b1 = np.mat(np.zeros([1, 10]))

    def sigmoid(self, z, derivative=False):
        sig = 1 / (1 + exp(-z))
        if not derivative:
            return sig
        return np.multiply(sig, (1 - sig))

    def fp(self, inputs):
        self.l0 = np.mat(inputs)
        self.z1 = inputs.dot(self.W0) + self.b0
        self.l1 = self.sigmoid(self.z1)
        self.z2 = self.l1.dot(self.W1) + self.b1
        self.l2 = self.sigmoid(self.z2)
        return self.l2

    def bp_step(self, batch=1, learning_rate=1, lr_ampl=1):
        inputs, t = self.data.train.next_batch(batch)
        y = self.fp(inputs)
        self.d2 = np.multiply(-(y - t), self.sigmoid(self.z2, derivative=True)).mean(axis=0)

        self.d1 = np.multiply(self.d2.dot(self.W1.T).mean(axis=0), self.sigmoid(self.z1, derivative=True)).mean(axis=0)

        self.gradw1 = self.l1.mean(axis=0).T.dot(self.d2)
        self.gradw0 = self.l0.mean(axis=0).T.dot(self.d1)
        self.gradb1 = self.d2
        self.gradb0 = self.d1

        self.W1 += self.gradw1 * learning_rate
        self.W0 += self.gradw0 * learning_rate * lr_ampl
        self.b1 += self.gradb1 * learning_rate
        self.b0 += self.gradb0 * learning_rate

    def training(self, times=35000, batch=100, learning_rate=3):
        correct_prediction = equal(argmax(self.fp(data.test.images), 1), np.mat(argmax(data.test.labels, 1)).T)
        accuracy = correct_prediction.mean()
        print(accuracy)
        for i in range(times):
            self.bp_step(batch, learning_rate)
            if i % 500 == 0:
                correct_prediction = equal(argmax(self.fp(data.test.images), 1), np.mat(argmax(data.test.labels, 1)).T)
                accuracy_test = correct_prediction.mean()
                print('%2.1f'%(i*100/times), accuracy_test)


net = mnist_net([784, 15, 10], data)
net.training()
for i in [net.gradw0, net.gradw1, net.W0, net.W1]:
    print(i)
    print(i.shape)

def s(data):
    for i in data:
        print(i.shape)
