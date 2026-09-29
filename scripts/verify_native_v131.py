"""Independent stdlib replay; no native/model execution or optimizer imports."""
import argparse,hashlib,itertools,json,math,random,statistics,struct
from fractions import Fraction
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--compact',action='store_true');args=ap.parse_args();root=args.root
 def read(n):return json.loads((root/n).read_text())
 def lines(n):return [json.loads(l) for l in (root/n).read_text().splitlines()]
 def digest(n):
  h=hashlib.sha256()
  with (root/n).open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  return h.hexdigest()
 a='artifacts/study_v131';o='results/v131_native';m='results/v131_proposals'
 if not args.compact:
  for n,h in read('reports/protocol_v131.freeze.json')['sha256'].items():assert digest(n)==h,n
 for n,h in read(a+'/inputs.freeze.json')['sha256'].items():assert digest(n)==h,n
 work=read(a+'/workloads.json');ref=None
 if not args.compact:
  ref=[complex(*pair) for pair in struct.iter_unpack('<dd',(root/work['fftw_reference']['path']).read_bytes())];assert len(ref)==24576 and all(math.isfinite(abs(v)) for v in ref)
 xs={'wavpack':list(itertools.product([0,1,2,3],[0,2,4,6],[0,2048,8192,32768,65536])),'fftw':list(itertools.product([0,1,2],[1,2,4],[0,1],[1,2]))};expert={'wavpack':(3,6,0),'fftw':(2,1,0,1)};default={'wavpack':(1,0,0),'fftw':(1,1,0,1)}
 records={};counts={'wavpack':0,'fftw':0};calls={'wavpack_encodes':0,'wavpack_decodes':0,'fftw_worker_calls':0}
 for phase,cap in [('classical',500),('continuations',148)]:
  folder=o+'/'+phase;starts=lines(folder+'/starts.jsonl');ledger=read(folder+'/ledger.json');commands=lines(folder+'/commands.jsonl');cursor=0
  assert len(starts)==ledger['configuration_attempts']==ledger['completed_configurations']==cap and ledger['seconds']<ledger['seconds_cap']
  assert [r['attempt'] for r in starts]==list(range(1,cap+1))
  for s in starts:
   r=read(folder+'/'+s['key']+'/result.json');assert r['task']==s['task'] and r['row']==s['row'] and r['settings']==s['settings']==list(xs[r['task']][r['row']]);assert r['valid'] is True and type(r['target']) is int and r['target']>0
   records[(phase,r['key'])]=r;counts[r['task']]+=1
   if r['task']=='wavpack':
    assert len(r['records'])==3 and r['target']==sum(w['bytes'] for w in r['records']);expected=[]
    for j,w in enumerate(r['records']):
     assert w['decoded_sha256']==work['workloads'][j]['raw_sha256'] and w['decoded_bytes']==work['workloads'][j]['raw_bytes'];expected.extend([w['encode'],w['decode']])
     if not args.compact:assert digest(w['encoded_path'])==w['encoded_sha256'] and (root/w['encoded_path']).stat().st_size==w['bytes']
   else:
    metrics=r['metrics'];assert metrics==json.loads(r['records'][0]['stdout']);assert r['target']==metrics['target_ns']==sum(metrics['workload_ns'])
    assert metrics['n']==8192 and metrics['clips']==3 and metrics['iterations_per_clip']==256 and metrics['warmup_per_clip']==8
    assert r['validation']['validated_complex_values']==24576 and r['validation']['max_absolute_error']<=r['validation']['tolerance'];expected=r['records']
    if not args.compact:
     assert digest(r['output_path'])==r['output_sha256'];actual=[complex(*p) for p in struct.iter_unpack('<dd',(root/r['output_path']).read_bytes())];assert len(actual)==24576 and all(math.isfinite(abs(v)) for v in actual)
     error=max(abs(x-y) for x,y in zip(actual,ref));bound=1e-10*max(1,max(map(abs,ref)));assert error<=bound
   assert commands[cursor:cursor+len(expected)]==expected;cursor+=len(expected)
  assert cursor==len(commands) and all(c['returncode']==0 and c['seconds']<=10 for c in commands)
  for k in calls:calls[k]+=ledger[k]
 assert counts=={'wavpack':303,'fftw':345} and calls=={'wavpack_encodes':909,'wavpack_decodes':909,'fftw_worker_calls':345}
 reqs=lines(m+'/generation_starts.jsonl');responses={r['key']:r['response'] for r in lines(m+'/responses.jsonl')};ledger=read(m+'/ledger.json');assert len(reqs)==len(responses)==ledger['generation_requests']==10
 assert ledger['allocated_output_tokens']==10240 and ledger['server_exit_code']==0 and ledger['resource_stop_reason'] is None and ledger['stage_seconds']<=600 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['retries']==0
 props={}
 for req in reqs:
  key=req['identity'];pre=read(m+'/preflight/'+key+'.json');task=pre['task'];ds=[sorted({x[k] for x in xs[task]}) for k in range(len(xs[task][0]))];p=req['payload'];res=responses[key]
  assert pre['domains']==ds and p['prompt']==pre['rendered']['prompt'] and p['seed']==131000+pre['seed'] and p['n_predict']==1024 and p['temperature']==.7 and p['top_p']==.95 and p['cache_prompt'] is False and p['stream'] is False
  assert len(pre['prompt_tokens'])+1024<=4096 and res['truncated'] is False and res['stop_type']=='eos' and 0<res['tokens_predicted']<=1024
  raw=json.loads(res['content']);assert len(raw)==10 and all(len(v)==len(ds) for v in raw);props[key]=[tuple(ds[k][int(c)] for k,c in enumerate(v)) for v in raw]
  saved=read(m+'/scores/'+key+'.json');assert saved['status']=='valid' and saved['score']==[list(v) for v in props[key]]
  prefix=read(pre['prefix_path']);assert digest(pre['prefix_path'])==pre['prefix_sha256'];body=json.loads(pre['messages'][1]['content']);assert body['symbol_to_value']==ds
  assert body['observed_examples']==[{'settings':''.join(str(ds[k].index(v)) for k,v in enumerate(xs[task][row])),'performance':f'{y[0]:.6f}'} for row,y in zip(prefix['ids'],prefix['labels'])]
 def rank(task,ids,ys,order):
  scores={}
  for row in order:
   if row in ids:continue
   near=sorted(range(len(ids)),key=lambda k:sum(a!=b for a,b in zip(xs[task][row],xs[task][ids[k]])))[:3];scores[row]=sum(Fraction(ys[k]) for k in near)/3
  return sorted(scores,key=scores.get)
 def project(task,rows,ids,order):
  used=set(ids);out=[]
  for v in rows:
   row=min((i for i in order if i not in used),key=lambda i:sum(a!=b for a,b in zip(v,xs[task][i])));out.append(row);used.add(row)
  return out
 comparison=read(o+'/comparison.json');incumbents={};gains={}
 for task in xs:
  gains[task]={mode:[] for mode in ['sequential_3nn','batch_3nn','random_projection','random_full','expert','default']}
  for seed in [11,23,37,53,71]:
   order=list(range(len(xs[task])));random.Random(seed).shuffle(order);ids=[];ys=[]
   for k in range(10):
    row=xs[task].index(expert[task]) if k==0 else xs[task].index(default[task]) if k==1 else next(i for i in order if i not in ids) if k==2 else rank(task,ids,ys,order)[0]
    r=records[('classical',f'{task}_{seed}_prefix_{k:02}')];assert row==r['row'];ids.append(row);ys.append(r['target'])
   assert read(o+f'/prefixes/{task}_{seed}.json')=={'ids':ids,'labels':[[y] for y in ys],'order':order}
   values={'expert':ys[0],'default':ys[1]}
   for mode in ['sequential_3nn','batch_3nn','random_projection','random_full','llm']:
    arm=read(o+f'/arms/{task}_{seed}_{mode}.json');bid=ids[:];by=ys[:];batch=None
    if mode=='batch_3nn':batch=rank(task,ids,ys,order)[:10]
    if mode=='random_full':batch=random.Random(131400+seed).sample([i for i in order if i not in ids],10)
    if mode=='random_projection':
     ds=[sorted({x[k] for x in xs[task]}) for k in range(len(xs[task][0]))];rng=random.Random(131900+seed);batch=project(task,[tuple(rng.choice(d) for d in ds) for _ in range(10)],ids,order)
    if mode=='llm':batch=project(task,props[f'{task}_{seed}'],ids,order);assert arm['fallback'] is False
    for k in range(10):
     row=rank(task,bid,by,order)[0] if batch is None else batch[k];r=records[('continuations' if mode=='llm' else 'classical',f'{task}_{seed}_{mode}_{k:02}')];assert row==r['row'] and row not in bid;bid.append(row);by.append(r['target'])
    assert arm['state']=={'ids':bid,'labels':[[y] for y in by],'order':order};assert arm['best']==min(by) and arm['incumbent']==bid[by.index(min(by))];values[mode]=min(by);incumbents[(task,seed,mode)]=arm['incumbent']
   comp=next(r for r in comparison['rows'] if r['task']==task and r['seed']==seed)
   for mode,v in values.items():assert comp[mode]==v
   for mode in gains[task]:gains[task][mode].append(Fraction(values[mode]-values['llm'],values[mode]))
 for task,modes in gains.items():
  for mode,gg in modes.items():
   saved=comparison['summary'][task]['selection_time_comparisons'][mode];assert saved['mean_fraction']==str(sum(gg)/5);assert (saved['wins'],saved['ties'],saved['losses'])==(sum(g>0 for g in gg),sum(g==0 for g in gg),sum(g<0 for g in gg))
 val=read(o+'/fresh_validation.json')['records'];assert len(val)==45;fresh=[];pos=0
 for seed in [11,23,37,53,71]:
  for block in range(3):
   modes=['sequential_3nn','llm','expert'];random.Random(131800+seed*10+block).shuffle(modes)
   for mode in modes:
    v=val[pos];pos+=1;assert v['seed']==seed and v['block']==block and v['mode']==mode
    row=xs['fftw'].index(expert['fftw']) if mode=='expert' else incumbents[('fftw',seed,mode)];r=records[('continuations',v['key'])];assert v['row']==r['row']==row and v['target']==r['target']
  med={mode:statistics.median(v['target'] for v in val if v['seed']==seed and v['mode']==mode) for mode in ['sequential_3nn','llm','expert']};g=Fraction(med['sequential_3nn']-med['llm'],med['sequential_3nn']);fresh.append(g)
  saved=next(r for r in comparison['rows'] if r['task']=='fftw' and r['seed']==seed);assert saved['fresh_medians_ns']==med and saved['fresh_gain_fraction']==str(g)
 saved=comparison['summary']['fftw']['fresh_validation_primary'];assert saved['mean_fraction']==str(sum(fresh)/5)
 assert len({records[('continuations',f'wavpack_expert_repeat_{k}')]['target'] for k in range(3)}|{records[('classical',f'wavpack_{s}_prefix_00')]['target'] for s in [11,23,37,53,71]})==1
 print(json.dumps({'verified':True,'configuration_attempts':648,'by_family':counts,'calls':calls,'paired_arms':50,'real_model_requests':10,'fresh_validation_trials':45,'groups':2,'compact':args.compact,'physical_outputs_and_dependency_freeze_checked':not args.compact}))
if __name__=='__main__':main()
