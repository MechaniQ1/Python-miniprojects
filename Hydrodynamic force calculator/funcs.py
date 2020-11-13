# -*- coding: utf-8 -*-
from cmath import exp
def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += float(step)

def potential_pressure(x,z,t):
    global k,w
    return exp(-k*z)*exp(complex(0,1)*(k*x-w*t))

