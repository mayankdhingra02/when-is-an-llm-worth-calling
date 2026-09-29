import numpy as np
from escalation.candidate_tasks_v66 import grids
from escalation.candidate_screen_v67 import encode

def test_declared_features_are_distinct_and_bounded():
    for family,rows in grids().items():
        x=encode(family,rows)
        assert len(np.unique(x,axis=0))==48
        assert np.all(x>=0) and np.all(x<=1)
        assert np.all(x.min(axis=0)==0) and np.all(x.max(axis=0)==1)
