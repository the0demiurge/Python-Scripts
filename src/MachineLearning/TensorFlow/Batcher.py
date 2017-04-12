#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

__author__ = 'the0demiurge'


class Batcher(object):

    '''create a batcher with the same api as tensorflow
    usage:
        data = Batcher(X, Y)
        batch_xs, batch_ys = data.next_batch(100)
    '''
    _batch_position = 0

    def __init__(
            self,
            X,
            Y,
            train_size=None,
            test_size=None,
            random_state=np.random.randint(0, 4294967295),
            to_shuffle=True):
        '''
Args:
    X, Y: either array or ndarray or pandas.core.DataFrame, training
        inputs and targets
    train_size : float, int, or None (default is None)
            If float, should be between 0.0 and 1.0 and represent the
            proportion of the dataset to include in the train split. If
            int, represents the absolute number of train samples. If None,
            the value is automatically set to the complement of the test size.
    test_size : float, int, or None (default is None)
            If float, should be between 0.0 and 1.0 and represent the
            proportion of the dataset to include in the test split. If
            int, represents the absolute number of test samples. If None,
            the value is automatically set to the complement of the train size.
            If train size is also None, test size is set to 0.25.
    random_state : int or RandomState
            Pseudo-random number generator state used for random sampling.
    to_shuffle: shuffle the data initially
            '''

        X = pd.DataFrame(X)
        Y = pd.DataFrame(Y)

        if X.shape[0] != Y.shape[0]:
            raise ValueError('Amount of X and Y are not equal!')

        if to_shuffle:
            X, Y = shuffle(X, Y)

        (self.X_train,
         self.X_test,
         self.Y_train,
         self.Y_test) = train_test_split(
            X,
            Y,
            train_size=train_size,
            test_size=test_size,
            random_state=random_state)

        self.test_size = self.X_test.shape[0]
        self.train_size = self.X_train.shape[0]

    def next_batch(self, batch_size=100):
        '''returns next_batch data with batch_size
        Args:
            batch_size: size per batch

        Returns:
            batch_xs, batch_ys: numpy.ndarray
        '''
        assert int(batch_size) > 0, 'batch_size {} is not > 0'.format(
            batch_size)
        batch_xs = self.next_xbatch(batch_size)
        batch_ys = self.this_ybatch()
        return batch_xs, batch_ys

    def this_xbatch(self):
        batch_index = np.array(range(
            self._batch_position,
            self._batch_position + self._batch_size))
        batch_index %= self.train_size
        batch_xs = self.X_train.iloc[batch_index, :]
        return batch_xs.values

    def this_ybatch(self):
        batch_index = np.array(range(
            self._batch_position,
            self._batch_position + self._batch_size))
        batch_index %= self.train_size
        batch_ys = self.Y_train.iloc[batch_index, :]
        return batch_ys.values

    def next_xbatch(self, batch_size=100):
        assert int(batch_size) > 0, 'batch_size {} is not > 0'.format(
            batch_size)
        self._batch_size = batch_size
        self._batch_position += batch_size
        self._batch_position %= self.train_size

        batch_index = np.array(range(
            self._batch_position,
            self._batch_position + batch_size))
        batch_index %= self.train_size
        batch_xs = self.X_train.iloc[batch_index, :]
        return batch_xs.values

    def next_ybatch(self, batch_size=100):
        assert int(batch_size) > 0, 'batch_size {} is not > 0'.format(
            batch_size)
        self._batch_size = batch_size
        self._batch_position += batch_size
        self._batch_position %= self.train_size

        batch_index = np.array(range(
            self._batch_position,
            self._batch_position + batch_size))
        batch_index %= self.train_size
        batch_ys = self.Y_train.iloc[batch_index, :]
        return batch_ys.values
