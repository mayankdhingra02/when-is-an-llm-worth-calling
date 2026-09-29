"""Synthetic capacity/provider regressions, excluded from measured aggregates."""
import json,sys,string,copy
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from proposal_v128 import capacity,grammar,payload,parse,MAX_OUTPUT
from runtime_proposal_v128 import Runtime

TOKENS=list(string.printable)
DS=[[0,1]]*17
def cfg():return {'allow_paid_api':False,'allow_cloud':False,'max_external_spend_usd':0,'retries':0,'max_generation_stage_seconds':900,'scientific_request_cap':1,'compatibility_request_cap':0,'new_generation_request_cap':1,'max_allocated_output_tokens':1024}

def test_v127_sac_error_prevented_before_generation():
    with pytest.raises(ValueError,match='capacity'):capacity([[0,1]]*59,TOKENS,100,512)
    assert capacity([[0,1]]*59,TOKENS,100)['constructive_token_upper_bound_including_eos']==622

def test_context_includes_full_reserved_output():
    assert capacity(DS,TOKENS,3072)['prompt_tokens']==3072
    with pytest.raises(ValueError,match='context'):capacity(DS,TOKENS,3073)

def test_missing_vocab_and_invalid_domain_fail_closed():
    with pytest.raises(ValueError,match='vocabulary'):capacity(DS,['0','1'],100)
    for ds in [[],[[]],[list(range(63))]]:
        with pytest.raises(ValueError):capacity(ds,TOKENS,100)

def test_grammar_is_bounded_and_capacity_matches_actual_ascii_width():
    assert '*' not in grammar(DS) and 'ws' not in grammar(DS)
    s=json.dumps(['0'*17]*10,separators=(',',':'))
    assert len(s)==capacity(DS,TOKENS,100)['maximum_output_ascii_bytes']==201
    r={'content':s,'truncated':False,'stop_type':'eos','tokens_predicted':202}
    assert parse(r,DS)==[(0,)*17]*10
    with pytest.raises(ValueError):parse({**r,'content':json.dumps(['0'*17]*10)},DS)

def test_provider_cannot_bypass_preflight_and_binds_payload(tmp_path):
    rt=Runtime(tmp_path,cfg());p=payload('fixture',11,DS);sent=[]
    rt._send=lambda *a:sent.append(a)
    with pytest.raises(PermissionError,match='preflight'):rt.generate(p,'scientific','fake')
    assert rt.ledger['generation_requests']==0 and not sent
    rt.authorize(p,DS,TOKENS,100)
    q={**p,'prompt':'different'}
    with pytest.raises(PermissionError):rt.generate(q,'scientific','fake')
    rt.generate(p,'scientific','fake');assert len(sent)==1 and rt.ledger['allocated_output_tokens']==1024
    with pytest.raises(PermissionError):rt.generate(p,'scientific','fake')

def test_grammar_identity_checked_before_authorizing(tmp_path):
    rt=Runtime(tmp_path,cfg());p=payload('fixture',11,DS);p['grammar']+='ws ::= [ ]*\n'
    with pytest.raises(ValueError,match='mismatch'):rt.authorize(p,DS,TOKENS,100)
    assert not rt.authorized

def test_failed_transport_is_charged_after_valid_preflight(tmp_path):
    rt=Runtime(tmp_path,cfg());p=payload('fixture',11,DS);rt.authorize(p,DS,TOKENS,100)
    def fail(*a):raise OSError('synthetic failure')
    rt._send=fail
    with pytest.raises(OSError):rt.generate(p,'scientific','fake')
    assert rt.ledger['generation_requests']==1 and rt.ledger['allocated_output_tokens']==1024
