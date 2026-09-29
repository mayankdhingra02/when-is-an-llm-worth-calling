import random
import numpy as np
import pytest
from escalation.kanzi_v75 import grid,features,choose,guard
from escalation.kanzi_v74 import TRANSFORMS,ENTROPY
def test_distinct_source_vectors_not_effective_behavior_claim():
    g=grid();assert len(g)==448
    signatures={(sum(TRANSFORMS[t]<<(42-6*i) for i,t in enumerate(c['transform'].split('+'))),ENTROPY[c['entropy']],c['block_bytes']) for c in g}
    assert len(signatures)==448 and {c['jobs'] for c in g}=={1}
    assert np.unique(features(g),axis=0).shape[0]==448
@pytest.mark.parametrize('method',['random','nn','rf_lcb'])
def test_deterministic_and_acquired_only(method):
    x=features(grid());obs=[{'config_id':0,'compressed_bytes':1000},{'config_id':1,'compressed_bytes':900}]
    a=choose(x,obs,method,11,random.Random(11));b=choose(x,obs,method,11,random.Random(11));assert a==b and a not in [0,1]
    polluted=[dict(o,hidden_value=-10000,other_arm_result=7) for o in obs];assert choose(x,polluted,method,11,random.Random(11))==a
@pytest.mark.parametrize('cid,obs,purpose,count',[(448,[],'search',0),(True,[],'search',0),(0,[{'config_id':0}],'search',0),(0,[],'search',200),(0,[{}]*20,'confirmation',0),(0,[],'other',0)])
def test_budget_guards(cid,obs,purpose,count):
    with pytest.raises(ValueError):guard(cid,obs,purpose,count)
def test_charged_confirmation_allowed():guard(0,[{'config_id':0}]*19,'confirmation',199)
