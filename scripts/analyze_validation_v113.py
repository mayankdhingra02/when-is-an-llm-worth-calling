"""Independently certify all fresh outcomes and compare frozen incumbents."""
import json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from scipy.io import mmread
from escalation.numerical_v94 import linear_certificate,lp_certificate
from collect_smollm_v47 import read,write,sha
from prepare_validation_v113 import expected_jobs,schedule,ARMS,SEEDS

def analyze(root=ROOT):
 for n,h in read(root/'reports/protocol_v113.freeze.json')['sha256'].items():assert sha(root/n)==h,n
 cfg=read(root/'configs/validation_v113.json');assert cfg['jobs']==expected_jobs() and cfg['schedule']==schedule(cfg['jobs'])
 out=root/'results/v113_validation';summary=read(out/'summary.json');records=summary['records'];starts=[json.loads(s) for s in (out/'starts.jsonl').read_text().splitlines()];completed=[json.loads(s) for s in (out/'completed.jsonl').read_text().splitlines()]
 assert records==completed and len(starts)==len(records)==summary['acquisitions']<=90 and summary['unattempted']==90-len(records)
 assert read(out/'ledger.json')['records']==records
 matrix=mmread(root/'data/native_v94/orsreg_1.mtx').tocsc();truth=1+(np.arange(matrix.shape[0])%17)/17;rhs=matrix@truth
 import highspy
 h=highspy.Highs();h.setOptionValue('output_flag',False);assert h.readModel(str(root/'artifacts/sources/v94/25fv47.mps'))==highspy.HighsStatus.kOk;lp=h.getLp()
 checked=physical_starts=physical_returns=0;labels={j['key']:[] for j in cfg['jobs']};peak=0;failures=[]
 for job,r,start in zip(cfg['schedule'],records,starts):
  key=job['request_key'];assert r['key']==key and r['row']==job['row'] and (r['family'],r['seed'],r['arm'],r['repeat'])==(job['family'],job['seed'],job['arm'],job['repeat'])
  assert all(r[k]==v for k,v in start.items()) and r['charged_acquisition'] and r['owned_process_group_absent']
  request=read(out/'requests'/f'{key}.json');assert all(request[k]==v for k,v in job.items())
  p=out/'evaluations'/f'{key}.json';events=p.with_suffix('.attempts.jsonl')
  ev=[json.loads(s) for s in events.read_text().splitlines()] if events.exists() else []
  physical_starts+=sum(e['status']=='started' for e in ev);physical_returns+=sum(e['status']=='returned' for e in ev)
  peak=max(peak,r['peak_sampled_rss_bytes'])
  if p.exists():
   result=read(p);assert result['request']==request
   with np.load(p.with_suffix('.npz')) as vec:
    certs=[]
    for i,m in enumerate(result['measurements']):
     cert=linear_certificate(matrix,rhs,vec[f'x{i}'],truth) if job['family']=='superlu' else lp_certificate(lp,vec[f'x{i}'],vec[f'y{i}'],vec[f'z{i}'])
     assert cert['valid']==m['certificate']['valid'];certs.append(cert['valid']);checked+=1
   label=statistics.median(m['seconds'] for m in result['measurements']) if all(certs) else 30
   assert result['objective_seconds']==label
   if r['status']=='valid':assert len(certs)==3 and all(certs) and result['valid'] and r['label']==label and r['returncode']==0
  else:assert r['status']!='valid'
  if r['status']!='valid':assert r['label']==30;failures.append(key)
  labels[job['key']].append(r['label'])
 assert physical_starts<=270 and physical_returns<=physical_starts
 cases=[]
 for family in ['superlu','highs']:
  for seed in SEEDS:
   vals={a:labels[f'{family}_{seed}_{a}'] for a in ARMS};complete=all(len(v)==3 for v in vals.values())
   if not complete:continue
   med={a:statistics.median(v) for a,v in vals.items()};job={a:next(j for j in cfg['jobs'] if (j['family'],j['seed'],j['arm'])==(family,seed,a)) for a in ARMS}
   gain={a:(med[a]-med['llm'])/med[a] for a in ARMS if a!='llm'}
   historical={a:(job[a]['historical_label']-job['llm']['historical_label'])/job[a]['historical_label'] for a in gain}
   cases.append(dict(family=family,seed=seed,medians=med,validation_labels=vals,relative_gains=gain,historical_gains=historical,incumbent_rows={a:j['row'] for a,j in job.items()},same_configuration_as_llm={a:job[a]['row']==job['llm']['row'] for a in gain},relative_ranges={a:(max(v)-min(v))/statistics.mean(v) for a,v in vals.items()},failed_acquisitions=sum(k.startswith(f'{family}_{seed}_') for k in failures)))
 groups={}
 for family in ['superlu','highs']:
  rs=[r for r in cases if r['family']==family]
  groups[family]={a:dict(mean_gain=statistics.mean(r['relative_gains'][a] for r in rs) if rs else None,historical_mean_gain=statistics.mean(r['historical_gains'][a] for r in rs) if rs else None,positive=sum(r['relative_gains'][a]>0 for r in rs),harmful_at_5pct=sum(r['relative_gains'][a]<=-.05 for r in rs)) for a in ['batch_3nn','full_sequential_3nn']}
 thresholds=[dict(margin=t,cases_at_least_margin_both=sum(all(g>=t for g in r['relative_gains'].values()) for r in cases),cases_strictly_above_margin_both=sum(all(g>t for g in r['relative_gains'].values()) for r in cases)) for t in [0,.02,.05,.1]]
 return dict(scope='post-selection validation; same host and exposed engines; not fresh search or independent systems',status=summary['status'],cases=cases,groups=groups,threshold_grid=thresholds,audit=dict(acquisitions=len(records),intended=90,unattempted=90-len(records),failures=len(failures),failure_keys=failures,physical_starts=physical_starts,physical_returns=physical_returns,certificates_recomputed=checked,peak_sampled_rss_bytes=peak,stage_seconds=summary['stage_seconds'],new_model_requests=0,new_download_bytes=0,external_spend_usd=0,historical_model_requests=100,historical_native_acquisitions=500,total_native_collection_including_validation=500+len(records),per_arm_historical_search_budget=20,per_incumbent_validation_budget=3))

def main():
 result=analyze();out=ROOT/'results/v113_analysis';out.mkdir(exist_ok=True);write(out/'summary.json',result);print(json.dumps(dict(groups=result['groups'],thresholds=result['threshold_grid'],audit=result['audit'])))
if __name__=='__main__':main()
