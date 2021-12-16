# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 22:16:06 2021

@author: Arthur
"""

import numpy as np
import celestialobject as co
import math

a = [1.78942341, -.742344807]
b = [1.78332591, -.78532352507]
a64 = np.array(a).astype(np.float64)
a32 = np.array(a).astype(np.float32)
b64 = np.array(b).astype(np.float64)
b32 = np.array(b).astype(np.float32)

def inner(u, v):
    return u[1]*v[1] + u[0]*v[0]

def norm_squared(u):
    return u[1]*u[1] + u[0]*u[0]

def norm(u):
    return math.sqrt(u[1]*u[1] + u[0]*u[0])


%timeit np.linalg.norm(a64)
%timeit norm(a64) #actually faster
%timeit np.dot(a64, b64)

%timeit np.dot(a32, b32)

%timeit inner(a64, b64)

%timeit inner(a64, a64)

%timeit norm_squared(a64)

%timeit inner(a32, b32)

c = co.inner(a64,b64)
d = inner(a64, a64)
a64[1]

a=[1,2,3,4]
a[:-1]
a[1:-1]
a[1::]

b =[[1,2],[3,4]]

c=[[]]

a= math.pi
%timeit a**2
%timeit a*a