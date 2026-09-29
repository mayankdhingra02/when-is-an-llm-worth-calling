"""Synthetic mutations of copied real records; never experimental responses."""
import copy,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from reasoning_v102_common import audit_case

def fixture():
    raw=ROOT/'results/v103_reasoning'
    jobs=json.loads((ROOT/'artifacts/study_v103/jobs.json').read_text())
    starts={r['identity']:r for r in map(json.loads,(raw/'generation_starts.jsonl').read_text().splitlines())}
    responses={r['key']:r for r in map(json.loads,(raw/'responses.jsonl').read_text().splitlines())}
    job=next(j for j in jobs if j['mode']=='thinking' and json.loads((raw/'choices'/f"{j['key']}.json").read_text())['status']=='completed')
    key=job['key'];pre=json.loads((raw/'preflight'/f'{key}.json').read_text());choice=json.loads((raw/'choices'/f'{key}.json').read_text())
    return job,pre,starts,responses,choice

@pytest.mark.parametrize('mutation',['thought_text','final_prompt','selected_ids'])
def test_saved_lineage_rejects_synthetic_corruption(mutation):
    data=copy.deepcopy(fixture());job,pre,starts,responses,choice=data
    assert audit_case(*data)['valid']
    if mutation=='thought_text':responses[job['key']+'_thought']['response']['content']+=' synthetic alteration'
    elif mutation=='final_prompt':starts[job['key']+'_final']['payload']['prompt']+=' synthetic alteration'
    else:choice['selected_ids']=list(reversed(choice['selected_ids']))
    with pytest.raises(AssertionError):audit_case(*data)
