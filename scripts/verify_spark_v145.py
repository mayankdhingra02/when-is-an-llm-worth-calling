"""Independent standard-library replay. No model execution/new target collection."""
import csv,hashlib,json,math,random,statistics,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT={4,9,16,19,25,26,27,28,29}
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):
 h=hashlib.sha256()
 with (ROOT/p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def jl(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def close(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
def dist(a,b):return sum(float(x!=y) if j in CAT else abs(x-y) for j,(x,y) in enumerate(zip(a,b)))/30

def choose(c,s,mode,anchor=None):
 av=[i for i in s['order'] if i not in s['ids']];valid=[k for k,y in enumerate(s['labels']) if y[0] is not None]
 if len(valid)<4 or mode=='random_full':return av[0]
 if mode in ['adaptive_neighbor','fixed_neighbor']:
  anchor=anchor if mode=='fixed_neighbor' else s['ids'][min(valid,key=lambda k:s['labels'][k][0])]
  return min(av,key=lambda i:dist(c['x'][i],c['x'][anchor]))
 def estimate(i):
  near=sorted(valid,key=lambda k:(dist(c['x'][i],c['x'][s['ids'][k]]),k))[:3]
  return sum(s['labels'][k][0] for k in near)/len(near)
 return min(av,key=estimate)

def project(c,s,props):
 ids=[];seen=set(s['ids']);diagnostics=[];prior=[]
 for p in props:
  assert len(p)==30 and all(v in d for v,d in zip(p,c['grid_domains']))
  x=[v if j in CAT else v/9 for j,v in enumerate(p)]
  i=min((i for i in s['order'] if i not in seen),key=lambda i:dist(x,c['x'][i]));ids.append(i);seen.add(i);diagnostics.append({'row_id':i,'distance':dist(x,c['x'][i]),'repeated_proposal':list(p) in prior,'matches_prefix':any(dist(x,c['x'][k])==0 for k in s['ids'])});prior.append(list(p))
 return ids,diagnostics

def verify():
 for name in ['reports/protocol_v144.freeze.json','reports/protocol_v145.freeze.json','artifacts/study_v144/inputs.freeze.json']:
  for p,h in read(name)['sha256'].items():assert sha(p)==h,p
 A='artifacts/study_v144/';O='results/v145_spark/';jobs=read(A+'jobs.json');assert len(jobs)==25 and len({j['key'] for j in jobs})==25;cs={j['app']:read(A+'candidates/'+j['app']+'.json') for j in jobs};assert sum(len(c['x']) for c in cs.values())==499
 for app,c in cs.items():
  assert sha(c['source_path'])==c['source_sha256']
  rows=list(csv.reader((ROOT/c['source_path']).open()));raw=[];lines=[]
  for line,row in enumerate(rows[1:],2):
   if (row[31],row[33])==(app,c['input_size']):raw.append([v.strip() if j in CAT else float(v) for j,v in enumerate(row[:30])]);lines.append(line)
  assert raw==c['raw_features'] and lines==c['source_lines']
  ds=[sorted({x[j] for x in raw}) for j in range(30)];assert ds==c['domains']
  assert [[ds[j].index(v) if j in CAT else (v-ds[j][0])/(ds[j][-1]-ds[j][0]) if len(ds[j])>1 else 0 for j,v in enumerate(x)] for x in raw]==c['x']
 events=jl(O+'acquisitions.jsonl');original=jl('results/v144_spark/acquisitions.jsonl');assert events[:len(original)]==original and len(original)==1036 and len(events)==2000
 bykey={};allmissing=[]
 for e in events:
  case=e['key'].removeprefix('smollm3_3b_').removeprefix('qwen3_8b_');app=case.split('_')[0];c=cs[app];i=e['row_id'];assert e['source_line']==c['source_lines'][i]
  raw=next(csv.reader([(ROOT/c['source_path']).read_text().splitlines()[e['source_line']-1]]))[30];assert raw==e['raw_target']
  if raw.strip():assert close(float(raw),e['value']) and e['value']>0
  else:assert e.get('value') is None and e.get('error');allmissing.append(e)
  bykey.setdefault(e['key'],[]).append(e)
 assert len(bykey)==200 #25prefix +125classical +50model arms
 decisions={r['key']:r for r in read(A+'decisions.json')['rows']};frozen=read('artifacts/study_v132/model.json');benefitcount=0
 for j in jobs:
  p=read(j['prefix']);c=cs[j['app']];assert sha(j['prefix'])==j['prefix_sha256'];order=list(range(len(c['x'])));random.Random(j['seed']).shuffle(order);assert order==p['order'];s={'ids':[],'labels':[],'order':order}
  for e in bykey[j['key']+'_prefix']:
   assert choose(c,s,'sequential_3nn')==e['row_id'];s['ids'].append(e['row_id']);s['labels'].append([e['value']])
  assert s==p and len(p['ids'])==10
  d=decisions[j['key']];y=[v[0] for v in p['labels']];best=[min(y[:i+1]) for i in range(10)];last=max(i for i in range(10) if i==0 or best[i]!=best[i-1]);rng=random.Random(132000);boots=[min(y[rng.randrange(10)] for _ in range(10)) for _ in range(64)];f=[math.log1p(len(order)),sum(len(x)>1 for x in c['domains']),statistics.mean(len(x) for x in c['domains']),statistics.pstdev(y)/statistics.mean(y),(best[0]-best[-1])/best[0],(9-last)/9,statistics.pstdev(boots)/statistics.mean(y)];assert all(close(a,b) for a,b in zip(f,d['features']))
  m=frozen['model'];score=sum((x-a)/b*z for x,a,b,z in zip(f,m['mean'],m['scale'],m['coef']))+m['intercept'];assert close(score,d['score'])
  for k,score2 in [('benefit',score),('uncertainty',f[-1])]:
   th=frozen[k+'_calibration']['selected']['threshold'];assert d[k]==(th is not None and score2>=th)
  benefitcount+=d['benefit'];msg=read(j['messages_path']);body=json.loads(msg[1]['content']);assert body['observed_examples']==[{'settings':[round(v,5) for v in c['x'][i]],'performance':yy[0]} for i,yy in zip(p['ids'],p['labels'])]
  for mode in ['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal']:
   key=j['key']+'_'+mode;arm=read(O+'classical/'+key+'.json');s=json.loads(json.dumps(p));anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])]
   if mode=='random_proposal':
    rng=random.Random(144200+j['seed']);ids,diags=project(c,p,[[rng.choice(d) for d in c['grid_domains']] for _ in range(10)]);assert diags==arm['projection']
   for step,e in enumerate(bykey[key]):
    assert (ids[step] if mode=='random_proposal' else choose(c,s,mode,anchor))==e['row_id'];s['ids'].append(e['row_id']);s['labels'].append([e.get('value')])
   assert len(bykey[key])==10 and s==arm['state'] and len(set(s['ids']))==20 and arm['target']==min(y[0] for y in s['labels'] if y[0] is not None)
 assert sum(d['random_matched_rate'] for d in decisions.values())==benefitcount
 # Input jobs are shuffled, original matched-rate decisions retain fixed app/seed order.
 selected=set(random.Random(144001).sample(range(25),benefitcount));ordered=read(A+'decisions.json')['rows'];assert all(d['random_matched_rate']==(i in selected) for i,d in enumerate(ordered))
 assert read(A+'decisions.json')['at_unix']<min(e['at_unix'] for e in events if not e['key'].endswith('_prefix'))
 starts=[];responses={};cost={}
 for stage,model in [('v144','smollm3_3b'),('v145','smollm3_3b'),('v145','qwen3_8b')]:
  base=f'results/{stage}_models/{model}/';st=jl(base+'generation_starts.jsonl');rr=jl(base+'responses.jsonl');ledger=read(base+'ledger.json');assert ledger['generation_requests']==len(st) and ledger['allocated_output_tokens']==1024*len(st) and ledger['retries']==0 and ledger['server_exit_code']==0 and ledger['peak_server_rss_bytes']<=8589934592
  assert ledger['stage_seconds']<=(763 if stage=='v145' and model=='smollm3_3b' else 800);starts.extend((model,s['identity']) for s in st)
  for r in rr:responses[(model,r['key'])]=r
  for rec in st:
   j=next(j for j in jobs if j['key']==rec['identity']);p=rec['payload'];pre=read(base+'preflight/'+j['key']+'.json');assert p['prompt']==pre['rendered']['prompt'] and p['seed']==144000+j['seed'] and p['n_predict']==1024 and p['temperature']==.7 and p['cache_prompt'] is False and p['stream'] is False;assert pre['messages']==read(j['messages_path']) and pre['output_capacity']['prompt_tokens']+1024<=4096
 assert 6<=len(starts)<=50 and len(set(starts))==len(starts) and len(responses)<len(starts) and ('smollm3_3b','bayes_11') not in responses
 seal=read(O+'selection_seal.json');assert seal['choices_sha256']==sha(O+'choices.json');choices=read(O+'choices.json');assert len(choices)==50
 for j in choices:
  c=cs[j['app']];p=read(j['prefix']);key=j['model']+'_'+j['key'];arm=read(O+'models/'+key+'.json');r=responses.get((j['model'],j['key']));s=json.loads(json.dumps(p))
  if r:
   z=r['response'];rows=json.loads(z['content']);assert len(rows)==10 and z['content']==json.dumps(rows,separators=(',',':')) and z['stop_type']=='eos' and z['truncated'] is False and 0<z['tokens_predicted']<=1024;props=[[int(ch) for ch in row] for row in rows];ids,diags=project(c,p,props);assert ids==j['selected_rows'] and diags==j['projection'] and not arm['fallback']
  else:assert arm['fallback'] and j['status'] in ['interrupted','unattempted']
  for step,e in enumerate(bykey[key]):
   assert e['at_unix']>=seal['at_unix'];assert (ids[step] if r else choose(c,s,'sequential_3nn'))==e['row_id'];s['ids'].append(e['row_id']);s['labels'].append([e.get('value')])
  assert len(bykey[key])==10 and s==arm['state'] and len(set(s['ids']))==20
 if (ROOT/O/'comparison.json').exists():
  from fractions import Fraction
  report=read(O+'comparison.json');assert report['charged_acquisitions']==len(events) and report['missing_acquisitions']==len(allmissing) and report['finite_acquisitions']==2000-len(allmissing) and len(report['cases'])==50
  for r in report['cases']:
   model=r['model'];case=r['key'];arm=read(O+'models/'+model+'_'+case+'.json');mm=any(y[0] is None for y in arm['state']['labels']);assert r['model_best_observed']==arm['target'] and r['fallback']==arm['fallback'] and r['model_missing']==mm
   for mode,g in r['contrasts'].items():
    control=read(O+'classical/'+case+'_'+mode+'.json');cm=any(y[0] is None for y in control['state']['labels']);expected=float((Fraction(str(control['target']))-Fraction(str(arm['target'])))/Fraction(str(control['target'])));assert close(g['gain'],expected) and g['scorable']==(not cm and not mm)
   for policy,q in r['policies'].items():
    call={'never':False,'always':True}.get(policy,decisions[case].get(policy));assert q['escalate']==call and q['gain']==(r['contrasts']['sequential_3nn']['gain'] if call else 0)
  for model,summary in report['models'].items():
   rs=[r for r in report['cases'] if r['model']==model]
   for mode,q in summary['contrasts'].items():
    ok=[r for r in rs if r['contrasts'][mode]['scorable']];assert q['intended']==25 and q['scorable']==len(ok) and q['inconclusive']==25-len(ok)
    means=[]
    for app in cs:
     vals=[r['contrasts'][mode]['gain'] for r in ok if r['app']==app];assert q['workload_denominators'][app]==len(vals)
     if vals:assert close(q['workload_means_complete_pairs'][app],statistics.mean(vals));means.append(statistics.mean(vals))
    assert close(q['equal_workload_mean_complete_pairs'],statistics.mean(means))
   model_responses=[v for (m,k),v in responses.items() if m==model];cost=summary['cost'];model_starts=sum(m==model for m,k in starts);assert cost['request_starts']==model_starts and cost['complete_responses']==len(model_responses) and cost['missing_usage_requests']==model_starts-len(model_responses) and cost['observed_generated_tokens_lower_bound']==sum(r['response']['tokens_predicted'] for r in model_responses) and cost['observed_prefill_tokens_lower_bound']==sum(r['response']['tokens_evaluated'] for r in model_responses)
 complete=read(O+'completion.json');assert complete['total_acquisitions']==2000 and complete['total_collection_seconds']<1800
 return {'verified':True,'original_and_repair_request_starts':len(starts),'complete_responses':len(responses),'incomplete_response_usage_unknown':len(starts)-len(responses),'unattempted_intents':50-len(starts),'total_charged_acquisitions':2000,'missing_acquisitions':len(allmissing),'finite_acquisitions':2000-len(allmissing),'independent_software_families':1,'B20_arms':175,'no_new_collection':True}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
