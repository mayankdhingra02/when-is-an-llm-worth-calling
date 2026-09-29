"""Independent ledger/choice/model/validation replay; no new measurements."""
import copy,datetime,hashlib,json,math,random,statistics
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v153';O=ROOT/'results/v153_native'
CONTROLS=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal'];MODELS=['smollm3_3b','qwen3_8b']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-8,abs_tol=1e-10),(a,b)
def dist(a,b):return (abs(a[0]-b[0])+abs(a[1]-b[1]))/2

def nextrow(c,ids,labels,order,mode,anchor=None):
 available=[i for i in order if i not in ids]
 if len(ids)<4 or mode=='random_full':return available[0]
 if mode in ['fixed_neighbor','adaptive_neighbor']:
  best=anchor if mode=='fixed_neighbor' else ids[min(range(len(ids)),key=lambda k:labels[k][0])]
  return min(available,key=lambda i:dist(c['x'][i],c['x'][best]))
 assert mode=='sequential_3nn'
 estimates=[]
 for i in available:
  near=sorted(range(len(ids)),key=lambda k:(dist(c['x'][i],c['x'][ids[k]]),k))[:3];estimates.append(sum(labels[k][0] for k in near)/3)
 return available[min(range(len(available)),key=lambda k:estimates[k])]

def project(c,p,proposals):
 ids=[];diagnostics=[];previous=[];seen=set(p['ids'])
 for x in proposals:
  assert len(x)==2 and all(type(v)==int and 0<=v<8 for v in x)
  actual=[c['domains'][i][v] for i,v in enumerate(x)];point=[(actual[0]-1)/7,(actual[1]-1)/49]
  i=min((i for i in p['order'] if i not in seen),key=lambda i:dist(c['x'][i],point));seen.add(i);ids.append(i)
  diagnostics.append({'row_id':i,'distance':dist(c['x'][i],point),'repeated_proposal':x in previous,'matches_prefix':any(dist(c['x'][k],point)==0 for k in p['ids'])});previous.append(x)
 return ids,diagnostics

def verify_records(events):
 assert len(events)==400
 for i,e in enumerate(events):
  assert e['index']==i and e['charged'] and e['status']=='correct' and e['server_reaped'] and e['server_exit'] in [0,-15,-9] and e['client_exit']==0
  m=json.loads(e['client_stdout']);assert m==e['measurement'];assert m['checked_operations']==2048000 and m['failed_clients']==0 and m['batches_per_client']==16000;assert 0<m['seconds']<=10 and 0<e['lifecycle_seconds']<=15;close(e['value'],m['seconds'])
  for k,v in {'cmd_get':1024000,'get_hits':1024000,'get_misses':0,'cmd_set':1025024,'curr_items':1024,'evictions':0}.items():assert int(e['stats'][k])==v
  assert e['stats']['version']=='1.6.45'
  argv=e['server_command'];assert argv[argv.index('-l')+1]=='127.0.0.1' and argv[argv.index('-U')+1]=='0' and argv[argv.index('-m')+1]=='64'
  assert [int(argv[argv.index('-t')+1]),int(argv[argv.index('-R')+1])]==e['settings']

