from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from reasoning_v95_common import parse,check_payload,applied_settings

def response(content):return dict(content=content,tokens_predicted=30,truncated=False,stopped_limit=False)
ANSWER='\n'.join('0123456789')

def test_thinking_requires_complete_delimiter_and_exact_answer():
    assert parse(response('some thoughts</think>\n'+ANSWER),'thinking')['valid']
    assert not parse(response('some thoughts '+ANSWER),'thinking')['valid']
    assert not parse(response('thoughts</think>Answer: '+ANSWER),'thinking')['valid']
    assert not parse(response('x</think>x</think>'+ANSWER),'thinking')['valid']

def test_truncation_duplicates_and_explanations_rejected():
    r=response(ANSWER);r['stopped_limit']=True
    assert not parse(r,'nonthinking')['valid']
    assert not parse(response('\n'.join('0012345678')),'nonthinking')['valid']
    assert not parse(response(ANSWER+'\nBecause'),'nonthinking')['valid']

def payload():return dict(n_predict=2048,temperature=.6,top_p=.95,top_k=20,min_p=0.,presence_penalty=1.5,repeat_penalty=1.,stream=False,cache_prompt=False,return_tokens=True,seed=11)

def test_sampler_guard_and_runtime_readback():
    p=payload();check_payload(p);applied_settings({'generation_settings':p},p)
    with pytest.raises(ValueError):check_payload({**p,'temperature':0})
    with pytest.raises(ValueError):check_payload({**p,'grammar':'root ::= "A"'})
    with pytest.raises(ValueError):applied_settings({'generation_settings':{**p,'presence_penalty':0}},p)
