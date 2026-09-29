"""Independent stdlib saved-evidence replay; never runs model or objective oracle."""
import argparse,hashlib,itertools,json,random
from fractions import Fraction
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--compact',action='store_true');args=ap.parse_args();root=args.root
 def read(p):return json.loads((root/p).read_text())
 def lines(p):return [json.loads(x) for x in (root/p).read_text().splitlines()]
 def digest(p):
  h=hashlib.sha256()
  with (root/p).open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  return h.hexdigest()
 native='results/v130_native';model='results/v130_proposals';art='artifacts/study_v130'
 if not args.compact:
  for n,h in read('reports/protocol_v130.freeze.json')['sha256'].items():assert digest(n)==h,n
 for n,h in read(art+'/inputs.freeze.json')['sha256'].items():assert digest(n)==h,n
 xs=list(itertools.product([1024,1536,2048,3072,4096,4608],[4,8,10,12],[0,2,4,6]));preset=xs.index((4096,12,6));ds=[sorted({x[k] for x in xs}) for k in range(3)]
 workloads=read(art+'/workloads.json')['workloads'];records={};physical={'encode':0,'decode':0}
 for phase,expected in [('classical',250),('continuations',53)]:
  folder=native+'/'+phase;starts=lines(folder+'/starts.jsonl');ledger=read(folder+'/ledger.json');assert len(starts)==ledger['configuration_attempts']==ledger['completed_configurations']==expected
  assert ledger['seconds']<ledger['max_seconds']
  assert [s['attempt'] for s in starts]==list(range(1,expected+1))
  commands=lines(folder+'/commands.jsonl');assert len(commands)==expected*6
  assert all(c['returncode']==0 and c['seconds']<=10 for c in commands)
  for s in starts:
   r=read(folder+'/'+s['key']+'/result.json');assert r['key'] not in records
   records[r['key']]=r;assert r['row']==s['row'] and r['settings']==s['settings']==list(xs[r['row']]);assert r['valid'] is True and len(r['workloads'])==3
   assert r['target_bytes']==sum(w['bytes'] for w in r['workloads'])
   for j,w in enumerate(r['workloads']):
    assert w['decoded_sha256']==workloads[j]['raw_sha256'] and w['decoded_bytes']==workloads[j]['raw_bytes'] and w['bytes']>0
    assert w['encode']['returncode']==w['decode']['returncode']==0
    if not args.compact:assert digest(w['encoded_path'])==w['encoded_sha256'] and (root/w['encoded_path']).stat().st_size==w['bytes']
   expected_commands=[z for w in r['workloads'] for z in [w['encode'],w['decode']]]
   assert commands[6*(s['attempt']-1):6*s['attempt']]==expected_commands
  for kind in physical:
   assert ledger[kind+'_attempts']==expected*3;physical[kind]+=ledger[kind+'_attempts']
 starts=lines(model+'/generation_starts.jsonl');responses=lines(model+'/responses.jsonl');ledger=read(model+'/ledger.json')
 assert len(starts)==len(responses)==ledger['generation_requests']==5
 assert ledger['allocated_output_tokens']==5120 and ledger['retries']==0 and ledger['server_exit_code']==0 and ledger['resource_stop_reason'] is None
 assert ledger['stage_seconds']<=900 and ledger['peak_server_rss_bytes']<=8589934592
 responses={r['key']:r['response'] for r in responses};proposals={}
 for req in starts:
  key=req['identity'];p=req['payload'];response=responses[key];pre=read(model+'/preflight/'+key+'.json')
  assert p['prompt']==pre['rendered']['prompt'] and p['seed']==pre['sampling_seed'] and pre['domains']==ds
  assert p['n_predict']==1024 and p['temperature']==.7 and p['top_p']==.95 and p['top_k']==0 and p['min_p']==0 and p['repeat_penalty']==1 and p['stream'] is False and p['cache_prompt'] is False
  assert len(pre['prompt_tokens'])+1024<=4096 and pre['output_capacity']['constructive_token_upper_bound_including_eos']==62
  assert response['truncated'] is False and response['stop_type']=='eos' and 0<response['tokens_predicted']<=1024
  raw=json.loads(response['content']);assert len(raw)==10 and all(len(s)==3 for s in raw)
  proposals[key]=[tuple(ds[k][int(c)] for k,c in enumerate(s)) for s in raw]
  cached=read(model+'/scores/'+key+'.json');assert cached['status']=='valid' and cached['score']==[list(x) for x in proposals[key]]
  prefix=read(pre['prefix_path']);assert digest(pre['prefix_path'])==pre['prefix_sha256']
  body=json.loads(pre['messages'][1]['content']);assert len(body['observed_examples'])==10
  assert [e['performance'] for e in body['observed_examples']]==[f'{y[0]:.6f}' for y in prefix['labels']]
  assert [e['settings'] for e in body['observed_examples']]==[''.join(str(ds[k].index(v)) for k,v in enumerate(xs[i])) for i in prefix['ids']]
 def rank(ids,values,order):
  scores={}
  for i in order:
   if i in ids:continue
   neighbors=sorted(range(len(ids)),key=lambda k:sum(xs[i][d]!=xs[ids[k]][d] for d in range(3)))[:3]
   scores[i]=sum(Fraction(values[k]) for k in neighbors)/3
  return sorted(scores,key=scores.get)
 def projection(rows,ids,order):
  seen=set(ids);chosen=[]
  for x in rows:
   row=min((i for i in order if i not in seen),key=lambda i:sum(a!=b for a,b in zip(x,xs[i])))
   chosen.append(row);seen.add(row)
  return chosen
 comparisons=read(native+'/comparison.json');gains={m:[] for m in ['sequential_3nn','batch_3nn','random_projection','random_full','preset']}
 for seed in [11,23,37,53,71]:
  order=list(range(96));random.Random(seed).shuffle(order);ids=[];values=[]
  for k in range(10):
   chosen=preset if k==0 else next(i for i in order if i not in ids) if k<3 else rank(ids,values,order)[0]
   r=records[f's{seed}_prefix_{k:02}'];assert r['row']==chosen;ids.append(chosen);values.append(r['target_bytes'])
  prefix=read(native+f'/prefixes/{seed}.json');assert prefix=={'ids':ids,'labels':[[v] for v in values],'order':order}
  best={}
  for mode in ['sequential_3nn','batch_3nn','random_projection','random_full','llm']:
   arm=read(native+f'/arms/{seed}_{mode}.json');branch_ids=ids[:];branch_values=values[:];batch=None
   if mode=='batch_3nn':batch=rank(ids,values,order)[:10]
   if mode=='random_full':batch=random.Random(130400+seed).sample([i for i in order if i not in ids],10)
   if mode=='random_projection':
    rng=random.Random(130900+seed);batch=projection([tuple(rng.choice(d) for d in ds) for _ in range(10)],ids,order)
   if mode=='llm':batch=projection(proposals[f'flac_{seed}'],ids,order);assert arm['fallback'] is False
   for k in range(10):
    chosen=rank(branch_ids,branch_values,order)[0] if batch is None else batch[k];r=records[f's{seed}_{mode}_{k:02}'];assert r['row']==chosen and chosen not in branch_ids;branch_ids.append(chosen);branch_values.append(r['target_bytes'])
   assert arm['state']=={'ids':branch_ids,'labels':[[v] for v in branch_values],'order':order}
   assert arm['best_bytes']==min(branch_values);best[mode]=min(branch_values)
  best['preset']=values[0]
  row=next(r for r in comparisons['rows'] if r['seed']==seed)
  for m,b in best.items():assert row[m+'_bytes']==b
  for m in gains:gains[m].append(Fraction(best[m]-best['llm'],best[m]))
 for m,gg in gains.items():
  summary=comparisons['comparisons'][m];assert summary['mean_gain_fraction']==str(sum(gg)/5)
  assert (summary['wins'],summary['ties'],summary['losses'])==(sum(g>0 for g in gg),sum(g==0 for g in gg),sum(g<0 for g in gg))
 repeats=[records[f'preset_repeat_{k}']['target_bytes'] for k in range(3)];assert len(set(repeats+[records[f's{s}_prefix_00']['target_bytes'] for s in [11,23,37,53,71]]))==1
 assert read(native+'/determinism.json')['targets']==repeats
 print(json.dumps({'verified':True,'configuration_attempts':len(records),'encoder_calls':physical['encode'],'decoder_calls':physical['decode'],'real_model_requests':len(starts),'paired_arms':25,'independent_groups':1,'compact':args.compact,'native_bytes_checked':not args.compact}))
if __name__=='__main__':main()
