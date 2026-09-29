"""Acquisition fixtures only; empirical results never sourced from these tests."""
from types import SimpleNamespace
import pytest
from escalation.quality_controls_v12 import choose


def test_feature_only_knn_uses_acquired_labels_and_stable_ties():
    c=SimpleNamespace(x=[(0,0),(0,1),(1,0),(1,1),(0,0)])
    ids=[0,1,2];labels=[[10,100],[20,100],[30,100]];order=[4,3,2,1,0]
    i,event=choose(c,order,ids,labels,100,'joint_3nn')
    assert i==4 and event['predicted_runtime']==20 and event['predicted_size']==100
    assert ids==[0,1,2] and labels==[[10,100],[20,100],[30,100]]


def test_random_order_and_infeasible_predictions():
    c=SimpleNamespace(x=[(0,),(1,),(2,),(3,),(4,)])
    assert choose(c,[4,3,2,1,0],[0,1,2],[[1,10]]*3,5,'random')[0]==4
    i,event=choose(c,[4,3,2,1,0],[0,1,2],[[1,10]]*3,5,'joint_3nn')
    assert i==4 and event['predicted_feasible'] is False


def test_invalid_methods_and_missing_acquired_labels():
    c=SimpleNamespace(x=[(i,) for i in range(5)])
    with pytest.raises(ValueError):choose(c,list(range(5)),[0,1,2],[[1,10]],5,'joint_3nn')
    with pytest.raises(ValueError):choose(c,list(range(5)),[0,1,2],[[1,10]]*3,5,'fake_llm')
