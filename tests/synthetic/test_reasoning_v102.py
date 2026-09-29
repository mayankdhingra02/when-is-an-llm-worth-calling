import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from reasoning_v102_common import payload,check_payload,valid_thought,final_prompt
from runtime_reasoning_v102 import Runtime

def test_only_thought_and_total_output_caps_change():
    old=json.loads((ROOT/'configs/study_v101.json').read_text());new=json.loads((ROOT/'configs/study_v102.json').read_text())
    assert {k for k in old if old[k]!=new[k]}=={'stage','thinking_output_cap','max_allocated_output_tokens'}
    assert new['thinking_output_cap']==128 and new['final_output_cap']==128
    assert (ROOT/'artifacts/study_v102/jobs.json').read_bytes()==(ROOT/'artifacts/study_v101/jobs.json').read_bytes()

def test_equal_length_phases_stay_distinct_and_long_thought_rejected():
    thought=payload('fixture',71,'thinking','thought');final=payload('fixture',71,'thinking','final')
    assert thought['n_predict']==final['n_predict']==128 and 'stop' in thought and 'stop' not in final
    check_payload(thought);check_payload(final)
    with pytest.raises(ValueError):check_payload({**thought,'n_predict':512})
    r={'content':'synthetic thought','tokens_predicted':128,'truncated':False,'stop_type':'limit'}
    assert valid_thought(r) and final_prompt('prefix',r)=='prefixsynthetic thought\n</think>\n\n'
    assert not valid_thought({**r,'tokens_predicted':129})

def test_three_request_budget_and_no_fourth_request(tmp_path):
    cfg=json.loads((ROOT/'configs/study_v102.json').read_text());rt=Runtime(tmp_path,cfg);calls=[]
    rt._send=lambda *args:calls.append(args)
    for mode,phase in [('nonthinking','final'),('thinking','thought'),('thinking','final')]:rt.generate(payload('fixture',71,mode,phase),'scientific',mode+phase)
    assert len(calls)==3 and rt.ledger['allocated_output_tokens']==384
    with pytest.raises(PermissionError):rt.generate(payload('fixture',71,'thinking','final'),'scientific','extra')
    assert len(calls)==3;rt.close()
