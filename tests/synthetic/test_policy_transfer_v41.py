"""Synthetic analysis tests; none is an experimental LLM response."""
import copy
import math
import pytest
from escalation.policy_transfer_v41 import predecision_masks,family_contrast,observed_usage,evaluate_policies


def fixture():
    rows=[{'dataset':f'fixture{i}','seed':11,'system_group':f'g{i//2}','features':{'x':float(i),'uncertainty':i/10}} for i in range(6)]
    seal={'benefit':{'features':['x','uncertainty'],'mean':[0,0],'scale':[1,1],'coefficient':[1,0],
                    'intercept':0,'threshold':2,'development_oof_rate':.5},'uncertainty':{'threshold':.3,'rate':.5}}
    return rows,seal


def test_masks_exact_strict_thresholds_and_matched_counts():
    rows,seal=fixture();m,s=predecision_masks(rows,seal)
    assert s==[0,1,2,3,4,5] and m['benefit']==[False,False,False,True,True,True]
    assert m['uncertainty']==[False,False,False,False,True,True]
    for name in ('benefit','uncertainty'):assert sum(m[name])==sum(m['random_matched_'+name+'_diagnostic'])


def test_randomization_stable_to_cohort_file_order():
    rows,seal=fixture();m,_=predecision_masks(rows,seal);reverse,_=predecision_masks(rows[::-1],seal)
    for name in m:assert m[name]==reverse[name][::-1]


def test_null_thresholds_never_call():
    rows,seal=fixture();seal['benefit']['threshold']=None;seal['uncertainty']['threshold']=None
    masks,_=predecision_masks(rows,seal)
    assert not any(masks['benefit']) and not any(masks['uncertainty'])


@pytest.mark.parametrize('mutation',['outcome','extra_feature','missing_feature','nan','duplicate','zero_scale'])
def test_bad_predecision_inputs_rejected(mutation):
    rows,seal=fixture()
    if mutation=='outcome':rows[0]['gain']=.99
    elif mutation=='extra_feature':rows[0]['features']['llm_score']=.99
    elif mutation=='missing_feature':rows[0]['features'].pop('x')
    elif mutation=='nan':rows[0]['features']['x']=float('nan')
    elif mutation=='duplicate':rows.append(copy.deepcopy(rows[0]))
    else:seal['benefit']['scale'][0]=0
    with pytest.raises(ValueError):predecision_masks(rows,seal)


def test_family_weights_not_seed_counts():
    r=family_contrast([1,1,1,-1],['a','a','a','b'])
    assert r['family_mean_gain']==0 and r['families']==2 and r['exact_family_sign_flip_p']==1


def test_sign_flip_has_family_denominator():
    r=family_contrast([.1]*30,[f'g{i//5}' for i in range(30)])
    assert r['family_mean_gain']==pytest.approx(.1)
    assert r['exact_family_sign_flip_p']==pytest.approx(2/64)


def test_unknown_usage_does_not_become_zero():
    assert observed_usage([],'tokens')==0
    assert observed_usage([{'tokens':3},{}],'tokens') is None
    with pytest.raises(ValueError):observed_usage([{'tokens':-1}],'tokens')


def test_nonfinite_or_missing_outcomes_not_dropped():
    with pytest.raises(ValueError):family_contrast([.1,float('nan')],['a','b'])
    with pytest.raises(ValueError):family_contrast([.1],['a','b'])


def test_policy_oracle_costs_and_failures():
    gains=[.03,-.02];groups=['a','b'];masks={'never':[False,False],'always':[True,True]}
    requests=[{'status':'response','input_tokens':10,'output_tokens':20,'wall_seconds':2},
              {'status':'error','input_tokens':None,'output_tokens':None,'wall_seconds':3}]
    rows=evaluate_policies(gains,groups,masks,requests,[1,1],[.1,.1])
    at=lambda name,cost:next(r for r in rows if r['policy']==name and r['hypothetical_relative_penalty_per_call']==cost)
    assert at('always',0)['observed_selected_input_tokens'] is None
    assert at('always',0)['selected_model_failures']==1
    assert at('always',0)['retrospective_deployment_objective_accesses']==40
    assert at('always',0)['estimated_observed_components_seconds']==7
    assert at('never',.01)['calls']==0 and at('never',.01)['net_utility']['family_mean_gain']==0
    assert at('hindsight_oracle_diagnostic',.01)['calls']==1
    assert at('hindsight_oracle_diagnostic',.01)['net_utility']['family_mean_gain']==pytest.approx(.01)
    assert at('hindsight_oracle_diagnostic',.05)['calls']==0


def test_request_identity_duplicates_fail(monkeypatch):
    monkeypatch.syspath_prepend('scripts')
    from analyze_models_v41 import unique_records
    with pytest.raises(ValueError):unique_records([{'request_id':1},{'request_id':1}])
