#!/usr/bin/env python3
"""Python MATLAB style tools
"""
import numpy as np

inv = np.linalg.inv
rank = np.linalg.matrix_rank
det = np.linalg.det
exp = np.linalg.matrix_power


def mat(data, shape):
    # Make a matrix by inputing data in one-line and mat-shape
    return np.mat(np.reshape(data, shape[::-1]))
