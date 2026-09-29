"""Synthetic V93 safety/format guards; excluded from research records."""
import json
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from decoder_v93_common import check_payload, validate, parse_native

@pytest.mark.parametrize('payload',[
    {'n_predict':129,'temperature':0,'stream':False},
    {'n_predict':128,'temperature':0,'stream':False,'grammar':'root ::= "A"'},
    {'n_predict':1,'temperature':0,'stream':False},
    {'n_predict':128,'temperature':1,'stream':False},
    {'n_predict':128,'temperature':0,'stream':True},
])
def test_changed_native_or_control_protocol_rejected(payload):
    with pytest.raises(ValueError):check_payload(payload)

@pytest.mark.parametrize('key,value',[
    ('new_generation_request_cap',145),('max_generated_tokens',7003),
    ('allow_paid_api',True),('host','example.org'),('retries',1),
    ('max_generation_stage_seconds',1801),('max_server_rss_bytes',8589934593),
])
def test_budget_expansion_rejected(key,value):
    cfg=json.loads((ROOT/'configs/study_v93.json').read_text());cfg[key]=value
    with pytest.raises(ValueError):validate(cfg)

def test_partial_but_plausible_response_remains_invalid():
    parsed=parse_native('\n'.join('0123456789'),truncated=True)
    assert not parsed['valid'] and parsed['selected_ids']==[] and parsed['reasons']==['truncated']

def test_native_output_is_not_repaired():
    parsed=parse_native('\n'.join('id'+c for c in '0123456789'))
    assert not parsed['valid'] and parsed['selected_ids']==[]
