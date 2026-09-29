"""Synthetic fixtures only: isolation, weighting and deterministic routing semantics."""
import copy
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import router_v147 as r

def fixture():
    return [{'key':f'{g}_{i}','group':g,'features':[i+1,2,j+1,.1*i,.2*i,i/4,.03*i],
             'gain':(.02 if (i+j)%3==0 else -.01)} for j,g in enumerate('abcdefg') for i in range(5)]

def test_held_outcomes_cannot_change_outer_model_or_threshold_or_decision():
    a=fixture();base=r.outer_fold(a,'g');b=copy.deepcopy(a)
    for row in b:
        if row['group']=='g':row['gain']=100000+row['features'][0]
    assert base==r.outer_fold(b,'g')
    for variant in base['variants'].values():
        for fold in variant['inner_folds']:
            assert not set(fold['training_keys'])&set(fold['validation_keys'])
            assert all(not k.startswith('g_') for k in fold['training_keys']+fold['validation_keys'])

def test_group_weight_is_unchanged_by_duplication_within_family():
    rows=fixture();more=rows+[dict(x,key=x['key']+'_copy') for x in rows if x['group']=='g']
    a=r.fit(rows,list(range(7)));b=r.fit(more,list(range(7)))
    for k in ['mean','scale','coef','intercept']:assert np.allclose(a[k],b[k],atol=1e-12)
    assert sum(r.weights(more)[i] for i,x in enumerate(more) if x['group']=='g')==pytest.approx(1/7)

def test_negative_calibration_prefers_never():
    rows=fixture()
    for x in rows:x['gain']=-.1
    selected=r.select([i/len(rows) for i in range(len(rows))],rows)['selected']
    assert selected=={'threshold':None,'gain':0.,'rate':0.}

def test_weighted_quantile_does_not_overweight_large_family():
    rows=[{'group':'a'} for _ in range(25)]+[{'group':'b'}]
    assert r.quantile([0]*25+[10],rows,.8)==10

def test_uncertainty_is_derived_only_from_prefix():
    from router_v132 import features
    state={'ids':list(range(10)),'order':list(range(60)),'labels':[[x] for x in [20,18,17,16,15,14,13,12,11,10]]}
    b=copy.deepcopy(state);b['labels']=[[x[0]*100] for x in state['labels']]
    assert np.allclose(features(state,[[1,2]],'minimize'),features(b,[[1,2]],'minimize'))
