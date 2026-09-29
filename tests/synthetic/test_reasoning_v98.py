import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from reasoning_v98_common import payload,check_payload,valid_thought,final_prompt,parse_final,END_CONTROL

def test_all_allowed_phases_and_cap_rejection():
    for mode,phase in [('thinking','thought'),('thinking','final'),('nonthinking','final')]:
        p=payload('synthetic fixture',11,mode,phase);check_payload(p)
        p['n_predict']+=1
        with pytest.raises(ValueError):check_payload(p)
    with pytest.raises(ValueError):payload('',11,'nonthinking','thought')

def test_final_prompt_contains_exact_observed_text_and_separate_control():
    r={'content':'synthetic reasoning text','tokens_predicted':512,'truncated':False,'stop_type':'limit'}
    assert valid_thought(r)
    assert final_prompt('prefix',r)=='prefix'+r['content']+END_CONTROL
    for changes in [{'truncated':True},{'stop_type':'eos'},{'tokens_predicted':513},{'content':'</think>'}]:
        assert not valid_thought({**r,**changes})
    assert valid_thought({**r,'stop_type':'word','stopping_word':'</think>'})
    assert not valid_thought({**r,'stop_type':'word','stopping_word':'anything_else'})

def test_final_parser_never_accepts_truncated_or_fabricated_completion():
    r={'content':'\n'.join('0123456789'),'tokens_predicted':20,'truncated':False,'stop_type':'eos'}
    assert parse_final(r)['valid']
    assert not parse_final({**r,'stop_type':'limit'})['valid']
    assert not parse_final({**r,'content':'0\n'*10})['valid']
    assert not parse_final({**r,'content':'Here are my choices:\n'+r['content']})['valid']
