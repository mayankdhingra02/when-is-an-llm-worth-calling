"""Prospective paired native study: ten shared labels + seven search + three validation."""
import argparse,copy,itertools,json,random,subprocess,time,datetime,hashlib
from pathlib import Path
from collect_smollm_v47 import read,write,sha,append
from native_study_v153 import choose as neighbor_choose
from router_v132 import features
import router_v151 as router
from controllers_v154 import signals
from gp_continuations_v155 import choose as gp_choose
from solver_worker_v157 import valid_queens
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v159';O=ROOT/'results/v159_native';SEEDS=[11,23,37,53,71]
CONTROLS=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal'];MODELS=['smollm3_3b','qwen3_8b'];ENGINES=['cvc5','ortools']

def candidates(engine):
 cs=read(ROOT/'artifacts/study_v158/candidates.json')[engine];names=list(cs[0]);ds=[list(dict.fromkeys(c[n] for c in cs)) for n in names]
 ix=[[d.index(c[n]) for n,d in zip(names,ds)] for c in cs]
 return {'names':names,'domains':ds,'grid_domains':[list(range(len(d))) for d in ds],'raw_features':[[c[n] for n in names] for c in cs],'indices':ix,'x':[[v/(len(d)-1) for v,d in zip(row,ds)] for row in ix],'configs':cs,'n':10 if engine=='cvc5' else 48}

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
 return [{'role':'system','content':f'Optimize {engine} settings from ten acquired measurements. Return a JSON array of ten {width}-digit strings ordered most promising first. Each digit indexes the listed values for its feature. Propose diverse settings and avoid duplicates. Only the first seven projected unseen settings will be measured; the last three objective evaluations are reserved for fresh validation of the best observed configuration.'},{'role':'user','content':json.dumps({'feature_order':c['names'],'indexed_values':c['domains'],'observed_examples':[{'settings':c['raw_features'][i],'loss_seconds':v[0]} for i,v in zip(s['ids'],s['labels'])],'objective':f'Minimize native solve wall seconds for a fixed {c["n"]}-queens instance: one queen per column, distinct rows and both diagonals. Return any exact valid solution. All constraints and the instance remain unchanged. Single worker and fixed solver seed0. A no-solution timeout costs the fixed utility penalty20 seconds; that penalty is not a measured successful runtime.','direction':'minimize','projection':'Normalized feature-coordinate L1 nearest unseen setting, fixed seeded order breaks ties.'},separators=(',',':'))}]

