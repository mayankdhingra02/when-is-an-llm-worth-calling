import math
import pytest
from escalation.opportunity_v24 import frontier

def test_hand_calculated_oracle_and_random():
    out=frontier([.3,-.2,.1]);r=out['curves']
    assert r[1]['oracle_gain']==pytest.approx(.1)
    assert r[1]['random_expected_gain']==pytest.approx(.2/9)
    assert r[2]['oracle_gain']==pytest.approx(.4/3)
    assert out['fewest_calls_at_maximum']==2
    assert [x['enumerated_subsets'] for x in r]==[1,3,3,1]

def test_all_harm_or_ties_prefers_no_calls():
    out=frontier([0,0,-.1]);assert out['fewest_calls_at_maximum']==0
    assert out['maximum_oracle_gain']==0 and out['curves'][3]['oracle_gain']<0

def test_reordering_cannot_change_frontier_quality():
    a=frontier([.1,-.2,.3,.1]);b=frontier([.3,.1,-.2,.1])
    for x,y in zip(a['curves'],b['curves']):
        assert x['oracle_gain']==pytest.approx(y['oracle_gain'])
        assert x['random_expected_gain']==pytest.approx(y['random_expected_gain'])
    assert a['enumerated_subsets']==16

@pytest.mark.parametrize('values',[[],[float('nan')],[float('inf')],[0]*16])
def test_bad_inputs_fail(values):
    with pytest.raises(ValueError):frontier(values)
