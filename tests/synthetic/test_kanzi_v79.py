import pytest
from escalation.kanzi_v75 import grid,features,choose as rf
from escalation.kanzi_v79 import choose,guard,PRESET_IDS

def test_preset_order_and_source_pair():
    assert PRESET_IDS==tuple(range(439,431,-1))
    assert {grid()[i]['entropy'] for i in PRESET_IDS}=={'CM'}
    assert {grid()[i]['transform'] for i in PRESET_IDS}=={'LZP+TEXT+BWT+LZP'}

def test_skips_acquired_preset_and_ignores_outcomes_for_unseen_preset():
    x=features(grid())
    for y in [1,10000]:
        obs=[{'config_id':439,'compressed_bytes':y}]
        assert choose(x,obs,'preset',11)==438

def test_exhausted_preset_uses_acquired_only_rf():
    x=features(grid());obs=[{'config_id':i,'compressed_bytes':100+i} for i in PRESET_IDS]
    assert choose(x,obs,'preset',11)==rf(x,obs,'rf_lcb',11)

@pytest.mark.parametrize('cid,purpose,count,length',[(448,'search',0,0),(True,'search',0,0),(2,'x',0,0),(2,'search',450,0),(2,'search',0,20),(1,'search',0,1)])
def test_budget_and_proposal_rejection(cid,purpose,count,length):
    with pytest.raises(ValueError):guard(cid,[{'config_id':1}]*length,purpose,count)

def test_confirmation_is_charged_and_allowed_duplicate():
    guard(1,[{'config_id':1}]*19,'confirmation',449)
