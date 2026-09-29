import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_restart_attempt_changes_only_stage_and_output_paths():
    old=json.loads((ROOT/'configs/study_v100.json').read_text())
    new=json.loads((ROOT/'configs/study_v101.json').read_text())
    assert {k for k in old if old[k]!=new[k]}=={'stage'}
    assert (ROOT/'scripts/runtime_reasoning_v101.py').read_bytes()==(ROOT/'scripts/runtime_reasoning_v100.py').read_bytes()
    assert (ROOT/'scripts/collect_reasoning_v101.py').read_text().replace('v101','v100')==(ROOT/'scripts/collect_reasoning_v100.py').read_text()
    assert (ROOT/'artifacts/study_v101/jobs.json').read_bytes()==(ROOT/'artifacts/study_v100/jobs.json').read_bytes()
