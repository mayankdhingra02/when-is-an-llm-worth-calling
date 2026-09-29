from fractions import Fraction as F
import pytest
from escalation.frontier_v40 import allocation_frontier

def test_hand_computed_mixed_gains_and_random_expectation():
    r=allocation_frontier([F(1,5),F(-1,10),0])
    assert r['maximum_gain_fraction']=='1/15' and r['fewest_calls_at_maximum']==1
    assert r['curves'][1]['random_expected_fraction']=='1/90'
    assert r['curves'][2]['oracle_gain_fraction']=='1/15'
    assert r['curves'][3]['oracle_gain_fraction']=='1/30'

def test_dominance_bound_and_fewest_calls_tie():
    r=allocation_frontier([0,0,F(-1,2)])
    assert r['maximum_gain_fraction']=='0' and r['fewest_calls_at_maximum']==0
    assert [x['oracle_gain_fraction'] for x in r['curves']]==['0','0','0','-1/6']

def test_exact_tiny_gain_not_rounded_into_tie():
    r=allocation_frontier([F(1,10**30),0])
    assert r['positive_cases']==1 and r['fewest_calls_at_maximum']==1

def test_permutation_invariance_of_bounds():
    a=allocation_frontier([F(1,7),F(-1,3),F(2,9)])
    b=allocation_frontier([F(2,9),F(1,7),F(-1,3)])
    assert [x['oracle_gain_fraction'] for x in a['curves']]==[x['oracle_gain_fraction'] for x in b['curves']]

@pytest.mark.parametrize('gains',[[],[0]*16])
def test_bounded_size(gains):
    with pytest.raises(ValueError):allocation_frontier(gains)
