import importlib.util,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from runtime_reasoning_v100 import Runtime
from reasoning_v98_common import payload

def test_loading_is_only_server_command_change():
    old=(ROOT/'scripts/runtime_reasoning_v99.py').read_text()
    new=(ROOT/'scripts/runtime_reasoning_v100.py').read_text()
    assert new.replace("'--load-mode','none',",'')==old
    jobs=json.loads((ROOT/'artifacts/study_v100/jobs.json').read_text())
    assert jobs==json.loads((ROOT/'artifacts/study_v99/jobs.json').read_text())[:2]

def test_request_cap_prevents_fourth_send(tmp_path):
    cfg=json.loads((ROOT/'configs/study_v100.json').read_text())
    rt=Runtime(tmp_path,cfg);calls=[]
    rt._send=lambda *args:calls.append(args)
    rt.generate(payload('fixture',11,'nonthinking','final'),'scientific','synthetic_a')
    rt.generate(payload('fixture',71,'thinking','thought'),'scientific','synthetic_b')
    rt.generate(payload('fixture',71,'thinking','final'),'scientific','synthetic_c')
    assert rt.ledger['allocated_output_tokens']==768 and len(calls)==3
    with pytest.raises(PermissionError):rt.generate(payload('fixture',71,'thinking','final'),'scientific','synthetic_d')
    assert len(calls)==3
    rt.close()

def test_output_cap_prevents_excess_thought_request(tmp_path):
    cfg=json.loads((ROOT/'configs/study_v100.json').read_text());rt=Runtime(tmp_path,cfg)
    rt._send=lambda *args:None
    rt.generate(payload('fixture',71,'thinking','thought'),'scientific','synthetic_a')
    with pytest.raises(PermissionError):rt.generate(payload('fixture',71,'thinking','thought'),'scientific','synthetic_b')
    assert rt.ledger['generation_requests']==1
    rt.close()
