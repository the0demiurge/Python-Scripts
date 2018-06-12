#!/usr/bin/env python3
"""Python MATLAB style tools
"""
import sympy as s
from sympy import symbols, Matrix, MatrixSymbol, abc, det, Inverse
import re
from ast import literal_eval

sinv = s.Inverse
sexp = s.MatPow
syms = symbols
sdet = det

def smat(data):
    # string -> sympy.Matrix
    return Matrix([[syms(number) for number in re.split('[ ,]+', numbers.strip())] for numbers in data.split(';')])
