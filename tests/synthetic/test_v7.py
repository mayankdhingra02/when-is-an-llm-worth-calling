import itertools,json
from pathlib import Path
import pytest
from escalation.grammar_v7 import PrefixExcludingGrammar,uniform_without_prefix
from escalation.finite_v6 import ALPHABET

class Tokenizer:
    eos_token_id=1000
    def encode(self,text,**kwargs):return [ord(c) for c in text]
    def decode(self,ids):return ''.join(chr(c) for c in ids)

def test_exhaustive_constraints_never_forbid_valid_completion():
    domains=[[0,1],[0],[0,1,2]];forbidden=['000','002','101']
    g=PrefixExcludingGrammar(Tokenizer(),domains,forbidden)
    allowed_rows={''.join(x) for x in itertools.product('01','0','012')}-set(forbidden)
    for length in range(3):
        for prefix in {r[:length] for r in allowed_rows}:
            expected={ord(r[length]) for r in allowed_rows if r.startswith(prefix)}
            assert set(g.allowed_after(list(map(ord,prefix))))==expected
    # Full legal generation, including fixed suffix, newline, EOS and all ten rows.
    generated=[]
    while len(generated)<len(g.schedule):generated.append(min(g.allowed_after(generated)))
    raw=Tokenizer().decode(generated[:-1]);assert not set(raw.splitlines())&set(forbidden)
    assert len(raw.splitlines())==10 and g.replay(generated)
    bad=list(generated);bad[:3]=list(map(ord,'000'))
    with pytest.raises(ValueError):g.replay(bad)

def test_no_exclusion_when_prefix_diverges():
    g=PrefixExcludingGrammar(Tokenizer(),[[0,1]]*4,['0000','0001'])
    assert g.allowed_after([ord('1')])==[ord('0'),ord('1')]
    assert g.allowed_after([ord('0'),ord('0')])==[ord('1')]

def test_all_forbidden_and_constant_tail():
    with pytest.raises(ValueError):PrefixExcludingGrammar(Tokenizer(),[[0]],['0'])
    g=PrefixExcludingGrammar(Tokenizer(),[[0,1],[0],[0]],['000'])
    assert g.allowed_after([])==[ord('1')]
    with pytest.raises(ValueError):PrefixExcludingGrammar(Tokenizer(),[[0,1]],['2'])

def test_uniform_complement_dense_space():
    domains=[[10,20],[0],[3,7,9]];forbidden=['000','001','002','100','101']
    result=uniform_without_prefix(domains,forbidden,11,100)
    assert result==[[20,0,9]]*100
    assert uniform_without_prefix([[0,1]]*4,['0000'],23)==uniform_without_prefix([[0,1]]*4,['0000'],23)
    with pytest.raises(ValueError):uniform_without_prefix([[0]],['0'],11)

def test_uniform_sampler_feature_only_and_repeated_novel_allowed():
    result=uniform_without_prefix([[0,1]]*2,['00'],37,1000)
    counts={tuple(x):result.count(x) for x in result}
    assert set(counts)=={(0,1),(1,0),(1,1)}
    assert all(250<n<420 for n in counts.values())

def test_full_arm_preflight_blocks_without_spending(monkeypatch,tmp_path):
    from escalation import study_v7 as module
    from escalation.config import load_config
    monkeypatch.setattr(module,'OUT',tmp_path)
    monkeypatch.setattr(module,'manifest',lambda:{'datasets':[{'id':x} for x in ['synthetic_a','synthetic_b','synthetic_c']],'seeds':[11,23,37,53,71]})
    monkeypatch.setattr(module,'run_config',lambda:load_config('configs/followup_v3.yaml'))
    monkeypatch.setattr(module,'read',lambda p:{'requests':98,'experiment_seconds':1471.,'active_since':None})
    saved=[];monkeypatch.setattr(module,'write',lambda p,v:saved.append(v))
    result=module.preflight()
    assert result['pending_requests']==15 and result['available_requests']==2 and not result['ready']
    assert len(saved)==1

def test_explicit_authorization_record_is_required(monkeypatch):
    from escalation import study_v7 as module
    monkeypatch.setattr(module,'read',lambda p:{'granted':False,'request_cap':113})
    with pytest.raises(ValueError):module.run_config()
    monkeypatch.setattr(module,'read',lambda p:{'granted':True,'request_cap':113,'user_authorization':None})
    with pytest.raises(ValueError):module.run_config()

def test_new_provider_keeps_paid_guard():
    from escalation.provider_v7 import NoCopyProvider
    from escalation.config import load_config
    cfg=load_config('configs/followup_v3.yaml');cfg['inference']['allow_paid_api']=True
    with pytest.raises(ValueError):NoCopyProvider(cfg,None,'unused')
