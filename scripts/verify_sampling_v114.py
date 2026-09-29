"""Independent replay:36intended replicas, isolated B20 states and real responses."""
import json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,sha,write
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain
from reasoning_v102_common import audit_case

def lines(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def verify(root=ROOT,check_freeze=True):
 if check_freeze:
  for n,h in read(root/'reports/protocol_v114.freeze.json')['sha256'].items():assert sha(root/n)==h,n
 model=root/'results/v114_reasoning';out=root/'results/v114_analysis';s=read(out/'summary.json');jobs=read(root/'artifacts/study_v114/jobs.json');cases={r['key']:r for r in s['cases']}
 specs={d['id']:d for d in read(root/'data/manifest_v41.json')['datasets']};acqs=lines(out/'acquisitions.jsonl');starts=lines(model/'generation_starts.jsonl');responses=lines(model/'responses.jsonl');sm={r['identity']:r for r in starts};rm={r['key']:r for r in responses}
 assert len(jobs)==len(cases)==36 and len(acqs)==360
 assert len(sm)==len(starts)==s['requests']==s['ledger']['generation_requests']<=36 and len(rm)==len(responses)==s['responses']<=len(starts)
 assert s['ledger']['allocated_output_tokens']==128*len(starts)<=4608 and s['ledger']['retries']==0 and s['ledger']['external_spend_usd']==0
 assert s['ledger']['server_exit_code'] is not None and s['ledger']['stage_seconds']<=1800
 assert {x['key'] for x in jobs}==set(cases)
 for j in jobs:
  r=cases[j['key']];p=read(root/j['prefix']);state=State(**p['state']).clone();arm=read(out/'arms'/f"{j['key']}.json");aa=[a for a in acqs if a['case']==j['key']]
  assert r['optimization_seed']==p['seed']==j['optimization_seed'] and r['sampling_seed']==j['seed']==j['sampling_seed']
  assert len(aa)==10 and r['selected_rows']==[a['row_id'] for a in aa]
  for a in aa:state.observe(a['row_id'],[float(a['raw_target'])],(specs[j['dataset']]['direction'],))
  assert len(state.ids)==len(set(state.ids))==20 and state.record()==arm['state'] and arm['prefix_sha256']==sha(root/j['prefix'])
  value=best(state,specs[j['dataset']]['direction']);assert value==r['target']
  # Verify both strong reference outcomes directly from their saved states.
  for name in ['full_sequential_3nn','batch_3nn']:
   reference=read(root/f"results/v41_transfer/arms/{j['base_key']}_{name}.json")['state']
   assert reference['ids'][:10]==p['state']['ids'] and reference['labels'][:10]==p['state']['labels']
   assert r['references'][name]==best(State(**reference),specs[j['dataset']]['direction'])
  for name,ref in r['references'].items():assert relative_gain(ref,value,specs[j['dataset']]['direction'])==r['gains'][name]
  pf=model/'preflight'/f"{j['key']}.json";cp=model/'choices'/f"{j['key']}.json";choice=read(cp) if cp.exists() else {'status':'unattempted','selected_ids':[]}
  if pf.exists():
   pre=read(pf);assert pre['messages']==p['messages'] and pre['prefix_sha256']==sha(root/j['prefix'])
   parsed=audit_case(j,pre,sm,rm,choice)
   if parsed and parsed['valid']:assert [p['pool']['mapping'][k] for k in parsed['selected_ids']]==r['selected_rows']
  if r['fallback']:
   assert r['selected_rows']==read(root/f"results/v41_transfer/arms/{j['base_key']}_batch_3nn.json")['state']['ids'][10:]
  assert r['fallback']==(r['status']!='completed') and r['charged_requests']==int(j['key']+'_final' in sm)
  assert r['returned_responses']==int(j['key']+'_final' in rm) and r['missing_request_usage']==r['charged_requests']-r['returned_responses']
 for group,means in s['family_means']['nonthinking'].items():
  for key,value in means.items():assert value==statistics.mean(r['gains'][key] for r in cases.values() if r['family']==group)
 return dict(verified=True,intended_conditions=36,prefixes=len({j['base_key'] for j in jobs}),groups=len({j['system_group'] for j in jobs}),saved_acquisitions_replayed=len(acqs),requests=len(starts),responses=len(responses),fallbacks=sum(r['fallback'] for r in cases.values()),new_objective_acquisitions=0,new_model_requests=0)
def main():
 result=verify();write(ROOT/'artifacts/study_v114/replay_verification.json',result);print(json.dumps(result))
if __name__=='__main__':main()
