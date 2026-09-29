"""Frozen finite MiniSat search domain, no hidden-label inputs."""
import itertools
import numpy as np
def grid():return list(itertools.product([.8,.95],[.9,.999],[25,100,400],[1.2,2],[0,2]))
def encode(configs):
    # Declared-domain scales expressed exactly to avoid float-subtraction tie drift.
    return np.array([[{.8:0.,.95:1.}[a],{.9:0.,.999:1.}[b],
                      {25:0.,100:.5,400:1.}[c],{1.2:0.,2:1.}[d],{0:0.,2:1.}[e]]
                     for a,b,c,d,e in configs])
