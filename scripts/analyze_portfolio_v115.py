"""Independently replay the single budget-matched control and pair every replica."""
import csv,json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,write,sha
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict,rank,best,relative_gain

def verify(root=ROOT,check_freeze=True):
 if check_freeze:
  for n,h in read(root/'reports/protocol_v115.freeze.json')['sha256'].items():assert sha(root/n)==h,n
 out=root/'results/v115_portfolio';s=read(out/'summary.json');jobs=read(root/'artifacts/study_v115/jobs.json');specs={x['id']:x for x in read(root/'data/manifest_v41.json')['datasets']}
 events=[json.loads(x) for x in (out/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==s['new_acquisitions']==120 and s['intended']==s['completed']==12
 arms={};cursor=0
 for j in jobs:
  p=read(root/j['prefix']);spec=dict(specs[j['dataset']]);spec['path']=str(root/spec['path']);c=restrict(load_candidates(spec),spec['fixed_features'])[0];state=State(**p['state']).clone();fixed=rank(c,state,p['pool']['ranked']);trace=[]
  for step in range(10):
   row=next(i for i in fixed if i not in state.ids) if step%2==0 else rank(c,state,[i for i in state.order if i not in state.ids])[0]
   e=events[cursor];cursor+=1;assert e['case']==j['base_key'] and e['row_id']==row
   y=[float(e['raw_target'])];state.observe(row,y,c.directions);trace.append(dict(turn=step,mode='batch' if step%2==0 else 'sequential',row=row,label=y))
  arm=read(out/'arms'/f"{j['base_key']}.json");assert arm['state']==state.record() and arm['trace']==trace and arm['prefix_sha256']==sha(root/j['prefix'])
  assert arm['logical_evaluations']==len(state.ids)==20 and arm['new_acquisitions']==10 and arm['target']==best(state,c.directions[0])
  assert state.ids[:10]==p['state']['ids'] and state.labels[:10]==p['state']['labels']
  for a,value in arm['references'].items():
   ref=read(root/f"results/v41_transfer/arms/{j['base_key']}_{a}.json")['state'];assert ref['ids'][:10]==p['state']['ids'] and ref['labels'][:10]==p['state']['labels']
   assert value==best(State(**ref),c.directions[0]) and relative_gain(value,arm['target'],c.directions[0])==arm['portfolio_gains'][a]
  assert arm==next(x for x in s['arms'] if x['key']==j['base_key']);arms[j['base_key']]=arm
 assert cursor==120
 rows=[]
 for r in read(root/'results/v114_analysis/summary.json')['cases']:
  a=arms[r['base_key']]
  rows.append(dict(key=r['key'],base_key=r['base_key'],family=r['family'],optimization_seed=r['optimization_seed'],sampling_seed=r['sampling_seed'],fallback=r['fallback'],llm_target=r['target'],portfolio_target=a['target'],gain=relative_gain(a['target'],r['target'],a['direction'])))
 assert len(rows)==36
 # First average replicas within prefix; then prefixes within system.
 prefix_means={key:statistics.mean(r['gain'] for r in rows if r['base_key']==key) for key in arms}
 groups={g:statistics.mean(prefix_means[k] for k,a in arms.items() if a['family']==g) for g in sorted({r['family'] for r in rows})}
 control_groups={g:{c:statistics.mean(a['portfolio_gains'][c] for a in arms.values() if a['family']==g) for c in ['batch_3nn','full_sequential_3nn']} for g in groups}
 return dict(verified=True,scope='exploratory post-V114 single-portfolio follow-up; not the original joint-control criterion',new_recorded_acquisitions=120,new_model_requests=0,logical_budget=20,prefixes=12,replica_comparisons=36,groups=groups,group_first_mean=statistics.mean(groups.values()),wins=sum(r['gain']>0 for r in rows),ties=sum(r['gain']==0 for r in rows),losses=sum(r['gain']<0 for r in rows),maximum_gain=max(r['gain'] for r in rows),valid_useful_at_5pct=sum(not r['fallback'] and r['gain']>=.05 for r in rows),policy_harmful_at_5pct=sum(r['gain']<=-.05 for r in rows),threshold_grid=[dict(margin=t,valid_gain_ge=sum(not r['fallback'] and r['gain']>=t for r in rows),valid_gain_strict_gt=sum(not r['fallback'] and r['gain']>t for r in rows)) for t in [0,.02,.05,.1]],portfolio_gains_vs_old_controls=control_groups,cases=rows,collection_stage_seconds=s['stage_seconds'],mean_portfolio_loop_seconds=statistics.mean(a['portfolio_loop_seconds'] for a in arms.values()),new_acquisitions_on_replay=0)

def main():
 d=verify();out=ROOT/'results/v115_analysis';out.mkdir(exist_ok=True);write(out/'summary.json',d)
 with (out/'contrasts.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(d['cases'][0]));w.writeheader();w.writerows(d['cases'])
 text=['# V115: a single deployable classical portfolio','',f"Completed12budget-20classical continuations using the same fixed prefixes as V114, acquiring120new recorded outcomes. The remaining ten turns alternate batch3NN and full-domain sequential3NN; no other branch's outcomes are consulted. This is one executable control, not a free hindsight choice between separately run controls.",'',f"Against this control, the36saved real LLM replicas have group-first mean gain **{d['group_first_mean']:+.2%}**; **{d['valid_useful_at_5pct']}/36** valid replicas improve by>=5%, and **{d['policy_harmful_at_5pct']}/36** are worse by>=5%. There are{d['wins']}wins,{d['ties']}ties and{d['losses']}losses; the largest gain is{d['maximum_gain']:.2%}. {next(x['valid_gain_ge'] for x in d['threshold_grid'] if x['margin']==.02)} replicas improve by at least2%, so the result is not an absence of all benefit. No new model calls occurred. All twelve prefixes and thirty-six replicas are retained.",'','|Group|Mean LLM gain vs portfolio|Portfolio gain vs batch3NN|Portfolio gain vs sequential3NN|','|---|---:|---:|---:|']
 for g,v in d['groups'].items():text.append(f"|{g}|{v:+.2%}|{d['portfolio_gains_vs_old_controls'][g]['batch_3nn']:+.2%}|{d['portfolio_gains_vs_old_controls'][g]['full_sequential_3nn']:+.2%}|")
 text+=['',f"Collection/scoring preparation took{d['collection_stage_seconds']:.3f}s; the mean ten-turn portfolio loop took{d['mean_portfolio_loop_seconds']:.6f}s, including indexed-table accesses. These are local computation times, not new executions of the original software systems. Actual additional research cost is120charged recorded accesses. A deployed portfolio uses20total objective evaluations and zero model requests; historical prefix collection remains costed. No native/cloud-dollar savings are inferred.",'', 'This follow-up was specified after seeingV114model results and is explicitly exploratory. Its rule was frozen before any of its own continuation outcomes. It does not retroactively turn the original joint-control screen into a single-control comparison or replace the stronger original controls. The portfolio can sacrifice the quality of either constituent; that is reported in the last two columns. No favorable blending ratio or starting method was selected after this run.','', 'Independent replay reconstructed every portfolio choice from its own acquired labels, checked exact paired prefixes and budgets, and recomputed all36relative gains from saved actual model outcomes. Six exposed groups remain six groups. Positive or negative contrasts here cannot establish a learned router, population generalization, or journal acceptance.']
 (ROOT/'reports/portfolio_v115.md').write_text('\n'.join(text)+'\n');print(json.dumps({k:v for k,v in d.items() if k not in ['cases','portfolio_gains_vs_old_controls']}))
if __name__=='__main__':main()
