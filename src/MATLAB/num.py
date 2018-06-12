#!/usr/bin/env python3
"""Python MATLAB style tools
"""
import numpy as np
import re
from ast import literal_eval

inv = np.linalg.inv
rank = np.linalg.matrix_rank
det = np.linalg.det
exp = np.linalg.matrix_power


def mat(data):
    # string -> numpy.mat
    return np.mat([[literal_eval(number) for number in re.split('[ ,]+', numbers.strip())] for numbers in data.split(';')])