def verify_choices(events,c,jobs):
 for e in events:assert e['settings']==c['raw_features'][e['row_id']]
 responses={};starts={}
 for m in MODELS:
  folder=ROOT/'results/v153_models'/m;responses[m]={r['key']:r for r in map(json.loads,(folder/'responses.jsonl').read_text().splitlines())};starts[m]=[json.loads(s) for s in (folder/'generation_starts.jsonl').read_text().splitlines()];ledger=read(folder/'ledger.json')
  assert len(starts[m])==ledger['generation_requests']==ledger['scientific_requests']==5;assert ledger['allocated_output_tokens']==5120 and ledger['retries']==ledger['external_spend_usd']==0 and ledger['stage_seconds']<=300 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['server_exit_code']==0
  assert len({s['identity'] for s in starts[m]})==5
  for s in starts[m]:
   payload=s['payload'];assert payload['n_predict']==1024
   response=responses[m][s['identity']]['response'];assert response['tokens_predicted']<=1024;assert response['tokens_evaluated']>0
   preflight=read(folder/'preflight'/f"{s['identity']}.json");assert payload['prompt']==preflight['rendered']['prompt']
   job=next(j for j in jobs if j['key']==s['identity']);assert preflight['messages']==read(ROOT/job['messages_path'])
 for job in jobs:
  key=job['key'];p=read(ROOT/job['prefix']);assert sha(ROOT/job['prefix'])==job['prefix_sha256'];order=list(range(64));random.Random(job['seed']).shuffle(order);assert p['order']==order
  es=[e for e in events if e['identity']==key and e['phase']=='prefix'];assert len(es)==10;ids=[];labels=[]
  for e in es:
   assert e['row_id']==nextrow(c,ids,labels,order,'sequential_3nn');ids.append(e['row_id']);labels.append([e['value']])
  assert ids==p['ids'] and labels==p['labels'];body=json.loads(read(ROOT/job['messages_path'])[1]['content']);assert body['observed_examples']==[{'settings':c['raw_features'][i],'seconds':v[0]} for i,v in zip(ids,labels)]
  for arm in CONTROLS+MODELS:
   s=read(O/'search'/f'{key}__{arm}.json');state=s['state'];assert state['ids'][:10]==p['ids'] and state['labels'][:10]==p['labels'];assert len(state['ids'])==len(set(state['ids']))==len(state['labels'])==17
   events_search=[e for e in events if e['identity']==key+'__'+arm and e['phase'] in ['classical_search','model_search']];assert len(events_search)==7
   ids=copy.deepcopy(p['ids']);labels=copy.deepcopy(p['labels']);projected=None
   if arm=='random_proposal':
    rng=random.Random(153200+job['seed']);props=[[rng.randrange(8),rng.randrange(8)] for _ in range(10)];assert props==s['proposals'];projected,diag=project(c,p,props);assert diag==s['projection']
   elif arm in MODELS:
    response=responses[arm].get(key);score=read(ROOT/'results/v153_models'/arm/'scores'/f'{key}.json')
    if score['status']=='valid':
     raw=json.loads(response['response']['content']);assert len(raw)==10 and all(isinstance(x,str) and len(x)==2 and all(ch in '01234567' for ch in x) for x in raw);props=[[int(v) for v in x] for x in raw];assert props==score['score'];projected,diag=project(c,p,props);assert diag==s['projection'] and s['fallback'] is False
    else:assert s['fallback'] is True
   anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])]
   for k,e in enumerate(events_search):
    expected=projected[k] if projected is not None else nextrow(c,ids,labels,order,arm if arm in CONTROLS else 'sequential_3nn',anchor);assert e['row_id']==expected;ids.append(expected);labels.append([e['value']])
   assert ids==state['ids'] and labels==state['labels']
 return starts,responses

def verify_decisions(jobs):
 from verify_router_v151 import score_model,calibration,quant
 from router_v132 import features
 from router_v151 import trajectory,KINDS
 data=read(ROOT/'artifacts/study_v151/inputs.json')['rows']
 for r in data:
  if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
 folds=read(ROOT/'results/v151_router/folds.json')['ecosystem'];trained=read(A/'routers.json');ds=read(A/'decisions.json')['rows']
 for m in MODELS:
  rs=[r for r in data if r['model']==m];t=trained[m];cals={};held=[]
  for j in jobs:
   p=read(ROOT/j['prefix']);f=features(p,read(A/'candidates.json')['domains'],'minimize')+trajectory(p,'minimize');d=next(d for d in ds if d['key']==j['key'] and d['model']==m);np.testing.assert_allclose(d['features'],f,atol=1e-12);held.append({'key':j['key'],'features':f})
  predictions={}
  for kind,v in t['variants'].items():
   scores={k:s for f in folds[m] for k,s in f['variants'][kind]['scores'].items()};ss=[scores[r['key']] for r in rs];cals[kind]=calibration(ss,rs,v['calibration']);close(v['q80'],quant(ss,rs,.8));predictions[kind]=score_model(v['model'],rs,held)
  selected=min(KINDS,key=lambda k:(-cals[k]['gain'],cals[k]['rate'],KINDS.index(k)));assert t['selected_kind']==selected;cal=cals[selected];us=[r['features'][6] for r in rs];uc=calibration(us,rs,t['uncertainty']);close(t['uncertainty_q80'],quant(us,rs,.8));rng=random.Random(153001);sub=[]
  for j,h,score in zip(jobs,held,predictions[selected]):
   d=next(d for d in ds if d['key']==j['key'] and d['model']==m);close(score,d['score']);score=d['score'];th=cal['threshold'];u=uc['threshold'];pol={'never':False,'always':True,'benefit':th is not None and score>=th,'benefit_q80':score>=t['variants'][selected]['q80'],'uncertainty':u is not None and h['features'][6]>=u,'uncertainty_q80':h['features'][6]>=t['uncertainty_q80'],'random_development_rate':rng.random()<cal['rate']};sub.append((d,pol))
  ix=set(random.Random(153002).sample(range(5),sum(p['benefit'] for d,p in sub)))
  for i,(d,p) in enumerate(sub):p['random_matched_rate']=i in ix;assert p==d['policies']

