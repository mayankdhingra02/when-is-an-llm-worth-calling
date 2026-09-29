"""Hand-computable, synthetic evaluator fixtures; excluded from research aggregates."""
import copy,math
import pytest
from escalation.checkpoint_audit_v18 import decompose

def fixture():
    labels=[[100.,50.]]+[[90.,50.]]*8+[[80.,50.]]+[[70.,50.]]*9+[[60.,50.]]+[[40.,50.],[1.,100.]]
    prefix={'ids':list(range(10)),'labels':copy.deepcopy(labels[:10]),'reference_row':0,'size_cap':50.}
    arm={'ids':list(range(20)),'labels':copy.deepcopy(labels[:20]),'size_cap':50.,'best_feasible_ms':60.,'best_row':19}
    return labels,prefix,arm

def test_decomposition_uses_common_denominator_and_excludes_infeasible_optimum():
    d=decompose(*fixture())
    assert d['hindsight_ms']==40 and d['hindsight_best_id']==20
    assert d['reference_headroom']==.6 and d['checkpoint_headroom']==.5
    assert math.isclose(d['cheap_headroom'],1/3)
    assert [d[k] for k in ['pre_checkpoint_saved_fraction_of_reference','continuation_saved_fraction_of_reference','remaining_fraction_of_reference']]==[.2,.2,.2]

def test_no_headroom_is_zero_without_division_by_zero_or_false_improvement():
    ys,p,a=fixture();ys=[[100.,50.]]*len(ys);p['labels']=ys[:10];a['labels']=ys[:20];a['best_feasible_ms']=100.;a['best_row']=0
    d=decompose(ys,p,a)
    assert d['reference_headroom']==d['checkpoint_headroom']==d['cheap_headroom']==0
    assert not d['cheap_continuation_improved'] and d['checkpoint_at_recorded_optimum']

@pytest.mark.parametrize('problem',['label','prefix','budget','cap','nonfinite'])
def test_malformed_evidence_fails_closed(problem):
    ys,p,a=fixture()
    if problem=='label':p['labels'][0][0]=999
    if problem=='prefix':a['ids'][0],a['ids'][1]=a['ids'][1],a['ids'][0]
    if problem=='budget':a['ids'][-1]=a['ids'][-2]
    if problem=='cap':p['size_cap']=999
    if problem=='nonfinite':ys[-1][0]=float('nan')
    with pytest.raises(ValueError):decompose(ys,p,a)
