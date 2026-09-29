"""B10+7search+3chargedvalidation native study; real local calls in separate stage."""
import copy,hashlib,json,math,random,socket,subprocess,time
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,append
from native_feasibility_v152 import prime,command,verify_stats,B
import router_v151 as router
from router_v132 import features
A=ROOT/'artifacts/study_v153';O=ROOT/'results/v153_native'
SEEDS=[11,23,37,53,71];DOMAINS=[list(range(1,9)),[1,2,4,8,12,20,32,50]]
CONTROLS=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal'];MODELS=router.MODELS

def candidate():
 xs=[[t,r] for t in DOMAINS[0] for r in DOMAINS[1]]
 return {'names':['worker_threads','max_requests_per_event'],'domains':DOMAINS,'grid_domains':[list(range(8)),list(range(8))],'raw_features':xs,'x':[[(t-1)/7,(r-1)/49] for t,r in xs]}
def distance(a,b):return sum(abs(x-y) for x,y in zip(a,b))/2

def choose(c,s,mode,anchor=None):
 if len(s['ids'])!=len(s['labels']) or len(set(s['ids']))!=len(s['ids']) or len(s['ids'])>=17:raise ValueError('Invalid search state or search budget')
 available=[i for i in s['order'] if i not in s['ids']]
 if len(s['ids'])<4 or mode=='random_full':return available[0]
 if mode in ['adaptive_neighbor','fixed_neighbor']:
  best=anchor if mode=='fixed_neighbor' else s['ids'][min(range(len(s['ids'])),key=lambda k:s['labels'][k][0])]
  return min(available,key=lambda i:distance(c['x'][i],c['x'][best]))
 if mode!='sequential_3nn':raise ValueError('Unknown mode')
 def est(i):
  near=sorted(range(len(s['ids'])),key=lambda k:(distance(c['x'][i],c['x'][s['ids'][k]]),k))[:3]
  return sum(s['labels'][k][0] for k in near)/3
 return min(available,key=est)

def project(c,s,proposals):
 if len(proposals)!=10:raise ValueError('Ten proposals required')
 seen=set(s['ids']);selected=[];diag=[];prior=[]
 for p in proposals:
  if len(p)!=2 or any(type(v)!=int or v not in d for v,d in zip(p,c['grid_domains'])):raise ValueError('Invalid prototype')
  raw=[DOMAINS[j][v] for j,v in enumerate(p)];x=[(raw[0]-1)/7,(raw[1]-1)/49];i=min((i for i in s['order'] if i not in seen),key=lambda i:distance(x,c['x'][i]));seen.add(i);selected.append(i);diag.append({'row_id':i,'distance':distance(x,c['x'][i]),'repeated_proposal':list(p) in prior,'matches_prefix':any(distance(x,c['x'][k])==0 for k in s['ids'])});prior.append(list(p))
 return selected,diag

def messages(c,s):
 return [{'role':'system','content':'Optimize Memcached configuration from ten acquired measurements. Propose ten diverse promising settings ordered best first, as a JSON array of ten two-digit strings. Each digit0..7 indexes the listed values for that feature. Only the first seven proposals will be evaluated; three remaining evaluations are reserved for fresh validation of the best observed configuration. Avoid duplicate proposals.'},{'role':'user','content':json.dumps({'feature_order':c['names'],'indexed_values':c['domains'],'observed_examples':[{'settings':c['raw_features'][i],'seconds':y[0]} for i,y in zip(s['ids'],s['labels'])],'direction':'minimize','objective':'Correct fixed-work elapsed seconds: four concurrent local clients perform 2,048,000 mixed GET/SET operations on a64MiBcache. All responses must remain correct. Numeric normalized distance projects prototypes to unseen configurations.'},separators=(',',':'))}]

