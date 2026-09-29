"""Acquire one120-label portfolio study, preserving old traces and all12prefixes."""
import json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,write,append,sha
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict,IndexedOracle,best,relative_gain
from portfolio_v115 import portfolio
OUT=ROOT/'results/v115_portfolio'
def main():
 for n,h in read(ROOT/'reports/protocol_v115.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 assert not OUT.exists();OUT.mkdir();os.chdir(ROOT);start=time.monotonic();accesses=0;arms=[]
 jobs=read(ROOT/'artifacts/study_v115/jobs.json');assert len(jobs)==12
 specs={d['id']:d for d in read(ROOT/'data/manifest_v41.json')['datasets']};old={r['key']:r for r in read(ROOT/'results/v91_analysis/cases.json')}
 for job in jobs:
  p=read(ROOT/job['prefix']);spec=specs[job['dataset']];c=restrict(load_candidates(spec),spec['fixed_features'])[0];prefix=State(**p['state']).clone()
  oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',dict(case=job['base_key'],**e)))
  def acquire(row):
   nonlocal accesses
   if accesses>=120:raise RuntimeError('120new-acquisition cap')
   if time.monotonic()-start>1795:raise TimeoutError('stage limit')
   accesses+=1;return oracle.acquire(row)
  t=time.perf_counter();state,trace=portfolio(c,prefix,p['pool']['ranked'],acquire);seconds=time.perf_counter()-t
  assert prefix.record()==p['state'] and oracle.new_accesses==10
  target=best(state,c.directions[0]);base=old[job['base_key']]
  row=dict(key=job['base_key'],family=job['system_group'],optimization_seed=job['optimization_seed'],state=state.record(),trace=trace,prefix_sha256=sha(ROOT/job['prefix']),logical_evaluations=20,new_acquisitions=10,target=target,direction=c.directions[0],portfolio_loop_seconds=seconds,references={a:base['references'][a] for a in ['batch_3nn','full_sequential_3nn']})
  row['portfolio_gains']={a:relative_gain(v,target,c.directions[0]) for a,v in row['references'].items()}
  write(OUT/'arms'/f"{job['base_key']}.json",row);arms.append(row)
 result=dict(intended=12,completed=len(arms),new_acquisitions=accesses,new_model_requests=0,stage_seconds=time.monotonic()-start,arms=arms,external_spend_usd=0)
 write(OUT/'summary.json',result);print(json.dumps({k:v for k,v in result.items() if k!='arms'}))
if __name__=='__main__':main()
