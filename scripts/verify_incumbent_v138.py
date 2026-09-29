"""Independent stdlib replay: does not import the collector or optimizer."""
import argparse,csv,hashlib,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODES=['fixed_prefix_neighbor','adaptive_incumbent_neighbor']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root=ROOT,compact=False):
 art=root/'artifacts/study_v138';out=root/'results/v138_incumbent';jobs=read(art/'jobs.json');summary=read(out/'summary.json');cfg=read(root/'configs/study_v138.json')
 assert len(jobs)==30 and len({j['system_group'] for j in jobs})==6
 assert jobs==sorted(jobs,key=lambda j:(j['system_group'],j['seed']))
 for g in {j['system_group'] for j in jobs}:assert sorted(j['seed'] for j in jobs if j['system_group']==g)==[11,23,37,53,71]
 assert summary['complete'] and summary['error'] is None and summary['new_acquisitions']==600 and summary['new_model_requests']==0 and summary['intended_arms']==60
 assert summary['seconds']<=cfg['max_seconds']==180 and cfg['max_new_acquisitions']==600 and cfg['new_model_requests']==0
 acqs=[json.loads(x) for x in (out/'acquisitions.jsonl').read_text().splitlines()];assert len(acqs)==600
 cursor=0;cache={};rows=[];completed=[];last_time=0
 for j in jobs:
  c=read(art/'candidates'/f"{j['system_group']}.json");xs=c['x'];spec=c['spec'];prefix=read(root/j['prefix'])['state'];assert sha(root/j['prefix'])==j['prefix_sha256']
  assert len(prefix['ids'])==len(prefix['labels'])==10 and len(set(prefix['ids']))==10
  assert set(prefix['order'])==set(range(len(xs))) and len(prefix['order'])==len(xs)
  if spec['path'] not in cache:
   if compact:
    ex=read(art/'source_extracts'/f"{j['system_group']}.json");assert ex['source_sha256']==spec['sha256'];cache[spec['path']]={int(k):v for k,v in ex['lines'].items()}
   else:
    assert sha(root/spec['path'])==spec['sha256'];cache[spec['path']]={i+1:v for i,v in enumerate((root/spec['path']).read_text().splitlines())}
  lines=cache[spec['path']];header=next(csv.reader([lines[1]],delimiter=spec['delimiter']))
  def verify_row(i,y):
   row=dict(zip(header,next(csv.reader([lines[c['source_ids'][i]]],delimiter=spec['delimiter']))))
   assert [float(row[k]) for k in c['names']]==xs[i] and float(row[spec['primary_objective']])==y[0] and math.isfinite(y[0]) and y[0]>0
   return row[spec['primary_objective']]
  for i,y in zip(prefix['ids'],prefix['labels']):verify_row(i,y)
  best=lambda s:(min if spec['direction']=='-' else max)(y[0] for y in s['labels'])
  r={'key':j['key'],'system_group':j['system_group'],'seed':j['seed'],'direction':spec['direction'],'prefix':best(prefix)}
  for mode in MODES:
   key=f"{j['key']}_{mode}";s={'ids':prefix['ids'][:],'labels':[y[:] for y in prefix['labels']],'order':prefix['order'][:]}
   for step in range(10):
    sel=read(out/'selections'/f'{key}_{step}.json');assert sel['key']==key and sel['step']==step
    assert all(sel['before'][k]==s[k] for k in s) and len(s['ids'])==10+step
    ref=prefix if mode==MODES[0] else s
    k=min(range(len(ref['ids'])),key=lambda k:ref['labels'][k][0] if spec['direction']=='-' else -ref['labels'][k][0]);anchor=ref['ids'][k]
    scores=[(sum(a!=b for a,b in zip(xs[i],xs[anchor])),rank,i) for rank,i in enumerate(s['order']) if i not in s['ids']]
    distance,_,i=min(scores);assert sel['selected']=={'row_id':i,'anchor_id':anchor,'hamming_distance':distance}
    a=acqs[cursor];cursor+=1;assert a['key']==key and a['row_id']==i and a['source_line']==c['source_ids'][i] and last_time<=sel['at_unix']<=a['at_unix'];last_time=a['at_unix']
    y=[float(a['raw_target'])];assert verify_row(i,y)==a['raw_target'];s['ids'].append(i);s['labels'].append(y)
   arm=read(out/'arms'/f'{key}.json');assert arm['key']==key and arm['case_key']==j['key'] and arm['mode']==mode and arm['new_acquisitions']==10
   assert len(set(s['ids']))==20 and all(arm['state'][k]==s[k] for k in s);completed.append(key);r[mode]=best(s)
  refs=[('historical_model',j['model_arm']),('historical_sequential',j['classical_arm'])]
  if j['system_group'] in ['llvm','sac']:refs.extend(('historical_'+m,f"results/v136_feedback/arms/{j['key']}_{m}.json") for m in ['feedback','masked'])
  for name,path in refs:
   s=read(root/path)['state'];assert len(s['ids'])==len(s['labels'])==len(set(s['ids']))==20 and s['ids'][:10]==prefix['ids'] and s['labels'][:10]==prefix['labels'] and s['order']==prefix['order']
   for i,y in zip(s['ids'],s['labels']):verify_row(i,y)
   r[name]=best(s)
  rows.append(r)
 assert completed==summary['completed_arms'] and cursor==600
 assert len(list((out/'selections').glob('*.json')))==600 and len(list((out/'arms').glob('*.json')))==60
 result=read(out/'comparison.json');assert result['rows']==rows
 def gain(ref,v,d):return (ref-v)/ref if d=='-' else (v-ref)/ref
 def contrast(v):return {'mean':statistics.mean(v),'wins':sum(x>1e-12 for x in v),'ties':sum(abs(x)<=1e-12 for x in v),'losses':sum(x< -1e-12 for x in v)}
 groups={}
 for g in sorted({r['system_group'] for r in rows}):
  rs=[r for r in rows if r['system_group']==g];group={};refs=['prefix','historical_sequential','historical_model']+(['historical_feedback','historical_masked'] if g in ['llvm','sac'] else [])
  for mode in MODES:
   for ref in refs:group[f'{mode}_vs_{ref}']=contrast([gain(r[ref],r[mode],r['direction']) for r in rs])
  group['adaptive_vs_fixed']=contrast([gain(r[MODES[0]],r[MODES[1]],r['direction']) for r in rs]);groups[g]=group
 assert result['groups']==groups and result['actual_collection_cost']['new_recorded_acquisitions']==600 and result['actual_collection_cost']['model_requests']==0 and result['actual_collection_cost']['seconds']==summary['seconds']
 assert {k:result['estimated_deployment'][k] for k in ['total_evaluations','prefix_evaluations','continuation_evaluations','model_requests']}==dict(total_evaluations=20,prefix_evaluations=10,continuation_evaluations=10,model_requests=0)
 return {'verified':True,'arms':60,'recorded_acquisitions':600,'new_model_requests':0,'cases':30,'exposed_groups':6,'source_verification':'acquired-row extracts' if compact else 'full source hashes and acquired rows','selection_before_acquisition':True,'same_prefix':True,'independent_selection_reconstruction':True,'comparison_recomputed':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--compact',action='store_true');a=p.parse_args();print(json.dumps(verify(a.root,a.compact),indent=2))
