import pytest
from escalation.flights_v90 import CONFIGS,BASELINE,schedule,comparison

def test_domain_and_baseline():
    assert len(CONFIGS)==12 and len({(c['threads'],c['disabled_optimizers']) for c in CONFIGS})==12
    assert CONFIGS[BASELINE]=={'name':'t4_j0_f0','threads':4,'disabled_optimizers':''}

def test_complete_fixed_blocks():
    a=schedule();assert a==schedule() and len(a)==60
    for b in range(5):assert sorted(x['configuration_index'] for x in a if x['block']==b)==list(range(12))

def test_material_screen_requires_all_blocks():
    assert comparison([.8]*5,[1.]*5)['qualified_descriptive_opportunity']
    assert not comparison([.8,.8,.8,.8,.95],[1.]*5)['material_all_blocks']

def test_precision_not_rounded_into_pass():
    assert not comparison([.6,.7,.7,.7,.741],[1.]*5)['precision_screen_pass']

def test_baseline_no_gain():assert comparison([1.]*5,[1.]*5)['median_block_gain']==0

@pytest.mark.parametrize('a,b',[([1],[1]),([0]*5,[1]*5)])
def test_bad_measurements(a,b):
    with pytest.raises(ValueError):comparison(a,b)
