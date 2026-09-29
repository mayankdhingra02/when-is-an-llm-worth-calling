import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from policy_envelope_v129 import envelope
def row(k,group,target,reference=10):return {'key':k,'system_group':group,'target':target,'references':{'full_sequential_3nn':reference}}
def test_one_improvement_defeats_dominance_and_is_retained():
    d=envelope([row('good','a',8),row('bad','a',12)])
    assert d['policies']==4 and d['positive_gain_policies']==1 and d['observed_hindsight_gain']==.1
    assert not d['never_dominates_all_nonempty_policies_in_quality_and_calls']
def test_ties_and_harms_give_zero_ceiling_without_deleting_ties():
    d=envelope([row('tie1','a',10),row('tie2','a',10),row('bad','b',12)])
    assert d['zero_gain_policies']==4 and d['positive_gain_policies']==0 and d['observed_hindsight_gain']==0
    assert d['never_dominates_all_nonempty_policies_in_quality_and_calls']
def test_equal_family_weights_do_not_turn_extra_seeds_into_groups():
    d=envelope([row('a1','a',8),row('a2','a',8),row('b','b',12)])
    assert d['masks'][-1]['gain_numerator']==0 and d['observed_hindsight_gain']==.1
