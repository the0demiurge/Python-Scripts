#!/usr/bin/env python3
"""Python MATLAB style tools
"""
import numpy as np
from math import sqrt

inv = np.linalg.inv
rank = np.linalg.matrix_rank
det = np.linalg.det
exp = np.linalg.matrix_power


def mat(data, shape=None):
    # Make a matrix by inputing data in one-line and mat-shape
    if not shape:
        shape = [round(sqrt(len(data)))] * 2
    elif isinstance(shape, int):
        shape = [shape, len(data) / shape]
    return np.mat(np.reshape(data, shape))