def measure(row_id,identity,phase):
 c=candidate();cfg=read(ROOT/'configs/study_v153.json');ledger=read(O/'ledger.json')
 if type(row_id)!=int or not 0<=row_id<64:raise ValueError('Invalid row')
 if ledger['acquisitions']>=400:raise PermissionError('400native acquisitions exhausted')
 if time.time()-ledger['collection_started_unix']>=1785:raise TimeoutError('Global cap reserve')
 idx=ledger['acquisitions'];ledger['acquisitions']+=1;write(O/'ledger.json',ledger)
 r={'index':idx,'identity':identity,'phase':phase,'row_id':row_id,'settings':c['raw_features'][row_id],'charged':True,'at_unix':time.time(),'status':'started'};p=None;log=None;t0=time.monotonic()
 try:
  with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
  t,req=c['raw_features'][row_id];argv=[str(B/'memcached-1.6.45/memcached'),'-l','127.0.0.1','-p',str(port),'-U','0','-m','64','-t',str(t),'-R',str(req)]
  r['server_command']=argv;logs=O/'server_logs';logs.mkdir(exist_ok=True);log=(logs/f'{idx:03d}.log').open('wb');p=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT);r['pid']=p.pid;deadline=time.monotonic()+2
  while True:
   if p.poll() is not None:raise RuntimeError('Early server exit')
   try:
    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
   except OSError:
    if time.monotonic()>deadline:raise TimeoutError('Server startup')
    time.sleep(.02)
  prime(port)
  if time.monotonic()-t0>3:raise TimeoutError('Prefill/startup')
  res=subprocess.run([str(B/'memcached_client_v152'),str(port)],capture_output=True,text=True,timeout=min(10,13-(time.monotonic()-t0)));r.update(client_stdout=res.stdout,client_stderr=res.stderr,client_exit=res.returncode);res.check_returncode();m=json.loads(res.stdout)
  if m['checked_operations']!=2048000 or m['failed_clients'] or not 0<m['seconds']<=10:raise ValueError('Invalid workload result')
  r['measurement']=m;r['stats']=verify_stats(command(port,b'stats\r\n'));r.update(value=m['seconds'],status='correct')
 except Exception as e:r.update(status='failed',value=None,error=repr(e));raise
 finally:
  if p is not None:
   if p.poll() is None:
    p.terminate()
    try:p.wait(timeout=1)
    except subprocess.TimeoutExpired:p.kill();p.wait(timeout=1)
   r.update(server_exit=p.returncode,server_reaped=p.poll() is not None)
  if log:log.close()
  r['lifecycle_seconds']=time.monotonic()-t0;write(O/'acquisitions'/f'{idx:03d}.json',r)
 return [r['value']]

def train_routers():
 data=copy.deepcopy(read(ROOT/'artifacts/study_v151/inputs.json')['rows']);folds=read(ROOT/'results/v151_router/folds.json')['ecosystem'];out={}
 for r in data:
  if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
 for m in MODELS:
  rs=[r for r in data if r['model']==m];variants={}
  for kind in router.KINDS:
   scores={k:v for f in folds[m] for k,v in f['variants'][kind]['scores'].items()};ordered=[scores[r['key']] for r in rs];cal=router.select(ordered,rs)
   variants[kind]={'calibration':cal,'q80':router.quantile(ordered,rs,.8),'model':router.fit(rs,kind)}
  chosen=min(router.KINDS,key=lambda k:(-variants[k]['calibration']['selected']['gain'],variants[k]['calibration']['selected']['rate'],router.KINDS.index(k)))
  us=[r['features'][6] for r in rs];out[m]={'selected_kind':chosen,'variants':variants,'uncertainty':router.select(us,rs),'uncertainty_q80':router.quantile(us,rs,.8),'training_groups':sorted({r['group'] for r in rs})}
 return out

def prepare():
 assert not (A/'routers.json').exists();write(A/'candidates.json',candidate());write(A/'routers.json',train_routers());write(A/'models.json',read(ROOT/'artifacts/study_v148/models.json'))

