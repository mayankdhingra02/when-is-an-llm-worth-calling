"""Synthetic retrospective size-constraint tests; no fabricated model data."""
import pytest
from escalation.quality_v11 import fastest,constrained_case


def test_ties_preserve_acquisition_order_and_cap_equality():
    assert fastest([2,0,1],[3,4,3])[0]==2
    assert fastest([0,1,2],[3,1,2],[10,12,10],10)==(2,2)


def test_fast_large_output_not_feasible_and_anchor_is_retained():
    r=constrained_case([0],[1,2],{'static':[0,1]},[10,1,6],[100,120,90])
    assert r['anchor']==0 and r['size_cap']==100
    assert r['arms']['static']['row_id']==0
    assert r['bounds']['shortlist']['row_id']==2 and r['bounds']['full_table']['runtime']==6


def test_restricted_pool_can_be_worse_than_other_arm():
    r=constrained_case([0],[1],{'adaptive':[0,2]},[10,9,5],[100,100,100])
    assert r['bounds']['shortlist']['runtime']>r['arms']['adaptive']['runtime']

@pytest.mark.parametrize('ids,runtime,size,cap',[([],[],None,None),([0],[0],None,None),([0],[1],[2],1),([0],[1],[2],None)])
def test_invalid_or_infeasible(ids,runtime,size,cap):
    with pytest.raises(ValueError):fastest(ids,runtime,size,cap)


def test_prefix_and_shortlist_integrity():
    with pytest.raises(ValueError):constrained_case([0],[0],{'static':[0]},[1],[1])
    with pytest.raises(ValueError):constrained_case([0],[1],{'static':[1]},[1,2],[1,1])
