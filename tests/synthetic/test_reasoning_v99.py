import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_context_repeat_keeps_method_order_and_guards():
    old=json.loads((ROOT/'configs/study_v98.json').read_text())
    new=json.loads((ROOT/'configs/study_v99.json').read_text())
    assert {k for k in old if old[k]!=new[k]}=={'stage','context_tokens'}
    assert new['context_tokens']==4096
    assert (ROOT/'artifacts/study_v98/jobs.json').read_bytes()==(ROOT/'artifacts/study_v99/jobs.json').read_bytes()
    assert "'-c','4096'" in (ROOT/'scripts/runtime_reasoning_v99.py').read_text()

def test_saved_prefixes_fit_declared_reserve_without_new_inference():
    paths=list((ROOT/'results/v98_reasoning/preflight').glob('*.json'))
    assert len(paths)==36
    assert max(len(json.loads(p.read_text())['prompt_tokens']) for p in paths)+512+128+16<=4096
