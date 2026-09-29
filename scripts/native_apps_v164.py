"""Prospective paired native study: ten shared labels + seven search + three validation."""
import argparse,copy,itertools,json,random,subprocess,time,datetime,hashlib
from pathlib import Path
from collect_smollm_v47 import read,write,sha,append
from native_study_v153 import choose as neighbor_choose
from router_v132 import features
import router_v151 as router
from controllers_v154 import signals
from gp_continuations_v155 import choose as gp_choose

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v164';O=ROOT/'results/v164_native';SEEDS=[11,23,37,53,71]
CONTROLS=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal'];MODELS=['smollm3_3b_numeric','smollm3_3b_catalog','qwen3_8b_numeric','qwen3_8b_catalog'];ENGINES=['ripgrep','hnswlib']

def candidates(engine):
 cs=read(ROOT/'artifacts/study_v162/candidates.json')[engine];names=list(cs[0]);ds=[list(dict.fromkeys(c[n] for c in cs)) for n in names]
 ix=[[d.index(c[n]) for n,d in zip(names,ds)] for c in cs]
 return {'names':names,'domains':ds,'grid_domains':[list(range(len(d))) for d in ds],'raw_features':[[c[n] for n in names] for c in cs],'indices':ix,'x':[[v/(len(d)-1) for v,d in zip(row,ds)] for row in ix],'configs':cs}

def choose(c,s,mode):
 if mode=='gp_ei':return gp_choose(c['raw_features'],s['ids'],[v[0] for v in s['labels']],s['order'],'minimize',1.)[0]
 return neighbor_choose(c,s,mode)

def project(c,s,proposals):
 if len(proposals)!=10:raise ValueError('Ten proposals required')
 seen=set(s['ids']);ids=[];diag=[];prior=[]
 for p in proposals:
  if len(p)!=len(c['domains']) or any(type(v)!=int or v not in d for v,d in zip(p,c['grid_domains'])):raise ValueError('Bad prototype')
  x=[v/(len(d)-1) for v,d in zip(p,c['domains'])]
  def dist(i):return sum(abs(a-b) for a,b in zip(x,c['x'][i]))/len(x)
  i=min((i for i in s['order'] if i not in seen),key=dist);seen.add(i);ids.append(i);diag.append({'row_id':i,'distance':dist(i),'duplicate_proposal':list(p) in prior,'matches_prefix':any(dist(k)==0 for k in s['ids'])});prior.append(list(p))
 return ids,diag

def messages(engine,c,s):
 width=len(c['names'])
 task={'ripgrep':'Complete five fixed keyword-count queries over a fixed 3407-file CPython source tree. All file counts must be exact. Minimize total elapsed time for all five queries, including native process launch and count emission. Every setting does the same work.','hnswlib':'Build an approximate nearest-neighbor index over 3823 real 64-dimensional Optdigits vectors, then query 1797 vectors for ten neighbors each, squared L2 distance. Fixed seed100 and single-thread index construction. Minimize build plus query elapsed time, subject to mean tie-aware recall at least95%. Quality-infeasible results receive a fixed20second utility penalty; this is not a measured successful runtime.'}[engine]
 return [{'role':'system','content':f'Optimize {engine} configuration from ten acquired outcomes. Return a JSON array of ten {width}-digit strings ordered most promising first. Each digit indexes the listed values for its feature. Avoid duplicate proposals and propose diverse promising settings. Only the first seven projected unseen settings will be measured; three remaining evaluations are reserved for fresh validation of the best observed setting.'},{'role':'user','content':json.dumps({'feature_order':c['names'],'indexed_values':c['domains'],'observed_examples':[{'settings':c['raw_features'][i],'loss_seconds':v[0]} for i,v in zip(s['ids'],s['labels'])],'objective':task,'direction':'minimize','projection':'Normalized ordinal-coordinate L1 nearest unseen setting; seeded order breaks ties.'},separators=(',',':'))}]

