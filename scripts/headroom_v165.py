"""Finite offline diagnostic: exhaustively select, freeze, then freshly validate."""
import argparse,hashlib,json,random,statistics,subprocess,time
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,sha
A=ROOT/'artifacts/study_v165';O=ROOT/'results/v165_headroom';ENGINES=['ripgrep','hnswlib']
def plan():
 jobs=[]
 for phase,seed in [('selection',165100),('validation',165200)]:
  for block in range(3):
   rows=[{'phase':phase,'block':block,'engine':e,'row_id':i} for e in ENGINES for i in range(64)];random.Random(seed+block).shuffle(rows);jobs+=rows
 return jobs

def summarize_cells(records):
 cells=[]
 for e in ENGINES:
  for i in range(64):
   rs=[r for r in records if r['job']['engine']==e and r['job']['row_id']==i];assert len(rs)==3;values=[r['value'] for r in rs];med=statistics.median(values)
   cells.append({'engine':e,'row_id':i,'median':med,'relative_mad':statistics.median(abs(x-med) for x in values)/med,'valid':all(r['status']=='correct' for r in rs),'values':values,'minimum_quality':min(r['measurement']['quality'] for r in rs)})
 return cells

def select_reference(cells):
 selected=[]
 for e in ENGINES:
  eligible=[x for x in cells if x['engine']==e and x['valid']]
  if not eligible:raise ValueError('No quality-feasible candidate for '+e)
  selected.append(min(eligible,key=lambda x:(x['median'],x['row_id'])))
 return selected

def prepare():
 assert not (A/'freeze.json').exists();old=ROOT/'artifacts/study_v164';assert sha(old/'evidence_manifest.json')=='002902e3e2701b72c0fb51e521e66be951b611b151cc07e78823402953e4115d'
 for e in ENGINES:write(A/'candidates'/f'{e}.json',read(old/'candidates'/f'{e}.json'))
 targets=[]
 for j in read(old/'jobs.json'):
  p=read(ROOT/j['prefix'])
  for checkpoint in [4,7,10]:
   k=min(range(checkpoint),key=lambda k:p['labels'][k][0]);targets.append({'case':j['key'],'engine':j['engine'],'seed':j['seed'],'kind':'prefix','checkpoint':checkpoint,'row_id':p['ids'][k],'source':j['prefix'],'source_sha256':sha(ROOT/j['prefix'])})
 for s in read(ROOT/'results/v164_native/selections.json'):targets.append({'case':s['case'],'engine':s['engine'],'kind':'prior_incumbent','arm':s['arm'],'row_id':s['row_id'],'source':'results/v164_native/selections.json','source_sha256':sha(ROOT/'results/v164_native/selections.json')})
 write(A/'targets.json',targets);write(A/'plan.json',plan());used=read(old/'freeze.json')['sha256'].copy()
 for n,h in used.items():assert sha(ROOT/n)==h,n
 paths=[A/'targets.json',A/'plan.json',ROOT/'results/v164_native/selections.json',ROOT/'reports/protocol_v165.md',ROOT/'configs/study_v165.json',ROOT/'scripts/headroom_v165.py',ROOT/'tests/synthetic/test_headroom_v165.py']+list((A/'candidates').glob('*.json'))
 for p in paths:used[str(p.relative_to(ROOT))]=sha(p)
 write(A/'freeze.json',{'at_unix':time.time(),'sha256':used});print('Frozen768outcomes/2304invocations/0modelrequests')

def collect():
 cfg=read(ROOT/'configs/study_v165.json');assert cfg['max_new_model_requests']==cfg['new_download_bytes_cap']==cfg['external_spend_usd_cap']==0
 for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):assert sha(ROOT/'.native-v160/search_corpus'/f['path'])==f['sha256']
 O.mkdir(exist_ok=False);start=time.monotonic();records=[];error=None;charged=0;invocations=0;cs={e:read(A/'candidates'/f'{e}.json') for e in ENGINES}
 try:
  for k,j in enumerate(read(A/'plan.json'),1):
   if k>cfg['total_new_objective_cap']:raise PermissionError('Acquisition cap')
   if time.monotonic()-start>=cfg['total_seconds_cap']-cfg['reserve_seconds']:raise TimeoutError('Time reserve')
   if k==385:
    selected=select_reference(summarize_cells(records));write(O/'selected_reference.json',selected);write(O/'reference.freeze.json',{'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [O/'selected_reference.json',*sorted((O/'acquisitions').glob('*.json'))]}});print('Selection fixed before validation',flush=True)
   charged=k;invocations+=5 if j['engine']=='ripgrep' else 1
   if invocations>cfg['total_native_invocation_cap']:raise PermissionError('Native invocation cap')
   write(O/'ledger.json',{'charged_outcomes':k,'planned_native_invocations_for_charged_attempts':invocations,'cap':768,'start_unix':time.time()-(time.monotonic()-start)});r={'charge':k,'job':j,'at_unix':time.time(),'status':'started','value':None};dest=O/'acquisitions'/f'{k:03d}.json';write(dest,r);t=time.monotonic()
   try:
    cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/app_worker_v162.py'),'--engine',j['engine'],'--config',json.dumps(cs[j['engine']]['configs'][j['row_id']])];r['command']=cmd;p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=cfg['worker_timeout_seconds']);r.update(returncode=p.returncode,stderr=p.stderr)
    if p.returncode:raise RuntimeError('Worker failure')
    v=json.loads(p.stdout);r['measurement']=v
    if v['engine']!=j['engine'] or v['config']!=cs[j['engine']]['configs'][j['row_id']] or not v['correct']:raise ValueError('Incorrect identity/output')
    if v['quality']>=.95 and v['value']==v['objective_seconds']:r.update(status='correct',value=v['value'])
    elif j['engine']=='hnswlib' and v['quality']<.95 and v['value']==20.:r.update(status='quality_penalty',value=20.)
    else:raise ValueError('Invalid utility')
   except Exception as e:r.update(status='failed',error=repr(e));raise
   finally:r['collection_seconds']=time.monotonic()-t;write(dest,r)
   records.append(r)
   if k%64==0:print(k,j['phase'],'charged outcomes',flush=True)
 except Exception as e:error=repr(e)
 finally:write(O/'completion.json',{'intended_outcomes':768,'charged_outcomes':charged,'unattempted':768-charged,'planned_native_invocations_for_charged_attempts':invocations,'observed_native_invocations_in_successful_records':sum(r['measurement']['native_invocations'] for r in records),'new_model_requests':0,'seconds':time.monotonic()-start,'error':error})
 if error:raise RuntimeError(error)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','collect']);args=p.parse_args();globals()[args.stage]()
