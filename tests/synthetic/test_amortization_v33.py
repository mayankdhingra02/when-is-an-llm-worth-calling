import pytest
from escalation.amortization_v33 import recovery_threshold,net_saved,presentation_scenarios

def test_recovery_equation_and_nonpositive_gains():
    assert recovery_threshold(.02,8)==400
    assert net_saved(.02,8,400)==0 and net_saved(.02,8,401)>0
    assert recovery_threshold(0,8) is None and recovery_threshold(-.02,8) is None
    assert net_saved(-.02,8,1000)==-28

def test_missing_and_invalid_cost_cannot_be_zero():
    for gain,cost in [(float('nan'),8),(.1,float('inf')),(.1,-1)]:
        with pytest.raises(ValueError):recovery_threshold(gain,cost)
    with pytest.raises(TypeError):recovery_threshold(.1,None)
    with pytest.raises(ValueError):net_saved(.1,1,-1)

def test_presentation_mean_is_not_mean_of_recovery_thresholds():
    rows=[{'condition':c,'gain':g,'request_seconds':t} for c,g,t in
        [('assigned_ids',.01,1),('reverse_display',.02,4),('reassigned_ids',.03,3)]]
    r=presentation_scenarios(rows)
    assert r['assigned_recovery_seconds']==100 and r['all_three_recovery_seconds']==200
    assert r['uniform_presentation_recovery_seconds']==pytest.approx((8/3)/.02)
    rows[1]['gain']=0
    assert presentation_scenarios(rows)['all_three_recovery_seconds'] is None
    assert presentation_scenarios(rows)['uniform_presentation_recovery_seconds'] is not None

def test_reject_duplicate_presentation_and_preserve_input():
    rows=[{'condition':'assigned_ids','gain':.1,'request_seconds':1}]*3
    with pytest.raises(ValueError):presentation_scenarios(rows)