def guard():
 for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def prepare():
 assert not (A/'freeze.json').exists();admission=read(ROOT/'results/v158_solvers/summary.json');assert all(admission[e]['admitted'] for e in ENGINES)
 for e in ENGINES:write(A/'candidates'/f'{e}.json',candidates(e))
 write(A/'models.json',read(ROOT/'artifacts/study_v153/models.json'));write(A/'routers.json',read(ROOT/'artifacts/study_v153/routers.json'))
 jobs=[{'key':e+'_'+str(seed),'engine':e,'system_group':e,'seed':seed,'prefix':f'artifacts/study_v159/prefixes/{e}_{seed}.json','messages_path':f'artifacts/study_v159/prompts/{e}_{seed}.json','sampling_seed':159000+seed,'domains':candidates(e)['grid_domains']} for e in ENGINES for seed in SEEDS]
 random.Random(159).shuffle(jobs);write(A/'plan.json',jobs)
 used=['reports/protocol_v159.md','configs/study_v159.json','scripts/native_solvers_v159.py','scripts/run_solvers_v159.py','scripts/collect_models_v159.py','scripts/runtime_models_v159.py','scripts/solver_worker_v157.py','scripts/native_study_v153.py','scripts/router_v132.py','scripts/router_v151.py','scripts/controllers_v154.py','scripts/gp_continuations_v155.py','scripts/proposal_v128.py','scripts/proposal_v127.py','scripts/audit_output_capacity_v127.py','scripts/process_rss_v129.py','src/escalation/receipts_v70.py','tests/synthetic/test_solvers_v159.py','artifacts/study_v159/plan.json','artifacts/study_v159/models.json','artifacts/study_v159/routers.json','artifacts/study_v159/candidates/cvc5.json','artifacts/study_v159/candidates/ortools.json','artifacts/study_v158/freeze.json','results/v158_solvers/summary.json','configs/solvers_v156.lock.txt']
 write(A/'freeze.json',{'at_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in used}})

def measure(j,i,arm,phase):
 c=read(A/'candidates'/f"{j['engine']}.json");ledger=read(O/'ledger.json');cfg=read(ROOT/'configs/study_v159.json')
 if type(i)!=int or not 0<=i<64:raise ValueError('Bad candidate')
 if ledger['acquisitions']>=800:raise PermissionError('800cap')
 if time.time()-ledger['start_unix']>=cfg['total_collection_seconds_cap']-20:raise TimeoutError('Stage cap reserve')
 k=ledger['acquisitions']+1;ledger['acquisitions']=k;write(O/'ledger.json',ledger)
 r={'charge':k,'case':j['key'],'engine':j['engine'],'arm':arm,'phase':phase,'row_id':i,'at_unix':time.time(),'status':'started','value':None};write(O/'acquisitions'/f'{k:03d}.json',r);t=time.monotonic()
 cmd=[str(ROOT/'.venv-solvers156/bin/python'),str(ROOT/'scripts/solver_worker_v157.py'),'--engine',j['engine'],'--config',json.dumps(c['configs'][i]),'--n',str(c['n']),'--limit','10']
 try:
  p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=15);r.update(command=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
  if p.returncode:raise RuntimeError('Worker failed')
  v=json.loads(p.stdout);r['measurement']=v
  if v['config']!=c['configs'][i] or v['n']!=c['n']:raise ValueError('Wrong solve identity')
  ok=valid_queens(v['rows'],c['n'])
  if ok and v['correct'] and v['status'] in ['sat','OPTIMAL','FEASIBLE']:r.update(status='correct',value=v['solve_seconds'])
  elif not v['rows'] and not v['correct'] and v['status'] in ['unknown (TIMEOUT)','UNKNOWN']:r.update(status='timeout_penalty',value=20.)
  else:raise ValueError('Incorrect/unsupported solve result')
 except Exception as e:r.update(status='failed',error=repr(e));raise
 finally:r['collection_seconds']=time.monotonic()-t;write(O/'acquisitions'/f'{k:03d}.json',r)
 return [r['value']]

def prefixes():
 guard();O.mkdir(exist_ok=False);write(O/'ledger.json',{'acquisitions':0,'start_unix':time.time(),'intended':800});decisions=[];jobs=[];trained=read(A/'routers.json')
 for j in read(A/'plan.json'):
  c=read(A/'candidates'/f"{j['engine']}.json");order=list(range(64));random.Random(j['seed']).shuffle(order);s={'ids':[],'labels':[],'order':order}
  for _ in range(10):
   i=choose(c,s,'sequential_3nn');s['labels'].append(measure(j,i,'shared','prefix'));s['ids'].append(i)
  write(ROOT/j['prefix'],s);write(ROOT/j['messages_path'],messages(j['engine'],c,s));j={**j,'prefix_sha256':sha(ROOT/j['prefix'])};jobs.append(j)
  f=features(s,c['domains'],'minimize')+router.trajectory(s,'minimize');sig=signals({'raw_features':c['raw_features'],'ids':s['ids'],'labels':[v[0] for v in s['labels']],'direction':'minimize','seed':j['seed'],'key':j['key']},1.)
  for m in MODELS:
   t=trained[m];selected=t['variants'][t['selected_kind']];score=router.predict(selected['model'],{'features':f});cal=selected['calibration']['selected'];th=cal['threshold'];uth=t['uncertainty']['selected']['threshold'];u=int(hashlib.sha256(('159|'+j['key']+'|'+m).encode()).hexdigest()[:13],16)/16**13
   decisions.append({'case':j['key'],'engine':j['engine'],'model':m,'features':f,'score':score,'signals':sig,'selected_kind':t['selected_kind'],'policies':{'never':False,'always':True,'benefit':th is not None and score>=th,'uncertainty':uth is not None and f[6]>=uth,'random_development_rate':u<cal['rate'],'bora_adaptation':sig['bora_action']!='a1','rank_draw_adaptation':sig['rank_draw_call']},'rank_expected_call':sig['p_llm']})
  print(j['key'],'prefix10',flush=True)
 for m in MODELS:
  rs=[r for r in decisions if r['model']==m];sel=set(random.Random(159002).sample(range(10),sum(r['policies']['benefit'] for r in rs)))
  for k,r in enumerate(rs):r['policies']['random_matched_rate']=k in sel
 write(A/'jobs.json',jobs);write(A/'decisions.json',{'at_unix':time.time(),'rows':decisions});paths=list((A/'prefixes').glob('*.json'))+list((A/'prompts').glob('*.json'))+[A/'jobs.json',A/'decisions.json'];write(A/'inputs.freeze.json',{'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})

def search(models=False):
 guard();jobs=read(A/'jobs.json');tasks=[(j,a) for j in jobs for a in (MODELS if models else CONTROLS)];random.Random(159701 if models else 159700).shuffle(tasks)
 for j,arm in tasks:
  c=read(A/'candidates'/f"{j['engine']}.json");p=read(ROOT/j['prefix']);s=copy.deepcopy(p);ids=[];diag=[];status='classical';proposals=None
  if models:
   path=ROOT/'results/v159_models'/arm/'scores'/f"{j['key']}.json";score=read(path) if path.exists() else {'status':'unattempted'};status=score['status'];proposals=score['score'] if status=='valid' else None
  elif arm=='random_proposal':
   rng=random.Random(159200+j['seed']);proposals=[[rng.randrange(len(d)) for d in c['domains']] for _ in range(10)]
  if proposals is not None:ids,diag=project(c,p,proposals)
  for k in range(7):
   i=ids[k] if proposals is not None else choose(c,s,'sequential_3nn' if models else arm);s['labels'].append(measure(j,i,arm,'search'));s['ids'].append(i)
  write(O/'search'/f"{j['key']}__{arm}.json",{'case':j['key'],'engine':j['engine'],'arm':arm,'state':s,'status':status,'fallback':models and status!='valid','proposals':proposals,'projection':diag});print(j['key'],arm,'17search',flush=True)
 if not models:classical_gate()

def classical_gate():
 assert read(O/'ledger.json')['acquisitions']==450
 for j in read(A/'jobs.json'):
  p=read(ROOT/j['prefix'])
  for a in CONTROLS:
   s=read(O/'search'/f"{j['key']}__{a}.json")['state'];assert len(s['ids'])==len(set(s['ids']))==len(s['labels'])==17;assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels']
 return True

def validate():
 guard();assert read(O/'ledger.json')['acquisitions']==590;selections=[];jobs={j['key']:j for j in read(A/'jobs.json')}
 for j in jobs.values():
  for arm in CONTROLS+MODELS:
   p=O/'search'/f"{j['key']}__{arm}.json";s=read(p)['state'];best=min(range(17),key=lambda k:s['labels'][k][0]);selections.append({'case':j['key'],'engine':j['engine'],'arm':arm,'row_id':s['ids'][best],'search_best':s['labels'][best][0],'search_sha256':sha(p)})
 write(O/'selections.json',selections);write(O/'selection_seal.json',{'at_unix':time.time(),'sha256':sha(O/'selections.json')});plan=[]
 for block in range(3):
  order=list(range(70));random.Random(159900+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
 write(O/'validation_plan.json',plan)
 for x in plan:append(O/'validation.jsonl',{**x,'value':measure(jobs[x['case']],x['row_id'],x['arm'],'validation')[0]})
 ledger=read(O/'ledger.json');assert ledger['acquisitions']==800;write(O/'completion.json',{'acquisitions':800,'logical_B20_arms':70,'seconds':time.time()-ledger['start_unix'],'unique_search_per_arm':17,'fresh_validation_per_arm':3});print('800nativeevaluations/70B20arms complete',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','prefixes','classical','model_search','validate']);q=p.parse_args();{'prepare':prepare,'prefixes':prefixes,'classical':lambda:search(False),'model_search':lambda:search(True),'validate':validate}[q.stage]()
