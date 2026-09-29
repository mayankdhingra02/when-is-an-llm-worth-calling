"""Independent raw-log, objective, branch, EI and response provenance replay."""
import copy,hashlib,json,math,random,statistics,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from report_apps_v168 import summaries
from proposal_v128 import parse
A=ROOT/'artifacts/study_v168';O=ROOT/'results/v168_native';M=ROOT/'results/v168_models';CONTROLS=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal'];MODELS=['smollm3_3b','qwen3_8b']
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objective(r,c):
 v=r['measurement'];assert v['engine']==r['engine'] and v['config']==c['configs'][r['row_id']] and r['returncode']==0
 raw=json.loads(r['raw_stdout']);assert all(v[k]==val for k,val in raw.items())
 assert 0<v['seconds']<60 and v['seconds']==v['objective_seconds']
 if r['engine']=='polars':
  assert v['answers']==read(ROOT/'data/flights_v88/query_contract.json')['expected']['answers'] and v['thread_pool_size']==v['config']['threads'];quality=1.;assert v['native_invocations']==3
 else:
  pred=v['predictions'];assert len(pred)==8192 and all(type(x)==int and 0<=x<7 for x in pred)
  truth=np.load(ROOT/'artifacts/study_v166/covertype.npz')['valid_y'];quality=sum(int(a==b) for a,b in zip(pred,truth))/8192;assert quality==v['accuracy'] and v['native_invocations']==1
  learner=v['booster_config']['learner'];tree=learner['gradient_booster'];cfg=v['config']
  assert int(learner['generic_param']['nthread'])==cfg['threads'] and learner['generic_param']['device']=='cpu'
  assert int(tree['tree_train_param']['max_bin'])==cfg['max_bin'] and int(tree['tree_train_param']['max_depth'])==cfg['max_depth'] and int(tree['gbtree_model_param']['num_trees'])==cfg['rounds']*7
 assert v['quality']==quality and v['correct'] is True
 value=v['seconds'] if quality>=.75 else 60.
 assert value==v['value']==r['value'] and r['status']==('correct' if quality>=.75 else 'quality_penalty')

def distance(c,a,b):return sum(abs(x-y) for x,y in zip(c['x'][a],c['x'][b]))/len(c['x'][a])
def reference_choice(c,ids,ys,order,mode):
 free=[i for i in order if i not in ids]
 if len(ids)<4 or mode=='random_full':return free[0]
 if mode=='adaptive_neighbor':
  anchor=ids[min(range(len(ys)),key=lambda k:ys[k])];return min(free,key=lambda i:distance(c,i,anchor))
 if mode=='sequential_3nn':
  def pred(i):
   near=sorted(range(len(ids)),key=lambda k:(distance(c,i,ids[k]),k))[:3];return sum(ys[k] for k in near)/3
  return min(free,key=pred)
 raise ValueError(mode)

def ei_reference(c,ids,ys,order):
 # Direct linear solves, not the collector's Cholesky implementation.
 raw=c['raw_features'];cats=[any(isinstance(r[j],str) for r in raw) for j in range(len(raw[0]))];cols=[]
 for j,cat in enumerate(cats):
  col=[r[j] for r in raw]
  if cat:levels=sorted(set(col),key=str);cols.append([levels.index(x) for x in col])
  else:lo=min(col);hi=max(col);cols.append([(float(x)-lo)/(hi-lo) for x in col])
 x=np.array(cols).T;numeric=[j for j,cat in enumerate(cats) if not cat];categorical=[j for j,cat in enumerate(cats) if cat]
 def cov(i,j):
  k=1.
  if numeric:
   radius=math.sqrt(sum((x[i,d]-x[j,d])**2 for d in numeric)/len(numeric));t=math.sqrt(5)*radius;k*=(1+t+t*t/3)*math.exp(-t)
  if categorical:k*=math.exp(-sum(x[i,d]!=x[j,d] for d in categorical)/len(categorical))
  return k
 y=np.asarray(ys);y=(y-y.mean())/(y.std() if y.std()>1e-12 else 1.);K=np.array([[cov(i,j) for j in ids] for i in ids])+np.eye(len(ids))*1e-6;coef=np.linalg.solve(K,y);free=[i for i in order if i not in ids];ei={}
 for i in free:
  k=np.array([cov(j,i) for j in ids]);mu=float(k@coef);sd=math.sqrt(max(0,1-float(k@np.linalg.solve(K,k))));d=min(y)-mu;z=d/sd if sd>1e-12 else 0;ei[i]=float(d*.5*math.erfc(-z/math.sqrt(2))+sd*math.exp(-z*z/2)/math.sqrt(2*math.pi)) if sd>1e-12 else max(d,0.)
 return ei

