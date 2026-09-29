"""Declared-domain feature scales; no measured outcomes or fitted normalization."""
import math
import numpy as np

def encode(family, configs):
    if family=='duckdb':
        rows=[[math.log2(t)/3,(math.log2(int(m[:-2]))-6)/3,h/12] for t,m,h in configs]
    elif family=='gnu_sort':
        rows=[[math.log2(t)/3,math.log2(int(m[:-1]))/6,(math.log2(b)-1)/5] for t,m,b in configs]
    elif family=='openjpeg':
        rows=[[(math.log2(b)-4)/2,(n-3)/2,(math.log2(t)-7)/3,math.log2(p)] for b,n,t,p in configs]
    else:raise ValueError('Unknown family')
    return np.asarray(rows,dtype=float)
