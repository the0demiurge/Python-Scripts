#!/usr/bin/env python3

import numpy as np


class Scaler(object):
    """Scaler for dataset
    Methods:
        refit: re-obtain min/max/mean/var with given data
        trans: standarize the data
        itrans: inverse transform data from standarized to original

    Usage:
        # loading sklearn datasets
        from sklearn.datasets import load_boston()
        dataset = load_boston()
        X, Y = dataset['data'], dataset['target']

        # using scaler to fit the variance, mean, and minmax
        scaler = Scaler(X, Y, method='minmax', attrs=[-1, 1])
        X, Y = scaler.trans(X, Y)

        # or just transform x or y only
        target = scaler.trans(Y=Y)

        # or inverse
        predicted_Y = scaler.itrans(Y=predicted)
    """

    def __init__(self, X=None, Y=None, method='minmax', attrs=None, axis=0):
        """
        methods: minmax, standard
        attrs:
            In minmax: min and max, [0, 1];
            In standard: mean and variance, [0, 1]
        """
        self._check_None(X, Y)
        self._method = method
        self._attrs = attrs
        self._axis = axis
        self._statistics = dict()

        self._trans_dict = {
            'minmax': self._min_max_scaler,
            'standard': self._standard_scaler}

        self.refit(X, Y)

    def refit(self, X=None, Y=None):
        # refit the data statics including minmax, mean, var
        self._check_None(X, Y)
        self._obtain_statistics(X, 'X')
        self._obtain_statistics(Y, 'Y')

    def trans(self, X=None, Y=None, inv=False):
        self._check_None(X, Y)
        if X is None:
            return self._trans_dict[self._method](Y, 'Y', inv)
        elif Y is None:
            return self._trans_dict[self._method](X, 'X', inv)
        else:
            return self._trans_dict[self._method](X, 'X', inv), self._trans_dict[self._method](Y, 'Y', inv)

    def itrans(self, X=None, Y=None):
        return self.trans(X, Y, inv=True)

    def _obtain_statistics(self, data, name):
        """Obtain minmax, mean and variance"""
        if data is not None:
            if not hasattr(data, 'shape'):
                raise ValueError("'{}' has no attribute '{}".format(name, 'shape'))

            self._statistics[name] = dict()
            self._statistics[name]['shape'] = data.shape

            # judge the dimention of data, decide which axis to use
            if len(data.shape) == 1:
                axis = 0
            elif len(data.shape) == 2:
                axis = self._axis
            else:
                raise ValueError("Dimention of '{}' is not 1 or 2, given {} with shape {}".format(
                    name,
                    len(data.shape).
                    data.shape))

            # record the real axis and obtain statistics
            self._statistics[name]['axis'] = axis

            self._statistics[name]['minmax'] = (
                np.min(data, axis=axis),
                np.max(data, axis=axis))

            self._statistics[name]['norm'] = (
                np.mean(data, axis=axis),
                np.var(data, axis=axis))

    def _min_max_scaler(self, data, name, inv=False):
        """MinMax Scaler
        inv: inverse transform
        """
        if self._attrs is None:
            self._attrs = [0, 1]
        self._attrs.sort()

        data_min, data_max = self._statistics[name]['minmax']

        if not inv:
            return (data - data_min) / (data_max - data_min)
        else:
            return data * (data_max - data_min) + data_min

    def _standard_scaler(self, data, name, inv=False):
        """Standard Scaler, force the mean and variance to given number
        inv: inverse transform
        """
        if self._attrs is None:
            self._attrs = [0, 1]

        data_mean, data_var = self._statistics[name]['norm']

        if not inv:
            return (data - data_mean) / data_var ** 0.5
        else:
            return data * data_var ** 0.5 + data_mean

    @property
    def statistics(self):
        return self._statistics

    def _check_None(self, X, Y):
        if X is None and Y is None:
            raise ValueError('X and Y cannot both be None')

    def __repr__(self):
        return '<{} Scaler with {} fitted, attrs={}>'.format(self._method, tuple(self._statistics.keys()), self._attrs)