def project_reference(c,p,proposals):
 seen=set(p['ids']);out=[]
 for row in proposals:
  x=[v/(len(d)-1) for v,d in zip(row,c['domains'])];free=[i for i in p['order'] if i not in seen];i=min(free,key=lambda i:sum(abs(a-b) for a,b in zip(x,c['x'][i]))/len(x));seen.add(i);out.append(i)
 return out

def main():
 for name in ['freeze.json','inputs.freeze.json']:
  for n,h in read(A/name)['sha256'].items():assert digest(ROOT/n)==h,n
 assert digest(ROOT/'.local-runtime/llama-b11146/llama-server')==read(A/'freeze.json')['sha256']['.local-runtime/llama-b11146/llama-server']
 acq=[read(O/'acquisitions'/f'{i:03d}.json') for i in range(1,801)];assert [r['charge'] for r in acq]==list(range(1,801));assert read(O/'ledger.json')['acquisitions']==800 and sum(r['measurement']['native_invocations'] for r in acq)==1600
 cs={e:read(A/'candidates'/f'{e}.json') for e in ['polars','xgboost']};jobs=read(A/'jobs.json');assert len(jobs)==10 and {j['system_group'] for j in jobs}==set(cs)
 for r in acq:objective(r,cs[r['engine']])
 assert read(A/'inputs.freeze.json')['at_unix']<min(r['at_unix'] for r in acq if r['phase']=='search')
 checked_gp=0;gaps=[]
 for j in jobs:
  key=j['key'];c=cs[j['engine']];p=read(ROOT/j['prefix']);assert digest(ROOT/j['prefix'])==j['prefix_sha256'];rr=[r for r in acq if r['case']==key and r['phase']=='prefix'];assert len(rr)==10;ids=[];ys=[];order=list(range(len(c['configs'])));random.Random(j['seed']).shuffle(order);assert p['order']==order
  for r in rr:
   assert reference_choice(c,ids,ys,order,'sequential_3nn')==r['row_id'];ids.append(r['row_id']);ys.append(r['value'])
  assert p['ids']==ids and p['labels']==[[y] for y in ys]
  body=json.loads(read(ROOT/j['messages_path'])[1]['content']);assert body['observed_examples']==[{'settings':c['raw_features'][i],'loss_seconds':y} for i,y in zip(ids,ys)]
  for arm in CONTROLS+MODELS:
   rec=read(O/'search'/f'{key}__{arm}.json');state=rec['state'];rr=[r for r in acq if r['case']==key and r['arm']==arm and r['phase']=='search'];assert len(rr)==7;ids=list(p['ids']);ys=[v[0] for v in p['labels']];proposals=rec['proposals'];projected=project_reference(c,p,proposals) if proposals is not None else None
   if arm=='random_proposal':
    rng=random.Random(168200+j['seed']);assert proposals==[[rng.randrange(len(d)) for d in c['domains']] for _ in range(10)]
   for k,r in enumerate(rr):
    i=r['row_id'];assert i not in ids
    if projected is not None:assert i==projected[k]
    elif arm=='gp_ei':
     ei=ei_reference(c,ids,ys,order);gap=max(ei.values())-ei[i];assert gap<1e-8;gaps.append(gap);checked_gp+=1
    else:assert i==reference_choice(c,ids,ys,order,'sequential_3nn' if arm in MODELS else arm)
    ids.append(i);ys.append(r['value'])
   assert len(set(ids))==17 and state=={'ids':ids,'labels':[[y] for y in ys],'order':order}
 selections=read(O/'selections.json');assert len(selections)==70 and digest(O/'selections.json')==read(O/'selection_seal.json')['sha256'];vs=lines(O/'validation.jsonl');assert len(vs)==210 and read(O/'selection_seal.json')['at_unix']<min(r['at_unix'] for r in acq if r['phase']=='validation')
 for sel in selections:
  rec=O/'search'/f"{sel['case']}__{sel['arm']}.json";s=read(rec)['state'];assert digest(rec)==sel['search_sha256'];best=min(range(17),key=lambda k:s['labels'][k][0]);assert sel['row_id']==s['ids'][best] and sel['search_best']==s['labels'][best][0]
 plan=[]
 for block in range(3):
  order=list(range(70));random.Random(168900+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
 assert read(O/'validation_plan.json')==plan
 for v,expected,r in zip(vs,plan,[r for r in acq if r['phase']=='validation']):
  assert {k:v[k] for k in expected}==expected;assert (v['case'],v['arm'],v['row_id'],v['value'])==(r['case'],r['arm'],r['row_id'],r['value'])
 starts_total=0
 for model in MODELS:
  ledger=read(M/model/'ledger.json');starts=lines(M/model/'generation_starts.jsonl');responses=lines(M/model/'responses.jsonl');assert ledger['generation_requests']==len(starts)<=10 and ledger['retries']==0 and ledger['server_exit_code']==0 and ledger['allocated_output_tokens']<=10240 and ledger['peak_server_rss_bytes']<=8*1024**3;starts_total+=len(starts)
  for start in starts:assert start['at_unix']>max(r['at_unix'] for r in acq if r['phase']=='search' and r['arm'] in CONTROLS)
  for n,h in read(M/model/'preflight_seal.json')['sha256'].items():assert digest(ROOT/n)==h
  for r in responses:
   j=next(j for j in jobs if j['key']==r['key']);score=read(M/model/'scores'/f"{j['key']}.json");pre=read(M/model/'preflight'/f"{j['key']}.json");req=next(s for s in starts if s['identity']==j['key']);assert pre['messages']==read(ROOT/j['messages_path']) and req['payload']['prompt']==pre['rendered']['prompt'] and req['payload']['seed']==j['sampling_seed']
   if score['status']=='valid':assert [list(x) for x in parse(r['response'],j['domains'])]==score['score'];assert read(O/'search'/f"{j['key']}__{model}.json")['proposals']==score['score']
 arms,cases=summaries(selections,vs,acq);comp=read(O/'comparison.json');assert comp['cases']==cases and comp['arms']==list(arms.values())
 # Outcome aggregation, call counts and matched rate independent of report code.
 decisions=read(A/'decisions.json')['rows'];assert len(decisions)==20
 trained=read(A/'routers.json');assert trained==read(ROOT/'artifacts/study_v153/routers.json')
 from router_v132 import features
 from router_v151 import trajectory,predict
 from controllers_v154 import signals
 for d in decisions:
  j=next(j for j in jobs if j['key']==d['case']);state=read(ROOT/j['prefix']);c=cs[j['engine']];f=features(state,c['domains'],'minimize')+trajectory(state,'minimize');assert np.allclose(f,d['features'],rtol=0,atol=1e-12)
  t=trained[d['model']];v=t['variants'][t['selected_kind']];assert not set(v['model']['training_groups'])&set(cs);pred=predict(v['model'],{'features':f});assert pred==d['score'];th=v['calibration']['selected']['threshold'];uth=t['uncertainty']['selected']['threshold'];assert d['policies']['benefit']==(th is not None and pred>=th) and d['policies']['uncertainty']==(uth is not None and f[6]>=uth)
  sig=signals({'raw_features':c['raw_features'],'ids':state['ids'],'labels':[y[0] for y in state['labels']],'direction':'minimize','seed':j['seed'],'key':j['key']},1.);assert sig==d['signals'];assert d['policies']['bora_adaptation']==(sig['bora_action']!='a1') and d['policies']['rank_draw_adaptation']==sig['rank_draw_call']
 for p in comp['policies']:
  rows=[d for d in decisions if d['model']==p['model']];g=[];calls=[]
  for d in rows:
   case=next(c for c in cases if c['model']==p['model'] and c['case']==d['case']);delta=case['gains']['sequential_3nn'];rate=d['rank_expected_call'] if p['policy']=='rank_expected_adaptation' else (float(delta>0) if p['policy']=='hindsight_oracle' else float(d['policies'][p['policy']]));g.append(rate*delta);calls.append(rate)
  assert abs(sum(calls)-p['calls_or_expected_calls'])<1e-12 and abs(sum(g)/len(g)-p['equal_group_mean_gain'])<1e-12
 for model in MODELS:
  ds=[d for d in decisions if d['model']==model];assert sum(d['policies']['benefit'] for d in ds)==sum(d['policies']['random_matched_rate'] for d in ds)
 # Three semantic corruption checks on measured records, in memory only.
 rejected=[]
 for kind in ['objective','output','identity']:
  r=copy.deepcopy(next(r for r in acq if r['status']=='correct'));c=cs[r['engine']]
  if kind=='objective':r['value']*=2
  elif kind=='output':r['measurement']['quality']=0.0
  else:r['measurement']['engine']='unrecognized'
  try:objective(r,c)
  except AssertionError:rejected.append(kind)
  else:raise AssertionError('Mutation accepted '+kind)
 receipt={'verified':True,'native_acquisitions':800,'prefixes':10,'B20_arms':70,'fresh_validation':210,'GP_choices_independently_checked':checked_gp,'max_EI_gap':max(gaps),'model_starts':starts_total,'native_invocations':sum(r['measurement']['native_invocations'] for r in acq),'mutations_rejected':rejected,'policy_prefix_recomputation':20,'policy_feature_replay_uses_existing_tested_helpers':True,'limitation':'Internal replay, not independently collected host replication. Policy decisions use frozen previously tested implementations.'}
 (A/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
