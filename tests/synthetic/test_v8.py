"""Synthetic only; no measured model responses or performance claims."""
import itertools,json
import pytest
from escalation.core import State
from escalation.finite_domain import FiniteCandidates
from escalation.selection_v8 import shortlist,messages,parse_ids,control_rows
from escalation.grammar_v8 import CandidateIDGrammar

class Tokenizer:
    eos_token_id=1000
    def encode(self,text,**kwargs):return [ord(c) for c in text]
    def decode(self,ids):return ''.join(chr(c) for c in ids)

def fixture():
    xs=tuple(itertools.product([0.,1.],repeat=5))
    c=FiniteCandidates(tuple('abcde'),xs,('time',),('-',),tuple(range(32)))
    s=State(list(range(32)))
    for i in range(10):s.observe(i,[float(i)],c.directions)
    return c,s

def test_shortlist_is_stable_feature_only_and_excludes_acquired():
    c,s=fixture();p=shortlist(c,s,11)
    assert len(p['ranked'])==len(set(p['ranked']))==20
    assert not set(p['ranked'])&set(s.ids)
    assert set(p['mapping'].values())==set(p['ranked'])
    assert p==shortlist(c,s.clone(),11)
    assert p['ranked']==shortlist(c,s,23)['ranked']
    assert p['mapping']!=shortlist(c,s,23)['mapping']
    # Unobserved targets are not part of the candidate object or function API.
    assert set(c.__dict__)=={'names','x','objective_names','directions','source_ids'}
    body=json.loads(messages(c,s,p)[1]['content'].split('\n',1)[1])
    assert len(body['observations'])==10
    assert all(set(r)=={'id','x'} for r in body['candidates'])
    assert all(0<=r['loss']<=1 for r in body['observations'])

def test_controls_share_fixed_pool_and_do_not_mutate_prefix():
    c,s=fixture();before=s.record();p=shortlist(c,s,11)
    for arm in ['uniform_selection','static_rank']:
        rows=control_rows(p,11,arm)
        assert len(rows)==len(set(rows))==10 and set(rows)<=set(p['ranked'])
        assert rows==control_rows(p,11,arm)
    assert control_rows(p,11,'static_rank')==p['ranked'][:10] and s.record()==before
    with pytest.raises(ValueError):control_rows(p,11,'fake_llm')

def test_grammar_enforces_unique_ids_and_complete_output():
    g=CandidateIDGrammar(Tokenizer());tokens=[]
    while len(tokens)<len(g.schedule):tokens.append(g.allowed_after(tokens)[0])
    trace=g.replay(tokens)
    assert [len(r['allowed']) for r in trace]==list(range(20,10,-1))
    assert len(g.choice_positions)==10
    c,s=fixture();p=shortlist(c,s,11)
    assert len(set(parse_ids(Tokenizer().decode(tokens[:-1]),p)))==10
    tokens[g.choice_positions[1]]=tokens[0]
    with pytest.raises(ValueError):g.replay(tokens)
    with pytest.raises(ValueError):g.replay(tokens[:-1])

@pytest.mark.parametrize('raw',['0\n'*10,'\n'.join('012345678Z'),'\n'.join('012345678'),'\n'.join('0123456789')+'\nexplanation'])
def test_malformed_ids_rejected(raw):
    c,s=fixture()
    with pytest.raises(ValueError):parse_ids(raw,shortlist(c,s,11))

def test_checkpoint_and_pool_requirements():
    c,s=fixture();s.ids.pop()
    with pytest.raises(ValueError):shortlist(c,s,11)
    c,s=fixture();s.order=list(range(20))
    with pytest.raises(ValueError):shortlist(c,s,11)

def test_explicit_cap_and_paid_guard(monkeypatch):
    from escalation import study_v8 as module
    from escalation.provider_v8 import SelectionProvider
    monkeypatch.setattr(module,'read',lambda path:{'granted':False,'request_cap':128})
    with pytest.raises(ValueError):module.run_config()
    monkeypatch.setattr(module,'read',lambda path:{'granted':True,'request_cap':128,'user_authorization':None})
    with pytest.raises(ValueError):module.run_config()
    monkeypatch.setattr(module,'read',lambda path:{'granted':False,'request_cap':113})
    cfg=module.run_config();assert cfg['inference']['max_new_model_requests']==113
    cfg['inference']['allow_paid_api']=True
    with pytest.raises(ValueError):SelectionProvider(cfg,None,'unused')

def test_preflight_blocks_full_arm_at_exhausted_cap(monkeypatch,tmp_path):
    from escalation import study_v8 as module
    from escalation.study_v7 import run_config
    monkeypatch.setattr(module,'OUT',tmp_path)
    monkeypatch.setattr(module,'manifest',lambda:{'datasets':[{'id':x} for x in 'abc'],'seeds':[11,23,37,53,71]})
    monkeypatch.setattr(module,'run_config',run_config)
    monkeypatch.setattr(module,'read',lambda path:{'requests':113,'experiment_seconds':1630.,'active_since':None})
    monkeypatch.setattr(module,'write',lambda *args:None)
    check=module.preflight()
    assert not check['ready'] and check['available_requests']==0 and check['pending_requests']==15
