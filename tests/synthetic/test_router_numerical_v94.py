import importlib.util
from pathlib import Path
import sys
import numpy as np
SCRIPTS=Path(__file__).resolve().parents[2]/'scripts'
sys.path.insert(0,str(SCRIPTS))
from prepare_router_numerical_v94 import fit,predict,choose

def test_ridge_handles_constant_and_training_only_scaling():
    x=np.array([[0.,10.],[1.,10.],[2.,10.],[3.,10.]])
    m=fit(x,np.array([0.,1.,2.,3.]))
    assert m['scale'][1]==1.
    original=list(m['mean']);predict(np.array([[1e6,10.]]),m)
    assert m['mean']==original and m['coefficient'][1]==0.

def test_negative_development_gains_choose_never():
    r=choose(np.array([.1,.2,.3,.4]),np.array([-.1,0.,.01,.02]),np.array(['a','a','b','b']),[0.,.2,float('inf')])
    assert r['threshold'] is None and r['development_rate']==0

def test_threshold_criterion_equal_weights_systems():
    # One three-seed losing group and one winning group; group mean, not seed mean.
    scores=np.ones(4);y=np.array([-.1,-.1,-.1,.3]);groups=np.array(['a','a','a','b'])
    r=choose(scores,y,groups,[0.,float('inf')])
    assert r['threshold']==0. and r['development_calls']==4
    assert abs(r['development_utility']-.05)<1e-12
