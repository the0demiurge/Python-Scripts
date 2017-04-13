import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


class IncreaseNN(object):

    def __init__(self, shape, X=None, Y=None, log_dir='/tmp/tf_charlesxu'):
        if X and Y:
            shape.insert(0, X.shape[1])
            shape.append(Y.shape[1])
        tf.reset_default_graph()
        self.__shape = shape
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        self.log_dir = log_dir + '/' + self.curtime
        self.sess = tf.InteractiveSession()
        self.net = self.interferece(self.shape)
        tf.global_variables_initializer().run()
        self.__step = 0

    def _init_placeholders(self, shape):
        with tf.name_scope('input'):
            placeholders = {
                'x': tf.placeholder(tf.float32, [None, shape[0]]),
                'y': tf.placeholder(tf.float32, [None, shape[-1]])
            }
        return placeholders

    def _init_variables(self, shape):

        def init_weight_variable(shape):
            """Create a weight variable with appropriate initialization."""
            initial = tf.truncated_normal(shape, stddev=0.1)
            return tf.Variable(initial)

        def init_bias_variable(shape):
            """Create a bias variable with appropriate initialization."""
            initial = tf.constant(0.1, shape=shape)
            return tf.Variable(initial)

        variables = {
            'weights': [init_weight_variable([a, b]) for a, b in zip(shape[:-1], shape[1:])],
            'biases': [init_bias_variable([a]) for a in shape[1:]]
        }
        for index, (w, b) in enumerate(zip(variables['weights'], variables['biases'])):
            self._variable_summaries(w, 'weight_%d' % index)
            self._variable_summaries(b, 'bias_%d' % index)
        return variables

    def _init_layer(self, name, x, w, b, activation=tf.nn.relu):
        with tf.name_scope(name):
            z = tf.matmul(x, w) + b
            tf.summary.histogram('z', z)
            layer = activation(z)
            tf.summary.histogram('layer', layer)
        return layer

    def _init_layers(self, placeholders, variables):
        layers = [placeholders['x']]
        for index, (w, b) in enumerate(zip(variables['weights'][:-1], variables['biases'][:-1])):
            layer = self._init_layer('layer_%d' % index, layers[-1], w, b)
            layers.append(layer)
        layer = self._init_layer('last_layer', layers[-1], variables['weights'][-1], variables['biases'][-1], tf.identity)
        layers.append(layer)
        return layers

    def _init_loss(self, labels, logits):
        with tf.name_scope('cross_entropy'):
            diff = tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits)
            with tf.name_scope('total'):
                cross_entropy = tf.reduce_mean(diff)
        tf.summary.scalar('cross entropy', cross_entropy)
        return cross_entropy

    def _init_accuracy(self, labels, logits):
        with tf.name_scope('accuracy'):
            with tf.name_scope('correct_prediction'):
                correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
            with tf.name_scope('accuracy'):
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)
        return accuracy

    def _init_train_ops(self, lost, learning_rate=0.01):
        with tf.name_scope('train'):
            train_step = tf.train.RMSPropOptimizer(learning_rate).minimize(lost)
        return train_step

    def interferece(self, shape):
        interfereces = dict()
        interfereces['placeholders'] = self._init_placeholders(shape)
        interfereces['variables'] = self._init_variables(shape)
        interfereces['layers'] = self._init_layers(interfereces['placeholders'], interfereces['variables'])
        interfereces['cross_entropy'] = self._init_loss(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['accuracy'] = self._init_accuracy(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['train_step'] = self._init_train_ops(interfereces['cross_entropy'])
        interfereces['merged'] = tf.summary.merge_all()
        interfereces['summary'] = {
            'train_writer': tf.summary.FileWriter(self.log_dir + '/train', self.sess.graph),
            'test_writer': tf.summary.FileWriter(self.log_dir + '/test', self.sess.graph)}
        return interfereces

    def _feed_dict(self, data, net):
        xs, ys = data.next_batch(100)
        feed_dict = {
            net['placeholders']['x']: xs,
            net['placeholders']['y']: ys
        }
        return feed_dict

    def fit(self, data_train, data_test, epoches=1000):
        net = self.net
        for epoch in range(epoches):
            # testing
            if epoch % 1 == 0:
                run_metadata = tf.RunMetadata()
                summary, test_accuracy = self.sess.run(
                    [net['merged'], net['accuracy']],
                    feed_dict=self._feed_dict(data_test, net),
                    run_metadata=run_metadata)
                net['summary']['test_writer'].add_run_metadata(run_metadata, 'step%06d' % self.__step)
                net['summary']['test_writer'].add_summary(summary, self.__step)
                print(self.__step, test_accuracy, end='\n')

            # training
            run_metadata = tf.RunMetadata()
            summary, _ = self.sess.run(
                [net['merged'], net['train_step']],
                feed_dict=self._feed_dict(data_train, net),
                run_metadata=run_metadata)
            net['summary']['train_writer'].add_run_metadata(run_metadata, 'step%06d' % self.__step)
            net['summary']['train_writer'].add_summary(summary, self.__step)
            self.__step += 1
        self.__step += 100

    def increase(self, shape):
        old_variables = {
            'weights': [var.eval() for var in self.net['variables']['weights']],
            'biases': [var.eval() for var in self.net['variables']['biases']]
        }
        self.sess.close()
        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()
        interfereces = dict()
        interfereces['placeholders'] = self._init_placeholders(shape)

        variables = {
            'weights': [self._increase_variable(
                [a, b], old_variables['weights'][index] if index < len(old_variables['weights']) else None
            ) for index, (a, b) in enumerate(zip(shape[:-1], shape[1:]))],
            'biases': [self._increase_variable(
                [a], old_variables['biases'][index] if index < len(old_variables['biases']) else None
            ) for index, a in enumerate(shape[1:])]
        }

        for index, (w, b) in enumerate(zip(variables['weights'], variables['biases'])):
            self._variable_summaries(w, 'weight_%d' % index)
            self._variable_summaries(b, 'bias_%d' % index)

        interfereces['variables'] = variables
        interfereces['layers'] = self._init_layers(interfereces['placeholders'], interfereces['variables'])
        interfereces['cross_entropy'] = self._init_loss(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['accuracy'] = self._init_accuracy(labels=interfereces['placeholders']['y'], logits=interfereces['layers'][-1])
        interfereces['train_step'] = self._init_train_ops(interfereces['cross_entropy'])
        interfereces['merged'] = tf.summary.merge_all()
        interfereces['summary'] = {
            'train_writer': tf.summary.FileWriter(self.log_dir + '/train', self.sess.graph),
            'test_writer': tf.summary.FileWriter(self.log_dir + '/test', self.sess.graph)}
        self.net = interfereces
        tf.global_variables_initializer().run()
        return interfereces

    def predict(self, data_x):
        return self.net['layers'][-1].eval(session=self.sess, feed_dict={self.net['placeholders']['x']: data_x})

    def _variable_summaries(self, variable, name='var'):
        """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
        with tf.name_scope(name):
            mean = tf.reduce_mean(variable)
            tf.summary.scalar('mean', mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(variable - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(variable))
            tf.summary.scalar('min', tf.reduce_min(variable))
            tf.summary.histogram('histogram', variable)

    def _increase_variable(self, shape, from_variable=None):
        if from_variable is None:
            to_values = np.random.randn(*shape) / 10
            var = tf.Variable(to_values, dtype=tf.float32)
            tf.variables_initializer([var]).run()
            return var

        if isinstance(from_variable, tf.Variable):
            try:
                from_variable.eval(session=self.sess)
            except tf.errors.FailedPreconditionError:
                tf.variables_initializer([from_variable]).run()
            from_shape = from_variable.get_shape().as_list()
            from_values = from_variable.eval(session=self.sess)
        elif isinstance(from_variable, np.ndarray):
            from_shape = from_variable.shape
            from_values = from_variable
        else:
            raise Exception('Not recognised type %s' % str(type(from_variable)))
        to_values = np.random.randn(*shape) / 10
        transfer_shape = [min(dim) for dim in zip(from_shape, shape)]

        if len(from_shape) == 1:
            to_values += 0.1
            to_values[:transfer_shape[0]] = from_values[:transfer_shape[0]]
        else:
            to_values[..., :transfer_shape[-2], :transfer_shape[-1]] = from_values[..., :transfer_shape[-2], :transfer_shape[-1]]
        var = tf.Variable(to_values, dtype=tf.float32)
        tf.variables_initializer([var]).run()
        return var

    @property
    def curtime(self):
        cur_time = time.strftime('%Y-%m-%d_%X', time.localtime(time.time()))
        return cur_time

    @property
    def shape(self):
        return self.__shape


def original(data):
    network = IncreaseNN([784, 20, 10], log_dir='/tmp/tf_charlesxu/original_wide')
    network.fit(data.train, data.test, epoches=100)
    for hidden in range(20):
        network.increase([784, 20, 10])
        network.fit(data.train, data.test, epoches=100)

    structure = [784] + [30] * 19 + [10]
    network = IncreaseNN(structure, log_dir='/tmp/tf_charlesxu/original_deep')
    network.fit(data.train, data.test, epoches=100)
    for hidden in range(20):
        network.increase(structure)
        network.fit(data.train, data.test, epoches=100)


def widen(data):
    network = IncreaseNN([784, 1, 10], log_dir='/tmp/tf_charlesxu/widen')
    network.fit(data.train, data.test, epoches=100)
    for hidden in range(20):
        network.increase([784, hidden + 2, 10])
        network.fit(data.train, data.test, epoches=100)


def deepen(data):
    structure = [784, 30, 10]
    network = IncreaseNN(structure, log_dir='/tmp/tf_charlesxu/deepen')
    network.fit(data.train, data.test, epoches=100)
    for hidden in range(20):
        structure.insert(1, 30)
        network.increase(structure)
        network.fit(data.train, data.test, epoches=100)


def main():
    data_path = '/home/charlesxu/Workspace/data/MNIST_data/'
    data = input_data.read_data_sets(data_path, one_hot=True)

    original(data)
    widen(data)
    deepen(data)


if __name__ == '__main__':
    main()
()
