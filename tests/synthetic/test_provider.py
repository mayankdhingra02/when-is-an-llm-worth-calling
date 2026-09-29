import json
import pytest
from escalation.llm import parse,messages
from escalation.core import initial_state
from escalation.config import load_config
from escalation.provider import LocalProvider
from escalation.resources import Resources,LimitReached
from test_integrity import fixture

def test_parser_strict():
    c,_=fixture();assert len(parse(json.dumps({'candidates':[[0]*5,[1]*5]}),c))==2
    for rows in [[[0]*4,[1]*5],[[0]*5],[[2]*5,[1]*5],[[True]*5,[1]*5]]:
        with pytest.raises(ValueError):parse(json.dumps({'candidates':rows}),c)

def test_provider_rejects_paid_before_loading():
    c=load_config();c['inference']['allow_paid_api']=True
    with pytest.raises(ValueError):LocalProvider(c,None,'unused')

def test_cap_persists_and_concurrency_lock(tmp_path):
    c=load_config();c['inference']['max_new_model_requests']=1;p=tmp_path/'ledger.json'
    with Resources(c,p) as r:
        assert r.request()==1
        with pytest.raises(LimitReached):r.request()
        with pytest.raises(LimitReached):
            with Resources(c,p):pass
    with Resources(c,p) as r:
        with pytest.raises(LimitReached):r.request()

def test_runtime_cap(tmp_path):
    c=load_config();c['resources']['max_experiment_runtime_minutes']=0
    with Resources(c,tmp_path/'ledger.json') as r:
        with pytest.raises(LimitReached):r.check()
