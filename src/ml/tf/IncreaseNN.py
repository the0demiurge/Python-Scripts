import argparse
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


class IncreaseNN(object):

    def init(self, shape):
        self.__shape = shape
        self.sess = tf.InteractiveSession()
        self.net = self.interferece(self.shape)
        tf.global_variables_initializer().run()

    def init_placeholders(self, shape):
        with tf.name_scope('input'):
            placeholders = {
                'x': tf.placeholder(tf.float32, [None, shape[0]]),
                'y': tf.placeholder(tf.float32, [None, shape[-1]])
            }
        return placeholders

    def init_variables(self, shape):

        def init_weight_variable(shape):
            """Create a weight variable with appropriate initialization."""
            initial = tf.truncated_normal(shape, stddev=0.1)
            return tf.Variable(initial)

        def init_bias_variable(shape):
            """Create a bias variable with appropriate initialization."""
            initial = tf.constant(0.1, shape=shape)
            return tf.Variable(initial)

        with tf.name_scope('variables'):
            variables = {
                'weights': [init_weight_variable(a, b) for a, b in zip(shape[:-1], shape[1:])],
                'biases': [init_bias_variable([a]) for a in shape[1:]]
            }
        for w, b in zip(variables['weights'], variables['biases']):
            self.variable_summaries(w)
            self.variable_summaries(b)
        return variables

    def init_layer(self, name, x, w, b, activation=tf.nn.relu):
        with tf.name_scope(name):
            z = x * w + b
            tf.summary('z', z)
            layer = activation(z)
            tf.summary.histogram('layer', layer)
        return layer

    def init_layers(self, placeholders, variables):
        layers = [placeholders['x']]
        for index, (w, b) in enumerate(zip(variables['weights'][:-1], variables['biases'][:-1])):
            layer = self.init_layer('layer %d' % index, layers[-1], w, b)
            layers.append(layer)
        layer = self.init_layer('last layer', layers[-1], variables['weights'][-1], variables['biases'][-1], tf.identity)
        layers.append(layer)
        return layers

    def init_loss(self, labels, logits):
        with tf.name_scope('cross entropy'):
            diff = tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits)
            with tf.name_scope('total'):
                cross_entropy = tf.reduce_mean(diff)
        tf.summary.scalar('cross entropy', cross_entropy)
        return cross_entropy

    def init_accuracy(self, labels, logits):
        with tf.name_scope('accuracy'):
            with tf.name_scope('correct_prediction'):
                correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
            with tf.name_scope('accuracy'):
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)
        return accuracy

    def init_train_ops(self, lost, learning_rate=0.01):
        with tf.name_scope('train'):
            train_step = tf.train.RMSPropOptimizer(learning_rate).minimize(lost)
        return train_step

    def interferece(self, shape):
        interfereces = dict()
        interfereces['placeholders'] = self.init_placeholders(shape)
        interfereces['variables'] = self.init_variables(shape)
        interfereces['layers'] = self.init_layers(interfereces['placeholders'], interfereces['variables'])
        interfereces['cross_entropy'] = self.init_loss(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['accuracy'] = self.init_accuracy(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['train_step'] = self.init_train_ops(interfereces['cross_entropy'])
        interfereces['merged'] = tf.summary.merge_all()
        interfereces['summary'] = {
            'train_writer': tf.summary.FileWriter(self.log_dir + '/train', self.sess.graph),
            'test_writer': tf.summary.FileWriter(self.log_dir + '/test', self.sess.graph)}
        return interfereces

    def train(self, data):
        pass

    def increase(self):
        pass

    def predict(self):
        pass

    def variable_summaries(self, variable):
        """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(variable)
            tf.summary.scalar('mean', mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(variable - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(variable))
            tf.summary.scalar('min', tf.reduce_min(variable))
            tf.summary.histogram('histogram', variable)

    @staticmethod
    def increase_variable(from_variable, shape):
        from_shape = from_variable.get_shape()
        from_values = from_variable.eval()
        to_values = np.random.randn(*shape) / 10

        # 应当适当扩展宽容性

    @property
    def shape(self):
        return self.__shape


def main():
    pass


if __name__ == '__main__':
    main()