def check_freeze():
 for n,h in read(ROOT/'reports/protocol_v153.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def prefixes():
 check_freeze();O.mkdir(exist_ok=False);write(O/'ledger.json',{'collection_started_unix':time.time(),'acquisitions':0,'intended':400});c=candidate();jobs=[];ds=[];trained=read(A/'routers.json');rng={m:random.Random(153001) for m in MODELS}
 for seed in SEEDS:
  key=f'memcached_{seed}';order=list(range(64));random.Random(seed).shuffle(order);s={'ids':[],'labels':[],'order':order}
  for _ in range(10):
   i=choose(c,s,'sequential_3nn');v=measure(i,key,'prefix');s['ids'].append(i);s['labels'].append(v)
  p=A/'prefixes'/f'{key}.json';write(p,s);mp=A/'prompts'/f'{key}.json';write(mp,messages(c,s));f=features(s,DOMAINS,'minimize')+router.trajectory(s,'minimize')
  jobs.append({'key':key,'system_group':'memcached_native','seed':seed,'prefix':str(p.relative_to(ROOT)),'prefix_sha256':sha(p),'messages_path':str(mp.relative_to(ROOT)),'domains':c['grid_domains'],'sampling_seed':153000+seed})
  for m,t in trained.items():
   chosen=t['variants'][t['selected_kind']];cal=chosen['calibration']['selected'];score=router.predict(chosen['model'],{'features':f});th=cal['threshold'];u=t['uncertainty']['selected']['threshold']
   ds.append({'key':key,'model':m,'features':f,'score':score,'selected_kind':t['selected_kind'],'policies':{'never':False,'always':True,'benefit':th is not None and score>=th,'benefit_q80':score>=chosen['q80'],'uncertainty':u is not None and f[6]>=u,'uncertainty_q80':f[6]>=t['uncertainty_q80'],'random_development_rate':rng[m].random()<cal['rate']}})
 for m in MODELS:
  sub=[d for d in ds if d['model']==m];ix=set(random.Random(153002).sample(range(5),sum(d['policies']['benefit'] for d in sub)))
  for i,d in enumerate(sub):d['policies']['random_matched_rate']=i in ix
 write(A/'jobs.json',jobs);write(A/'decisions.json',{'at_unix':time.time(),'rows':ds});ps=list((A/'prefixes').glob('*.json'))+list((A/'prompts').glob('*.json'))+[A/'jobs.json',A/'decisions.json']
 write(A/'inputs.freeze.json',{'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in ps}});print('50nativeprefixlabels;decisionsfrozen',flush=True)

def classical():
 check_freeze();c=candidate();tasks=[(j,mode) for j in read(A/'jobs.json') for mode in CONTROLS];random.Random(153700).shuffle(tasks)
 for j,mode in tasks:
  p=read(ROOT/j['prefix']);s=copy.deepcopy(p);anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])];diag=[];proposals=None
  if mode=='random_proposal':
   rng=random.Random(153200+j['seed']);proposals=[[rng.randrange(8),rng.randrange(8)] for _ in range(10)];ids,diag=project(c,p,proposals)
  for k in range(7):
   i=ids[k] if mode=='random_proposal' else choose(c,s,mode,anchor);v=measure(i,j['key']+'__'+mode,'classical_search');s['ids'].append(i);s['labels'].append(v)
  write(O/'search'/f"{j['key']}__{mode}.json",{'case':j['key'],'arm':mode,'state':s,'proposals':proposals,'projection':diag});print(j['key'],mode,'17searchlabels',flush=True)
 classical_gate()

def classical_gate():
 assert read(O/'ledger.json')['acquisitions']==225
 for j in read(A/'jobs.json'):
  p=read(ROOT/j['prefix'])
  for mode in CONTROLS:
   s=read(O/'search'/f"{j['key']}__{mode}.json")['state'];assert len(s['ids'])==len(set(s['ids']))==len(s['labels'])==17;assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels']
 return True

def model_search():
 check_freeze();classical_gate();c=candidate();tasks=[(j,m) for j in read(A/'jobs.json') for m in MODELS];random.Random(153701).shuffle(tasks)
 for j,m in tasks:
  p=read(ROOT/j['prefix']);s=copy.deepcopy(p);sp=ROOT/'results/v153_models'/m/'scores'/f"{j['key']}.json";score=read(sp) if sp.exists() else {'status':'unattempted'};valid=score['status']=='valid';ids,diag=project(c,p,score['score']) if valid else ([],[])
  for k in range(7):
   i=ids[k] if valid else choose(c,s,'sequential_3nn');v=measure(i,j['key']+'__'+m,'model_search');s['ids'].append(i);s['labels'].append(v)
  write(O/'search'/f"{j['key']}__{m}.json",{'case':j['key'],'arm':m,'state':s,'status':score['status'],'fallback':not valid,'projection':diag});print(j['key'],m,'17searchlabels',flush=True)

def validate():
 assert read(O/'ledger.json')['acquisitions']==295;selections=[]
 for j in read(A/'jobs.json'):
  for arm in CONTROLS+MODELS:
   p=O/'search'/f"{j['key']}__{arm}.json";s=read(p)['state'];best=min(range(17),key=lambda k:s['labels'][k][0]);selections.append({'case':j['key'],'arm':arm,'row_id':s['ids'][best],'search_best':s['labels'][best][0],'search_sha256':sha(p)})
 write(O/'selections.json',selections);write(O/'selection_seal.json',{'at_unix':time.time(),'sha256':sha(O/'selections.json')})
 plan=[]
 for block in range(3):
  order=list(range(35));random.Random(153900+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
 write(O/'validation_plan.json',plan)
 for x in plan:
  v=measure(x['row_id'],x['case']+'__'+x['arm'],'validation');append(O/'validation.jsonl',{**x,'value':v[0]})
 assert read(O/'ledger.json')['acquisitions']==400
 write(O/'completion.json',{'at_unix':time.time(),'acquisitions':400,'logical_B20_arms':35,'unique_search_evaluations_per_arm':17,'charged_validation_per_arm':3,'seconds':time.time()-read(O/'ledger.json')['collection_started_unix']});print('400nativeacquisitions;35validatedB20armscomplete',flush=True)
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','prefixes','classical','model_search','validate']);args=ap.parse_args();globals()[args.stage]()