def guard():
 for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def measure(j,i,arm,phase):
 c=read(A/'candidates'/f"{j['engine']}.json");ledger=read(O/'ledger.json');cfg=read(ROOT/'configs/study_v164.json')
 if type(i)!=int or not 0<=i<64:raise ValueError('Bad candidate')
 if ledger['acquisitions']>=900:raise PermissionError('900cap')
 if time.time()-ledger['start_unix']>=cfg['total_collection_seconds_cap']-60:raise TimeoutError('Stage cap reserve')
 k=ledger['acquisitions']+1;ledger['acquisitions']=k;write(O/'ledger.json',ledger)
 r={'charge':k,'case':j['key'],'engine':j['engine'],'arm':arm,'phase':phase,'row_id':i,'at_unix':time.time(),'status':'started','value':None};write(O/'acquisitions'/f'{k:03d}.json',r);t=time.monotonic()
 cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/app_worker_v162.py'),'--engine',j['engine'],'--config',json.dumps(c['configs'][i])]
 try:
  p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=60);r.update(command=cmd,returncode=p.returncode,stderr=p.stderr)
  if p.returncode:raise RuntimeError('Worker failed')
  v=json.loads(p.stdout);r['measurement']=v
  if v['engine']!=j['engine'] or v['config']!=c['configs'][i]:raise ValueError('Wrong measurement identity')
  if v['correct'] and v['quality']>=.95 and v['value']==v['objective_seconds']:r.update(status='correct',value=v['value'])
  elif j['engine']=='hnswlib' and v['correct'] and v['quality']<.95 and v['value']==20.:r.update(status='quality_penalty',value=20.)
  else:raise ValueError('Incorrect/unsupported application result')
 except Exception as e:r.update(status='failed',error=repr(e));raise
 finally:r['collection_seconds']=time.monotonic()-t;write(O/'acquisitions'/f'{k:03d}.json',r)
 return [r['value']]

def search(models=False):
 guard();jobs=read(A/'jobs.json');tasks=[(j,a) for j in jobs for a in (MODELS if models else CONTROLS)];random.Random(164701 if models else 164700).shuffle(tasks)
 for j,arm in tasks:
  c=read(A/'candidates'/f"{j['engine']}.json");p=read(ROOT/j['prefix']);s=copy.deepcopy(p);ids=[];diag=[];status='classical';proposals=None
  if models:
   model,condition=arm.rsplit('_',1);path=ROOT/'results/v164_models'/model/'scores'/f"{j['key']}__{condition}.json";score=read(path) if path.exists() else {'status':'unattempted'};status=score['status'];proposals=score['score'] if status=='valid' else None
  elif arm=='random_proposal':
   rng=random.Random(164200+j['seed']);proposals=[[rng.randrange(len(d)) for d in c['domains']] for _ in range(10)]
  if proposals is not None:
   if models and condition=='catalog':proposals=[c['indices'][i] for i in proposals]
   ids,diag=project(c,p,proposals)
  for k in range(7):
   i=ids[k] if proposals is not None else choose(c,s,'sequential_3nn' if models else arm);s['labels'].append(measure(j,i,arm,'search'));s['ids'].append(i)
  write(O/'search'/f"{j['key']}__{arm}.json",{'case':j['key'],'engine':j['engine'],'arm':arm,'state':s,'status':status,'fallback':models and status!='valid','proposals':proposals,'projection':diag});print(j['key'],arm,'17search',flush=True)
 if not models:classical_gate()

def classical_gate():
 assert read(O/'ledger.json')['acquisitions']==350
 for j in read(A/'jobs.json'):
  p=read(ROOT/j['prefix'])
  for a in CONTROLS:
   s=read(O/'search'/f"{j['key']}__{a}.json")['state'];assert len(s['ids'])==len(set(s['ids']))==len(s['labels'])==17;assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels']
 return True

def validate():
 guard();assert read(O/'ledger.json')['acquisitions']==630;selections=[];jobs={j['key']:j for j in read(A/'jobs.json')}
 for j in jobs.values():
  for arm in CONTROLS+MODELS:
   p=O/'search'/f"{j['key']}__{arm}.json";s=read(p)['state'];best=min(range(17),key=lambda k:s['labels'][k][0]);selections.append({'case':j['key'],'engine':j['engine'],'arm':arm,'row_id':s['ids'][best],'search_best':s['labels'][best][0],'search_sha256':sha(p)})
 write(O/'selections.json',selections);write(O/'selection_seal.json',{'at_unix':time.time(),'sha256':sha(O/'selections.json')});plan=[]
 for block in range(3):
  order=list(range(90));random.Random(164900+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
 write(O/'validation_plan.json',plan)
 for x in plan:append(O/'validation.jsonl',{**x,'value':measure(jobs[x['case']],x['row_id'],x['arm'],'validation')[0]})
 ledger=read(O/'ledger.json');assert ledger['acquisitions']==900;write(O/'completion.json',{'acquisitions':900,'reused_prefix_outcomes':100,'logical_B20_arms':90,'seconds':time.time()-ledger['start_unix'],'unique_search_per_arm':17,'fresh_validation_per_arm':3});print('900 new configuration outcomes/90 B20 arms complete',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['classical','model_search','validate']);q=p.parse_args();{'classical':lambda:search(False),'model_search':lambda:search(True),'validate':validate}[q.stage]()
