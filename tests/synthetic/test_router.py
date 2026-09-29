import copy
import numpy as np
import pytest
from escalation.router import GainRouter,FEATURES,select_threshold

def rows():
    return [{'split':'development','system_group':g,'features':dict(zip(FEATURES,[i+len(g)]*len(FEATURES))),'gain':i*.01,'classical_loss':.5,'llm_loss':.5-i*.01} for g in ['a','bb'] for i in range(5)]

def test_fit_blocks_test_rows():
    r=rows();r[0]['split']='heldout_smoke'
    with pytest.raises(ValueError):GainRouter().fit(r)

def test_prediction_ignores_counterfactual_labels():
    m=GainRouter().fit(rows());a=rows()[:2];b=copy.deepcopy(a)
    for r in b:r.update({'gain':-1000,'classical_loss':-999,'llm_loss':999,'split':'heldout_smoke'})
    assert np.array_equal(m.predict(a),m.predict(b))

def test_threshold_can_choose_never_without_claiming_equivalence():
    t,curve,rate=select_threshold([0,0],[.1,.1],[.11,.11],['a','b'],[-.02,0,.02,float('inf')])
    assert rate==0 and len(curve)==4