def verify_validation(events,summary):
 choices=read(O/'selections.json');seal=read(O/'selection_seal.json');assert sha(O/'selections.json')==seal['sha256'];assert len(choices)==35
 for x in choices:
  path=O/'search'/f"{x['case']}__{x['arm']}.json";assert sha(path)==x['search_sha256'];s=read(path)['state'];k=min(range(17),key=lambda k:s['labels'][k][0]);assert x['row_id']==s['ids'][k] and x['search_best']==s['labels'][k][0]
 plan=[]
 for block in range(3):
  order=list(range(35));random.Random(153900+block).shuffle(order);plan.extend({'block':block,**choices[i]} for i in order)
 assert plan==read(O/'validation_plan.json');validation=[json.loads(s) for s in (O/'validation.jsonl').read_text().splitlines()];es=[e for e in events if e['phase']=='validation'];assert len(es)==len(validation)==105
 for p,v,e in zip(plan,validation,es):
  assert e['identity']==p['case']+'__'+p['arm'] and e['row_id']==p['row_id'] and e['at_unix']>seal['at_unix'];assert v=={**p,'value':e['value']}
 for r in summary['cases']:
  vals=[e['value'] for e in es if e['identity']==r['key']+'__'+r['model']];assert len(vals)==3;assert r['arm']['validation_times']==vals;med=statistics.median(vals);close(med,r['arm']['validation_median'])
  for c in CONTROLS:
   cv=[e['value'] for e in es if e['identity']==r['key']+'__'+c];ref=statistics.median(cv);assert r['references'][c]['validation_times']==cv;close(r['gains'][c],(ref-med)/ref)
 for m in MODELS:
  rs=[r for r in summary['cases'] if r['model']==m];assert len(rs)==5
  for name,p in summary['models'][m]['policies'].items():
   chosen=[r for r in rs if r['policies'][name]];assert p['calls']==len(chosen);close(p['mean_gain'],sum(r['gains']['sequential_3nn'] for r in chosen)/5)
  for c in CONTROLS:close(summary['models'][m]['contrasts'][c]['mean_gain'],statistics.mean(r['gains'][c] for r in rs))

def main():
 for f in [ROOT/'reports/protocol_v153.freeze.json',A/'inputs.freeze.json']:
  for n,h in read(f)['sha256'].items():assert sha(ROOT/n)==h,n
 events=[read(p) for p in sorted((O/'acquisitions').glob('*.json'))];c=read(A/'candidates.json');jobs=read(A/'jobs.json');summary=read(O/'comparison.json');verify_records(events);starts,responses=verify_choices(events,c,jobs);verify_decisions(jobs);verify_validation(events,summary)
 assert read(O/'ledger.json')['acquisitions']==summary['completion']['acquisitions']==400 and summary['completion']['seconds']<=1800
 assert sum(e['phase']=='prefix' for e in events)==50;assert sum(e['phase']=='classical_search' for e in events)==175;assert sum(e['phase']=='model_search' for e in events)==70
 decisiontime=read(A/'decisions.json')['at_unix'];assert all(e['at_unix']>decisiontime for e in events if e['phase']!='prefix');assert all(s['at_unix']>max(e['at_unix'] for e in events if e['phase']=='classical_search') for ss in starts.values() for s in ss)
 stopped=datetime.datetime.fromisoformat(read(ROOT/'results/v153_models/summary.json')['at']).timestamp();assert min(e['at_unix'] for e in events if e['phase']=='model_search')>stopped
 mutations=[]
 for name in ['counter','median_gain','late_selection']:
  ee=copy.deepcopy(events);ss=copy.deepcopy(summary)
  if name=='counter':ee[0]['stats']['cmd_get']='0'
  elif name=='median_gain':ss['cases'][0]['gains']['sequential_3nn']+=.1
  else:next(e for e in ee if e['phase']=='validation')['at_unix']=0
  try:verify_records(ee);verify_validation(ee,ss)
  except AssertionError:mutations.append({'name':name,'rejected':True})
  else:raise AssertionError('Mutation accepted')
 result={'verified':True,'native_acquisitions':400,'native_server_exit_counts':{str(v):sum(e['server_exit']==v for e in events) for v in sorted({e['server_exit'] for e in events})},'logical_B20_arms':35,'charged_validation':105,'model_starts':sum(len(v) for v in starts.values()),'complete_responses':sum(len(v) for v in responses.values()),'mutations':mutations,'scope':'counter/stdout correctness receipts; independent search/projection/budget replay; independent router algebra/calibration; frozen selection and randomized charged validation; no new native or model calls'}
 (A/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
