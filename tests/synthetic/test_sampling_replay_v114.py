"""Mutated copies only; no model call or objective acquisition."""
import json,shutil,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from verify_sampling_v114 import verify
from report_sampling_v114 import summarize
@pytest.fixture
def saved(tmp_path):
 # Bind immutable historical prefixes/controls; copy new measured evidence.
 jobs=json.loads((ROOT/'artifacts/study_v114/jobs.json').read_text());names=['artifacts/study_v114/jobs.json','data/manifest_v41.json']
 for j in jobs:names.extend([j['prefix'],f"results/v41_transfer/arms/{j['base_key']}_batch_3nn.json",f"results/v41_transfer/arms/{j['base_key']}_full_sequential_3nn.json"])
 for n in set(names):
  p=tmp_path/n;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(ROOT/n)
 for name in ['v114_reasoning','v114_analysis']:shutil.copytree(ROOT/'results'/name,tmp_path/'results'/name)
 return tmp_path
@pytest.mark.parametrize('kind',['sampling_seed','label','prompt','response','request_count'])
def test_reject_corrupted_replication(saved,kind):
 if kind=='sampling_seed':
  p=saved/'results/v114_analysis/summary.json';d=json.loads(p.read_text());d['cases'][0]['sampling_seed']+=1;p.write_text(json.dumps(d))
 elif kind=='label':
  p=saved/'results/v114_analysis/acquisitions.jsonl';rows=[json.loads(s) for s in p.read_text().splitlines()];rows[0]['raw_target']=str(float(rows[0]['raw_target'])+999);p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
 elif kind=='prompt':
  p=next((saved/'results/v114_reasoning/preflight').glob('*.json'));d=json.loads(p.read_text());d['rendered']['prompt']+='changed';p.write_text(json.dumps(d))
 elif kind=='response':
  p=saved/'results/v114_reasoning/responses.jsonl';rows=[json.loads(s) for s in p.read_text().splitlines()];rows[0]['response']['content']='invalid';p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
 else:
  p=saved/'results/v114_analysis/summary.json';d=json.loads(p.read_text());d['requests']+=1;p.write_text(json.dumps(d))
 with pytest.raises(AssertionError):verify(saved,check_freeze=False)

def test_equal_group_weight_and_no_case_mutation():
 s=json.loads((ROOT/'results/v114_analysis/summary.json').read_text());before=json.dumps(s,sort_keys=True);d=summarize(s)
 assert json.dumps(s,sort_keys=True)==before
 assert len(d['prefixes'])==12 and len(d['groups'])==6
 for a in ['batch_3nn','full_sequential_3nn']:
  assert math.isclose(d['group_first_policy_mean'][a],sum(x[a] for x in d['groups'].values())/6,rel_tol=0,abs_tol=1e-15)
 assert d['valid']+d['fallbacks']==d['intended']==36
