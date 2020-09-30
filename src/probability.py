import math
import random
from functools import wraps


def binsearch_solve(function, lo, hi, e=0.001):
    while hi - lo >= e:
        mid = (lo + hi) / 2
        result = function(mid)
        if result * function(hi) <= 0:
            lo = mid
        elif result * function(lo) <= 0:
            hi = mid
        else:
            lo, hi = (lo + mid) / 2, (hi + mid) / 2
    return (lo + hi) / 2


def integrate(function, start, end, step=0.001):
    result = 0
    step = abs(step)
    flag = 1
    if start > end:
        start, end = end, start
        flag = -1
    elif start == end:
        return 0
    lo = start
    hi = start + step
    while hi <= end:
        column = function((lo + hi) / 2) * step
        if not math.isnan(column):
            result += column
        lo, hi = hi, hi + step
    result = result * flag
    return result


def iterfunc(function):
    @wraps(function)
    def iterfunc_wrapper(x):
        if '__iter__' in dir(x):
            return [function(x_i) for x_i in x.__iter__()]
        elif x is None or x is math.isnan(x):
            return math.nan
        else:
            try:
                return function(x)
            except ZeroDivisionError:
                return math.nan
    return iterfunc_wrapper


def pdf2cdf(start, end):
    def pdf2cdf_wrapper(PDF):
        @wraps(PDF)
        @iterfunc
        def CDF(x):
            if x < start:
                return 0
            elif x > end:
                return 1
            else:
                y = integrate(PDF, start, x)
                return y
        return CDF
    return pdf2cdf_wrapper


def cdf2pdf(step=0.001):
    def cdf2pdf_wrapper(CDF):
        @wraps(CDF)
        @iterfunc
        def PDF(x):
            if '__iter__' in dir(x):
                return [CDF(x_i) for x_i in x.__iter__()]
            y = (CDF(x + step / 2) - CDF(x - step / 2)) / step
            return y
        return PDF
    return cdf2pdf_wrapper


def reverse_function(lo=-100, hi=100):
    def reverse_function_wrapper(function):
        @wraps(function)
        @iterfunc
        def reversed_function(y):
            result = binsearch_solve(lambda x: function(x) - y, lo, hi)
            return result
        return reversed_function
    return reverse_function_wrapper


def sampler(CDF, lo=-100, hi=100):
    y = random.random()
    x = reverse_function()(CDF)(y)
    return x


def integrate_sample(function, CDF, n):  # ERR
    result = 0
    for i in range(n):
        x = sampler(CDF)
        result += function(x) / (CDF(x) * n)
    return result
