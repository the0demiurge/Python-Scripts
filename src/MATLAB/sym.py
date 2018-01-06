#!/usr/bin/env python3
"""Python MATLAB style tools
"""
import sympy as s
from math import sqrt
from sympy import symbols, Matrix, MatrixSymbol, abc, det, Inverse

inv = s.Inverse
exp = s.MatPow
syms = symbols


def mat(data, shape=None):
    # Make a matrix by inputing data in one-line and mat-shape
    if not shape:
        shape = [round(sqrt(len(data)))] * 2
    elif isinstance(shape, int):
        shape = [shape, len(data) / shape]
    return Matrix(s.reshape(data, [shape[0]]))
