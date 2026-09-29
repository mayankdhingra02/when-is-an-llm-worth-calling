"""Verify saved evidence without acquiring labels or making model requests."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from escalation.io import lines,read,write,now,digest
from escalation.data import read_table,validate_manifest
from escalation.core import State,initial_state,recommend,features
from escalation.evaluator import evaluate

m=read('data/manifest_v3.json');validate_manifest(m);classic=lines('results/v3/classical/runs.jsonl');paired=lines('results/v3/runs.jsonl')
assert len(classic)==30
for d in m['datasets']:
 c,hidden,excluded=read_table(d['path'])
 for run in [r for r in classic+paired if r['dataset']==d['id']]:
  assert run['namespace']=='measured' and run['logical_evaluations']==len(run['ids'])<=20
  assert len(set(run['ids']))==len(run['ids'])
  assert all(tuple(y)==hidden[i] for i,y in zip(run['ids'],run['labels']))
  assert evaluate(hidden,c.directions,run['ids'])['loss']==run['loss']
  if run['status']=='completed':assert len(run['ids'])==20
  if run['method']=='ezr_centroid_adapted':
   p=read(f'results/v3/classical/prefixes/{d["id"]}_{run["seed"]}.json')
   assert digest(p['state'])==p['prefix_hash']==run['prefix_hash']
   state=initial_state(c,run['seed'])
   for i,y in zip(run['ids'],run['labels']):
    assert recommend(c,state)==i
    state.observe(i,y,c.directions)
   z,_=features(c,State(**p['state']),run['seed']);assert z==p['features']
requests=lines('results/v3/requests.jsonl');starts=lines('results/v3/request_starts.jsonl')
assert len(requests)==len(starts) and len(requests)<=100
assert len(set(r['request_id'] for r in requests))==len(requests)
for r in requests:
 assert r['provider']=='local_transformers' and r['revision'] and r['parameters']['max_new_tokens']<=1024
 assert r['wall_seconds']<=181 and r['retry']<=1
 if r['status']=='response':assert r['raw_output'] is not None and r['input_tokens']>0 and r['output_tokens']>0 and r['rendered_prompt_sha256']
for r in paired:
 c=next(x for x in classic if x['method']=='ezr_centroid_adapted' and x['dataset']==r['dataset'] and x['seed']==r['seed'])
 assert r['ids'][:10]==c['ids'][:10] and r['labels'][:10]==c['labels'][:10] and r['prefix_hash']==c['prefix_hash']
write('artifacts/result_verification_v3.json',{'verified':True,'at':now(),'classical_runs':len(classic),'paired_records':len(paired),'requests':len(requests),'checks':['saved labels match table','inclusive budgets','unique acquisitions','prefix equality and hash','deterministic replay from acquired labels without new oracle queries','predecision features replay','offline metric recalculation','real local provenance','request and retry bounds']})
print('Evidence verification passed')
