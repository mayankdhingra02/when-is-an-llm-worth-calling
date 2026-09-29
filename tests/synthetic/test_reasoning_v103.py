import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from runtime_reasoning_v103 import Runtime
from reasoning_v102_common import payload

def test_cohort_is_all_groups_two_preselected_seeds_in_original_order():
    jobs=json.loads((ROOT/'artifacts/study_v103/jobs.json').read_text())
    old=json.loads((ROOT/'artifacts/study_v99/jobs.json').read_text())
    assert jobs==[j for j in old if j['seed'] in [11,37]]
    assert len(jobs)==24 and len({j['base_key'] for j in jobs})==12
    assert len({j['system_group'] for j in jobs})==6
    for group in {j['system_group'] for j in jobs}:
        assert {(j['seed'],j['mode']) for j in jobs if j['system_group']==group}=={(s,m) for s in [11,37] for m in ['thinking','nonthinking']}

def test_full_cohort_caps_and_unchanged_inference(tmp_path):
    cfg=json.loads((ROOT/'configs/study_v103.json').read_text());rt=Runtime(tmp_path,cfg);calls=[];rt._send=lambda *args:calls.append(args)
    assert cfg['max_generation_stage_seconds']==1800 and cfg['max_new_recorded_objective_acquisitions']==240
    for seed in range(12):
        for mode,phase in [('thinking','thought'),('thinking','final'),('nonthinking','final')]:rt.generate(payload('fixture',seed,mode,phase),'scientific',str(seed)+mode+phase)
    assert len(calls)==36 and rt.ledger['allocated_output_tokens']==4608
    with pytest.raises(PermissionError):rt.generate(payload('fixture',71,'thinking','final'),'scientific','extra')
    assert len(calls)==36;rt.close()
    assert (ROOT/'scripts/runtime_reasoning_v103.py').read_bytes()==(ROOT/'scripts/runtime_reasoning_v102.py').read_bytes()
