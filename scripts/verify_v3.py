"""Audit v2 real generations, constrained choices and paired budgets offline."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from escalation.io import read,lines,write,now,digest
from escalation.data import read_table,sha
from escalation.evaluator import evaluate
from escalation.llm import parse
from escalation.core import State,project
from escalation.followup_v3 import compact_messages,parse_bits
from transformers import AutoTokenizer
root=Path(__file__).resolve().parents[1]
import os
os.chdir(root)
manifest=read('results/v3/manifest.json')
assert manifest['protocol_sha256']==sha('reports/protocol_v3.md')==Path('reports/protocol_v3.sha256').read_text().strip()
for path,expected in manifest['code_hashes'].items():assert sha(Path('results/v3/source_snapshot')/path)==expected
classical_manifest=read('results/v3/classical/manifest.json')
for path,expected in classical_manifest['code_hashes'].items():assert sha(Path('results/v3/classical/source_snapshot')/path)==expected
req=lines('results/v3/requests.jsonl');runs=lines('results/v3/runs.jsonl');gate=read('results/v3/feasibility/gate.json')
assert len(req)<=100 and len(req)==len(set(r['request_id'] for r in req))
assert len(runs)==15 if gate['passed'] else len(runs)==0
assert all(r['namespace']=='measured' for r in runs)
assert len([r for r in req if r['stage']=='format_gate'])==3
assert all(r['stage']=='paired' for r in req if r['namespace']=='measured')
t=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
for r in req:
 if r['status']!='response':continue
 assert t.decode(r['generated_token_ids'],skip_special_tokens=True)==r['raw_output']
 assert len(r['generated_token_ids'])==len(r['grammar_schedule'])==r['output_tokens']
 assert all(token in allowed for token,allowed in zip(r['generated_token_ids'],r['grammar_schedule']))
 assert len(r['model_choice_positions'])==5*len(r['grammar_domains'])
 assert r['provider']=='local_transformers' and r['revision']=='7ae557604adf67be50417f59c2c2f167def9a775'
 assert r['wall_seconds']<=61
for d in read('data/manifest_v3.json')['datasets']:
 c,hidden,_=read_table(d['path'])
 for run in [r for r in runs if r['dataset']==d['id']]:
  prefix=read(f'results/v3/classical/prefixes/{d["id"]}_{run["seed"]}.json')
  assert run['ids'][:10]==prefix['state']['ids'] and run['prefix_hash']==prefix['prefix_hash']
  assert len(run['ids'])==len(set(run['ids']))==run['logical_evaluations']<=20
  assert run['actual_new_accesses']==len(run['ids'])-10
  assert all(tuple(label)==hidden[i] for label,i in zip(run['labels'],run['ids']))
  assert evaluate(hidden,c.directions,run['ids'])['loss']==run['loss']
  state=State(**prefix['state']);expected=[];collisions=[]
  for response in [r for r in req if r.get('dataset')==d['id'] and r.get('seed')==run['seed'] and r['status']=='response']:
   assert response['messages']==compact_messages(c,state,collisions)
   proposals=parse_bits(response['raw_output'],c);next_collisions=[]
   for proposal in proposals:
    i,event=project(c,state,proposal)
    if event['collision']:next_collisions.append([int(v) for v in c.x[event['nearest_seen']]])
    expected.append(i);state.observe(i,hidden[i],c.directions)
   collisions=next_collisions
  assert expected==run['ids'][10:]
  if run['status']=='completed':assert len(expected)==10 and run['requests']==2
write('artifacts/verification_v3.json',{'verified':True,'at':now(),'requests':len(req),'paired_records':len(runs),'completed_pairs':sum(r['status']=='completed' for r in runs),'checks':['protocol/source snapshots','real local provenance','raw text matches generated tokens','every generated token satisfies grammar','choice slots left to model','strict parse','same saved prefix','feature-only projection replay','20 inclusive labels','recorded objectives match tables','offline scores','synthetic gate excluded from quality']})
print('V3 evidence verified:',len(req),'requests,',len(runs),'paired records')
