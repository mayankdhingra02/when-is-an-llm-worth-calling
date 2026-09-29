import numpy as np
from escalation.sat_v64 import grid,encode

def test_sat_grid_includes_both_admission_configs_and_unique_encodings():
    g=grid();assert len(g)==len(set(g))==48
    assert (.95,.999,100,2,2) in g and (.8,.9,25,1.2,0) in g
    x=encode(g);assert x.shape==(48,5) and np.min(x)>=0 and np.max(x)<=1+1e-12
    assert len({tuple(row) for row in x})==48
