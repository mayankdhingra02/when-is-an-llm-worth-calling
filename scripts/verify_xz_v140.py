"""Independent stdlib replay; compact mode omits physical images/binary/source check."""
import argparse,hashlib,itertools,json,math,random
from pathlib import Path
from fractions import Fraction
SEEDS=[11,23,37,53,71];XS=list(itertools.product([0,1,3],[0,1],[0,2],[0,1],[16,64,128],[0,16,64]));DS=[[0,1,3],[0,1],[0,2],[0,1],[16,64,128],[0,16,64]]
MODES=['sequential_3nn','random_full','fixed_prefix_neighbor','adaptive_incumbent_neighbor','context_sweep','llm']
def mean(x):return sum(x)/len(x)
def sd(x):m=mean(x);return math.sqrt(mean([(v-m)**2 for v in x]))
def close(a,b):return abs(a-b)<=1e-9*max(1,abs(a),abs(b))
def ranked(s):
 def score(row):
  nearest=sorted(range(len(s['ids'])),key=lambda k:sum(a!=b for a,b in zip(XS[row],XS[s['ids'][k]])))[:3]
  return sum(Fraction(s['labels'][k][0]) for k in nearest)/3
 return sorted([r for r in s['order'] if r not in s['ids']],key=score)
def project(props,prefix):
 seen=set(prefix['ids']);out=[]
 for x in props:
  row=min([r for r in prefix['order'] if r not in seen],key=lambda r:sum(a!=b for a,b in zip(x,XS[r])));out.append(row);seen.add(row)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--compact',action='store_true');ap.add_argument('--comparison',type=Path);args=ap.parse_args();root=args.root
 def read(n):return json.loads((root/n).read_text())
 def lines(n):return [json.loads(l) for l in (root/n).read_text().splitlines()]
 def sha(n):return hashlib.sha256((root/n).read_bytes()).hexdigest()
 freeze=read('reports/protocol_v140.freeze.json');inputs=read('artifacts/study_v140/inputs.freeze.json')
 if not args.compact:
  for n,h in freeze['sha256'].items():assert sha(n)==h,n
 for n,h in inputs['sha256'].items():assert sha(n)==h,n
 command_root=Path(read('artifacts/study_v140/command_root.json')['path']);work=read('artifacts/study_v140/workloads.json')['workloads'];receipts={};starts={};phases={}
 for phase,cap in [('classical',300),('continuations',53)]:
  base=f'results/v140_native/{phase}';ledger=read(base+'/ledger.json');assert ledger['configuration_attempts']==ledger['completed_configurations']==ledger['cap']==cap
  assert ledger['encodes']==ledger['decodes']==3*cap and ledger['seconds']<=ledger['seconds_cap'];ss=lines(base+'/starts.jsonl');commands=lines(base+'/commands.jsonl');assert len(ss)==cap and len(commands)==cap*6
  assert all(c['returncode']==0 and c['seconds']<=10.1 for c in commands)
  for number,start in enumerate(ss,1):
   assert start['attempt']==number and start['at']>freeze['at'];key=start['key'];assert key not in receipts;row=start['row'];assert start['settings']==list(XS[row]);r=read(base+'/'+key+'/result.json');assert r['valid'] and r['row']==row and r['key']==key and r['settings']==list(XS[row])
   assert len(r['records'])==3 and r['target']==sum(z['encoded_bytes'] for z in r['records'])
   for w,z in zip(work,r['records']):
    assert z['name']==w['name'];v=z['validation'];assert v=={'decoded_bytes':w['bytes'],'decoded_sha256':w['sha256']}
    lc,lp,pb,algo,nice,depth=XS[row];mode,mf=[('fast','hc4'),('normal','bt4')][algo];c=z['encode']['command'];assert c==[str(command_root/'.local-runtime/xz-v140/xz'),'--format=xz','--threads=1','--check=crc64','--memlimit-compress=256MiB','--no-adjust',f'--lzma2=dict=8MiB,lc={lc},lp={lp},pb={pb},mode={mode},mf={mf},nice={nice},depth={depth}','--stdout','--',str(command_root/w['path'])];assert z['decode']['command']==[str(command_root/'.local-runtime/xz-v140/xz'),'--decompress','--stdout','--threads=1','--memlimit-decompress=256MiB','--',str(command_root/z['encoded_path'])]
    assert z['encode'] in commands and z['decode'] in commands
    if not args.compact:assert sha(z['encoded_path'])==z['encoded_sha256'] and (root/z['encoded_path']).stat().st_size==z['encoded_bytes']
   receipts[key]=r;starts[key]=start;phases[key]=phase
 assert len(receipts)==353
 model=read('artifacts/study_v132/model.json');decisions=read('artifacts/study_v140/decisions.json')['rows'];jobs=read('artifacts/study_v140/jobs.json');responses=lines('results/v140_proposals/responses.jsonl');generation=lines('results/v140_proposals/generation_starts.jsonl');ml=read('results/v140_proposals/ledger.json');assert len(jobs)==len(responses)==len(generation)==ml['generation_requests']==5 and ml['retries']==0 and ml['allocated_output_tokens']==5120 and ml['server_exit_code']==0
 assert ml['stage_seconds']<=600 and ml['peak_server_rss_bytes']<=8589934592 and ml['external_spend_usd']==0
 preflightseal=read('results/v140_proposals/preflight_seal.json')
 for n,h in preflightseal['sha256'].items():assert sha(n)==h,n
 observed_keys=set();computed=[]
 for seed in SEEDS:
  order=list(range(216));random.Random(seed).shuffle(order);s={'ids':[],'labels':[],'order':order}
  for k in range(10):
   row=XS.index((3,0,2,1,128,0)) if k==0 else XS.index((3,0,2,1,64,0)) if k==1 else next(r for r in order if r not in s['ids']) if k==2 else ranked(s)[0];key=f'{seed}_prefix_{k:02}';r=receipts[key];assert r['row']==row and phases[key]=='classical';sel=read(f'results/v140_native/selections/{key}.json');assert sel['before']==s and sel['row']==row and sel['at_unix']<=starts[key]['at_unix'];s['ids'].append(row);s['labels'].append([r['target']]);observed_keys.add(key)
  prefix=read(f'results/v140_native/prefixes/{seed}.json');assert s==prefix;job=next(j for j in jobs if j['seed']==seed);assert job['domains']==DS and job['system_group']=='xz' and sha(job['prefix_path'])==job['prefix_sha256']
  body=json.loads(read(job['messages_path'])[1]['content']);assert body['direction']=='minimize' and body['symbol_to_value']==DS and len(body['observed_examples'])==10
  spec=read('artifacts/study_v140/domain.json');assert set(body)=={'direction','symbol_to_value','observed_examples','feature_order','performance_meaning'} and body['feature_order']==spec['names'] and body['performance_meaning']==spec['meaning']
  for example,row,y in zip(body['observed_examples'],s['ids'],s['labels']):assert example=={'settings':''.join(str(d.index(v)) for d,v in zip(DS,XS[row])),'performance':f'{y[0]:.6f}'}
  raw=next(x for x in responses if x['key']==job['key'])['response'];assert raw['stop_type']=='eos' and raw['truncated'] is False and 0<raw['tokens_predicted']<=1024
  coded=json.loads(raw['content']);assert len(coded)==10 and raw['content']==json.dumps(coded,separators=(',',':'))
  props=[tuple(d[int(c)] for d,c in zip(DS,x)) for x in coded];assert all(len(x)==6 and all(c.isdigit() and int(c)<len(d) for c,d in zip(x,DS)) for x in coded)
  score=read(f'results/v140_proposals/scores/{job["key"]}.json');assert score['status']=='valid' and score['score']==[list(x) for x in props]
  gen=next(g for g in generation if g['identity']==job['key']);payload=gen['payload'];assert payload['seed']==140000+seed and payload['n_predict']==1024 and payload['temperature']==.7 and payload['top_p']==.95 and payload['cache_prompt'] is False
  pf=read(f'results/v140_proposals/preflight/{job["key"]}.json');assert pf['messages']==read(job['messages_path']) and payload['prompt']==pf['rendered']['prompt'] and len(pf['prompt_tokens'])+1024<=4096
  assert all(payload[k]==v for k,v in {'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'stream':False,'return_tokens':True}.items())
  assert pf['output_capacity']['constructive_token_upper_bound_including_eos']==92 and pf['output_capacity']['cap']==1024
  d=next(x for x in decisions if x['seed']==seed);y=[v[0] for v in prefix['labels']];best=[min(y[:i+1]) for i in range(10)];last=max(i for i in range(10) if i==0 or best[i]!=best[i-1]);rng=random.Random(132000);boots=[min(y[rng.randrange(10)] for _ in range(10)) for _ in range(64)];f=[math.log1p(216),6,15/6,sd(y)/mean(y),(best[0]-best[-1])/best[0],(9-last)/9,sd(boots)/mean(y)];assert len(d['features'])==7 and all(close(a,b) for a,b in zip(f,d['features']))
  mo=model['model'];prediction=mo['intercept']+sum((x-m)/s*c for x,m,s,c in zip(f,mo['mean'],mo['scale'],mo['coef']));assert close(prediction,d['predicted_gain']) and d['decision_seconds']>0
  bt=model['benefit_calibration']['selected']['threshold'];ut=model['uncertainty_calibration']['selected']['threshold'];assert d['decisions']=={'benefit':bt is not None and prediction>=bt,'uncertainty':ut is not None and f[-1]>=ut}
  # Each decision predates all this seed's classical/model continuations.
  assert all(d['at']<v['at'] for key,v in starts.items() if key.startswith(str(seed)+'_') and '_prefix_' not in key)
  from datetime import datetime
  assert datetime.fromisoformat(d['at']).timestamp()<min(g['at_unix'] for g in generation)
  targets={};rng=random.Random(131900+seed);randprops=[tuple(rng.choice(v) for v in DS) for _ in range(10)]
  for mode in MODES:
   a=read(f'results/v140_native/arms/{seed}_{mode}.json');state=json.loads(json.dumps(prefix));batch=None
   if mode=='batch_3nn':batch=ranked(prefix)[:10]
   elif mode=='random_full':batch=random.Random(131400+seed).sample([r for r in order if r not in prefix['ids']],10)
   elif mode in ['random_projection','llm']:batch=project(randprops if mode=='random_projection' else props,prefix)
   elif mode=='context_sweep':
    batch=[XS.index((lc,lp,pb,1,128,0)) for lc in [0,1,3] for lp in [0,1] for pb in [0,2] if XS.index((lc,lp,pb,1,128,0)) not in prefix['ids']];batch.extend(r for r in ranked(prefix) if r not in batch);batch=batch[:10]
   for k in range(10):
    row=ranked(state)[0] if batch is None else batch[k]
    if mode in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor']:
     ref=prefix if mode=='fixed_prefix_neighbor' else state;anchor=ref['ids'][min(range(len(ref['ids'])),key=lambda i:ref['labels'][i][0])];row=min((i for i in order if i not in state['ids']),key=lambda i:sum(a!=b for a,b in zip(XS[i],XS[anchor])))
    key=f'{seed}_{mode}_{k:02}';sel=read(f'results/v140_native/selections/{key}.json');assert sel['before']==state and sel['row']==row and sel['at_unix']<=starts[key]['at_unix'];r=receipts[key];assert r['row']==row and phases[key]==('continuations' if mode=='llm' else 'classical');state['ids'].append(row);state['labels'].append([r['target']]);observed_keys.add(key)
   assert state==a['state'] and len(set(state['ids']))==20 and a['best']==min(y[0] for y in state['labels']);inc=min(range(20),key=lambda k:state['labels'][k][0]);assert a['incumbent']==state['ids'][inc];targets[mode]=a['best']
   if mode=='llm':
    assert a['fallback'] is False and a['model_status']=='valid';seen=set(prefix['ids']);prior=[];diagnostics=[]
    for prop in props:
     row=min((i for i in order if i not in seen),key=lambda i:sum(a!=b for a,b in zip(prop,XS[i])));diagnostics.append({'proposal':list(prop),'row_id':row,'hamming_distance':sum(a!=b for a,b in zip(prop,XS[row])),'repeated_proposal':tuple(prop) in prior,'matches_initial_observation':any(tuple(prop)==XS[i] for i in prefix['ids'])});seen.add(row);prior.append(tuple(prop))
    assert a['diagnostics']==diagnostics
  computed.append({'seed':seed,'prefix_best':min(y[0] for y in prefix['labels']),'reference':prefix['labels'][0][0],'default_anchor':prefix['labels'][1][0],**targets})
 for k in range(3):
  key=f'reference_repeat_{k}';assert receipts[key]['row']==XS.index((3,0,2,1,128,0)) and receipts[key]['target']==computed[0]['reference'];observed_keys.add(key)
 assert set(receipts)==observed_keys
 comparison=json.loads(args.comparison.read_text()) if args.comparison else read('results/v140_native/comparison.json');assert comparison['groups']==1 and comparison['cases']==5
 for r,c in zip(comparison['rows'],computed):
  for name,value in c.items():assert r[name]==value,('comparison',r['seed'],name)
  assert r['gain_fraction']==str(Fraction(c['sequential_3nn']-c['llm'],c['sequential_3nn']))
 assert comparison['llm_improved_prefix']==sum(c['llm']<c['prefix_best'] for c in computed) and comparison['classical_improved_prefix']==sum(c['sequential_3nn']<c['prefix_best'] for c in computed)
 for mode,stat in comparison['summary'].items():
  gs=[Fraction(c[mode]-c['llm'],c[mode]) for c in computed];assert stat['mean_fraction']==str(sum(gs)/5) and stat['wins']==sum(g>0 for g in gs) and stat['ties']==sum(g==0 for g in gs) and stat['losses']==sum(g<0 for g in gs)
 rng=random.Random(140900);rate=model['benefit_calibration']['selected']['development_rate'];chosen=set(random.Random(140900).sample(range(5),sum(d['decisions']['benefit'] for d in decisions)))
 for i,r in enumerate(comparison['rows']):
  d=next(x for x in decisions if x['seed']==r['seed']);assert r['decisions']=={'never':False,'always':True,**d['decisions'],'random_development_rate':rng.random()<rate,'random_matched_realized_rate':i in chosen,'hindsight_oracle_diagnostic':r['llm']<r['sequential_3nn']}
 for p,v in comparison['policies'].items():
  rs=comparison['rows'];gs=[Fraction(r['gain_fraction']) if r['decisions'][p] else Fraction(0) for r in rs];assert v['gain']['mean_fraction']==str(sum(gs)/5) and v['modeled_calls']==sum(r['decisions'][p] for r in rs);assert v['missed_benefit_over_1pct']==sum(not r['decisions'][p] and Fraction(r['gain_fraction'])>Fraction(1,100) for r in rs);assert v['harmful_escalation_over_1pct']==sum(r['decisions'][p] and Fraction(r['gain_fraction'])<Fraction(-1,100) for r in rs)
 for field in ['tokens_predicted','tokens_evaluated']:assert comparison['usage'][field]=={'observed_sum':sum(r['response'][field] for r in responses),'missing_intended':0}
 assert comparison['native_ledgers']==[read(f'results/v140_native/{p}/ledger.json') for p in ['classical','continuations']] and comparison['model_ledger']==ml
 assert comparison['model_projection_diagnostics']==[d for seed in SEEDS for d in read(f'results/v140_native/arms/{seed}_llm.json')['diagnostics']]
 assert comparison['reference_repeat_bytes']==[receipts[f'reference_repeat_{i}']['target'] for i in range(3)]
 assert len(list((root/'results/v140_native/selections').glob('*.json')))==350
 print(json.dumps({'verified':True,'compact':args.compact,'native_trials':353,'encodes':1059,'decodes':1059,'logical_B20_arms':30,'real_model_requests':5,'pre_decision_features_and_frozen_policies_verified':True,'new_collection':0}))
if __name__=='__main__':main()
