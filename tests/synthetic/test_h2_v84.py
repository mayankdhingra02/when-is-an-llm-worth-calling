import pytest
from escalation.h2_v84 import CONFIGS,PRIOR,choose,prefix_choice,incumbent,guard,features

def test_domain_and_prefix():
    assert len(CONFIGS)==336 and features().shape==(336,11)
    assert prefix_choice([],11)==PRIOR
    obs=[dict(config_id=PRIOR,query_seconds=1.)]
    assert prefix_choice(obs,11)==prefix_choice(obs,11)!=PRIOR

def test_rf_uses_only_acquired_values():
    obs=[dict(config_id=i,query_seconds=1+i/10) for i in range(10)]
    a=choose(obs,'rf_lcb',23)
    assert a>=10 and a==choose(obs,'rf_lcb',23)
    obs2=[dict(o,hidden_unacquired_label=-9999,other_branch_outcome=1e9) for o in obs]
    assert choose(obs2,'rf_lcb',23)==a

def test_budget_reliability_charges():
    obs=[dict(config_id=i,query_seconds=1.) for i in range(20)]
    for purpose in ['search','confirmation','fixed_prior']:
        with pytest.raises(ValueError):guard(100,obs,purpose)
    with pytest.raises(ValueError):guard(0,obs[:10],'search')
    with pytest.raises(ValueError):guard(0,obs[:10],'confirmation')
    guard(0,obs[:17],'confirmation')

def test_incumbent_and_branch_isolation():
    prefix=[dict(config_id=2,query_seconds=2.),dict(config_id=1,query_seconds=1.)]
    a=prefix+[dict(config_id=3,query_seconds=.5)];b=list(prefix)
    assert incumbent(a)==3 and incumbent(b)==1 and len(prefix)==2
