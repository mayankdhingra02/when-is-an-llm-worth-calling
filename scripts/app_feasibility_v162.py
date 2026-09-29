"""Forty charged prospective probes; no LLM request or outcome-based admission."""
import argparse,json,hashlib,itertools,random,subprocess,time,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v162';O=ROOT/'results/v162_apps'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def candidates():
 ds={'ripgrep':{'threads':[1,2,3,4,6,8,10,12],'mmap':[False,True],'buffering':['block','line'],'engine':['default','pcre2']},'hnswlib':{'M':[8,12,16,32],'ef_construction':[64,128],'ef_search':[16,32,64,128],'query_threads':[1,4]}}
 return {e:[dict(zip(d,vs)) for vs in itertools.product(*d.values())] for e,d in ds.items()}
def prepare():
 assert not (A/'freeze.json').exists();cs=candidates();write(A/'candidates.json',cs);jobs=[{'engine':e,'candidate_id':i,'repeat':r,'config':cs[e][i]} for e in cs for i in [0,21,42,63] for r in range(5)];random.Random(162).shuffle(jobs);write(A/'jobs.json',jobs)
 used=['reports/protocol_v162.md','scripts/app_worker_v162.py','scripts/app_feasibility_v162.py','scripts/hnsw_worker_v161.cpp','tests/synthetic/test_apps_v161.py','artifacts/study_v162/candidates.json','artifacts/study_v162/jobs.json','artifacts/study_v160/ann_train.f32','artifacts/study_v160/ann_query.f32','artifacts/study_v160/ann_kth_squared.npy','artifacts/study_v160/rg_reference.json','artifacts/study_v160/references.json','artifacts/study_v162/query_references.json','artifacts/study_v160/corpus_files.json','.native-v160/bin/hnsw_worker_v161','.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/rg']
 write(A/'freeze.json',{'at_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in used},'native_cap':40,'seconds_cap':600})
def guard():
 for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):
  assert sha(ROOT/'.native-v160/search_corpus'/f['path'])==f['sha256']
def collect():
 guard();O.mkdir(exist_ok=False);start=time.monotonic();charged=0;error=None
 try:
  for k,j in enumerate(read(A/'jobs.json'),1):
   if time.monotonic()-start>540:raise TimeoutError('600secondreserve')
   charged=k;write(O/'ledger.json',{'charged':k,'cap':40});row={'charge':k,'job':j,'status':'started','at_unix':time.time(),'result':None};write(O/f'{k:03d}.json',row);t=time.monotonic()
   try:
    cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/app_worker_v162.py'),'--engine',j['engine'],'--config',json.dumps(j['config'])];p=subprocess.run(cmd,capture_output=True,text=True,timeout=60);row.update(returncode=p.returncode,stderr=p.stderr)
    if p.returncode:row['status']='failed'
    else:row.update(status='completed',result=json.loads(p.stdout))
   except subprocess.TimeoutExpired:row['status']='external_timeout'
   row['collection_seconds']=time.monotonic()-t;write(O/f'{k:03d}.json',row);print(k,j['engine'],j['candidate_id'],row['status'],flush=True)
 except Exception as e:error=repr(e)
 finally:write(O/'completion.json',{'intended':40,'charged':charged,'unattempted':40-charged,'seconds':time.monotonic()-start,'error':error})
 if error:raise RuntimeError(error)
def summarize():
 rs=[read(O/f'{i:03d}.json') for i in range(1,41)];summary={}
 for e in candidates():
  cells=[]
  for i in [0,21,42,63]:
   rr=[r for r in rs if r['job']['engine']==e and r['job']['candidate_id']==i];good=[r['result'] for r in rr if r['result'] and r['result']['correct'] and r['result']['quality']>=.95];ts=[r['objective_seconds'] for r in good];med=statistics.median(ts) if ts else None;mad=statistics.median(abs(x-med) for x in ts)/med if ts else None
   cells.append({'candidate_id':i,'charged':len(rr),'valid_quality':len(good),'median_seconds':med,'relative_mad':mad,'min_quality':min((r['quality'] for r in good),default=None),'pass':len(good)==5 and med>=.01 and mad<=.05})
  summary[e]={'cells':cells,'admitted':all(c['pass'] for c in cells)}
 write(O/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','collect','summarize']);a=p.parse_args();globals()[a.stage]()
