"""Independent standard-library replay; no model, optimizer or evaluator imports."""
import argparse,csv,hashlib,json,math,random,statistics
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ABC='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
SYSTEM='Optimize software configurations using the acquired measurements shown. Propose two diverse promising configurations. Settings encode each feature by its index in symbol_to_value using 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. A null performance value means the measurement is withheld; do not infer its value. Do not repeat any initial or newly evaluated settings or your own proposals. Feature-distance projection will map proposals to valid unobserved rows. Output only a JSON array of two setting strings.'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
def verify(root=ROOT,compact=False):
 out=root/'results/v136_feedback';jobs=read(root/'artifacts/study_v136/jobs.json');summary=read(out/'summary.json');cfg=read(root/'configs/study_v136.json');ledger=read(out/'ledger.json')
 assert summary['complete'] and summary['error'] is None and summary['new_acquisitions']==200
 assert len(jobs)==10 and summary['intended_arms']==20 and summary['intended_requests']==100
 widths=read(root/'artifacts/study_v136/admission.json')['widths'];groups=sorted(widths,key=lambda g:(widths[g],g));assert {j['system_group'] for j in jobs}=={groups[0],groups[-1]}
 order=sorted(jobs,key=lambda j:(j['system_group'],j['seed']));random.Random(136000).shuffle(order);assert order==jobs
 for group in {j['system_group'] for j in jobs}:assert sorted(j['seed'] for j in jobs if j['system_group']==group)==[11,23,37,53,71]
 responses=lines(out/'responses.jsonl');starts=lines(out/'generation_starts.jsonl');acqs=lines(out/'acquisitions.jsonl')
 assert len(acqs)==200 and len(starts)==ledger['generation_requests']<=100
 assert ledger['allocated_output_tokens']==256*len(starts)<=25600 and ledger['retries']==ledger['external_spend_usd']==0
 assert ledger['peak_server_rss_bytes']<=cfg['max_server_rss_bytes'] and ledger['stage_seconds']<=1600 and summary['total_seconds']<=1800
 raw={r['identity']:r for r in responses};startmap={r['identity']:r for r in starts};assert len(raw)==len(responses) and len(startmap)==len(starts) and set(raw)<=set(startmap)
 assert [r['generation'] for r in starts]==list(range(1,len(starts)+1))
 intended=[];valid=0;fallback=0;zero_equal=0;acq_index=0;all_results=[];source_cache={};projected=0;repeated=0;matches=0;evaluation_seconds=0
 for index,j in enumerate(jobs):
  snap=read(root/f"artifacts/study_v136/candidates/{j['system_group']}.json");xs=snap['x'];spec=snap['spec'];ds=[sorted({x[k] for x in xs}) for k in range(len(xs[0]))];assert ds==j['domains']
  prefix=read(root/j['prefix'])['state'];assert sha(root/j['prefix'])==j['prefix_sha256']
  if spec['path'] not in source_cache:
   if compact:
    extract=read(root/f"artifacts/study_v136/source_extracts/{j['system_group']}.json");assert extract['source_sha256']==spec['sha256'];source_cache[spec['path']]={int(k):v for k,v in extract['lines'].items()}
   else:
    p=root/spec['path'];assert sha(p)==spec['sha256'];source_cache[spec['path']]={i+1:x for i,x in enumerate(p.read_text().splitlines())}
  source=source_cache[spec['path']];header=next(csv.reader([source[1]],delimiter=spec['delimiter']))
  state={m:{'ids':prefix['ids'][:],'labels':[x[:] for x in prefix['labels']],'order':prefix['order'][:]} for m in ['feedback','masked']}
  initial_raw={}
  for step in j['schedule']:
   r=step['round'];assert step['sampling_seed']==136000+index*100+r
   modes=['feedback','masked'];random.Random(step['sampling_seed']).shuffle(modes);assert modes==step['arm_order']
   for mode in modes:
    identity=f"{j['key']}_{mode}_{r}";intended.append(identity);s=state[mode];d=read(out/'decisions'/f'{identity}.json');sel=read(out/'selections'/f'{identity}.json');after=read(out/'rounds'/f'{identity}.json')
    assert d['identity']==sel['identity']==after['identity']==identity and d['round']==r and d['arm']==mode and d['sampling_seed']==step['sampling_seed']
    assert all(d['before'][k]==s[k] for k in ['ids','labels','order']) and len(s['ids'])==10+2*r
    def example(i,y,reveal):return {'settings':''.join(ABC[dom.index(v)] for dom,v in zip(ds,xs[i])),'performance':f'{y[0]:.6f}' if reveal else None}
    body={'feature_order':snap['names'],'symbol_to_value':ds,'performance_meaning':spec['meaning'],'direction':'minimize' if spec['direction']=='-' else 'maximize','initial_observations':[example(i,y,True) for i,y in zip(prefix['ids'],prefix['labels'])],'new_evaluations':[example(i,y,mode=='feedback') for i,y in zip(s['ids'][10:],s['labels'][10:])],'remaining_evaluations':20-len(s['ids'])}
    msgs=[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(body,separators=(',',':'))}];assert d['messages']==msgs
    assert sel['decision_sha256']==sha(out/'decisions'/f'{identity}.json') and after['selection_sha256']==sha(out/'selections'/f'{identity}.json')
    assert d['at_unix']<=sel['at_unix']<=after['at_unix']
    proposals=None
    if identity in raw:
     response=raw[identity]['response'];pf=read(out/'preflight'/f'{identity}.json');p=pf['payload'];st=startmap[identity]
     assert st['payload']==p and st['kind']=='scientific' and p['seed']==step['sampling_seed'] and p['n_predict']==256
     expected={'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'stream':False,'cache_prompt':False,'return_tokens':True}
     assert all(p[k]==v for k,v in expected.items())
     grammar='root ::= "[" row "," row "]"\nrow ::= "\\\"" '+' '.join('['+ABC[:len(dom)]+']' for dom in ds)+' "\\\""\n'
     assert p['grammar']==grammar and p['prompt']==pf['rendered']['prompt'] and all(m['content'] in p['prompt'] for m in msgs)
     assert pf['decision_sha256']==sha(out/'decisions'/f'{identity}.json') and len(pf['prompt_tokens'])+256<=4096
     assert pf['capacity']['constructive_token_upper_bound_including_eos']==2*(len(ds)+3)+2
     assert d['at_unix']<=pf['at_unix']<=st['at_unix']<=raw[identity]['at_unix']<=sel['at_unix']
     try:
      z=json.loads(response['content']);assert response['truncated'] is False and response['stop_type']=='eos' and type(response['tokens_predicted']) is int and 0<response['tokens_predicted']<=256
      assert len(z)==2 and all(isinstance(x,str) and len(x)==len(ds) and all(c in ABC[:len(dom)] for c,dom in zip(x,ds)) for x in z) and response['content']==json.dumps(z,separators=(',',':'))
      proposals=[[dom[ABC.index(c)] for dom,c in zip(ds,x)] for x in z]
     except (AssertionError,ValueError,KeyError,TypeError):pass
     if r==0:initial_raw[mode]=response['content']
    if proposals is not None:
     valid+=1;assert not sel['fallback'];seen=set(s['ids']);chosen=[];diagnostics=[];prior=[]
     for prop in proposals:
      row=min((i for i in s['order'] if i not in seen),key=lambda i:sum(a!=b for a,b in zip(prop,xs[i])))
      diagnostics.append({'proposal':prop,'row_id':row,'hamming_distance':sum(a!=b for a,b in zip(prop,xs[row])),'repeated_proposal':prop in prior,'matches_acquired':any(prop==xs[i] for i in s['ids'])});prior.append(prop);chosen.append(row);seen.add(row)
     assert sel['diagnostics']==diagnostics
     projected+=sum(d['hamming_distance']>0 for d in diagnostics);repeated+=sum(d['repeated_proposal'] for d in diagnostics);matches+=sum(d['matches_acquired'] for d in diagnostics)
    else:
     fallback+=1;assert sel['fallback'] and sel['reason'];scored=[]
     for i in s['order']:
      if i in s['ids']:continue
      near=sorted(range(len(s['ids'])),key=lambda k:sum(a!=b for a,b in zip(xs[i],xs[s['ids'][k]])))[:3]
      value=sum(Decimal(str(s['labels'][k][0])) for k in near)/3
      scored.append((value if spec['direction']=='-' else -value,i))
     chosen=[x[1] for x in sorted(scored,key=lambda x:x[0])[:2]]
    assert chosen==sel['rows'] and len(set(chosen))==2 and not set(chosen)&set(s['ids'])
    for i in chosen:
     a=acqs[acq_index];acq_index+=1;line=snap['source_ids'][i];assert a['key']==j['key'] and a['arm']==mode and a['row_id']==i and a['source_line']==line and sel['at_unix']<=a['at_unix']<=after['at_unix']
     row=dict(zip(header,next(csv.reader([source[line]],delimiter=spec['delimiter']))));assert [float(row[k]) for k in snap['names']]==xs[i] and a['raw_target']==row[spec['primary_objective']]
     y=float(a['raw_target']);assert math.isfinite(y) and y>0;s['ids'].append(i);s['labels'].append([y])
    assert all(after['state'][k]==s[k] for k in ['ids','labels','order'])
    evaluation_seconds+=after['evaluation_seconds']
  zero_equal+=int(len(initial_raw)==2 and initial_raw['feedback']==initial_raw['masked'])
  results={'key':j['key'],'system_group':j['system_group'],'seed':j['seed'],'direction':spec['direction']}
  best=lambda s:(min if spec['direction']=='-' else max)(y[0] for y in s['labels'])
  results['prefix']=best(prefix)
  for mode,s in state.items():
   arm=read(out/'arms'/f"{j['key']}_{mode}.json");assert arm['new_acquisitions']==10 and len(set(s['ids']))==20 and all(arm['state'][k]==s[k] for k in ['ids','labels','order']);results[mode]=best(s)
  for name in ['historical_batch','historical_sequential']:
   s=read(root/j[name])['state'];assert len(set(s['ids']))==20 and s['ids'][:10]==prefix['ids'] and s['labels'][:10]==prefix['labels'];results[name]=best(s)
  all_results.append(results)
 assert valid+fallback==100 and acq_index==200 and [s['identity'] for s in starts]==[i for i in intended if i in startmap]
 assert len(list((out/'decisions').glob('*.json')))==len(list((out/'selections').glob('*.json')))==len(list((out/'rounds').glob('*.json')))==100
 result={'verified':True,'source_verification':'charged-row extracts only' if compact else 'full source hashes and charged rows','intended_rounds':100,'valid_rounds':valid,'fallback_rounds':fallback,'arms':20,'recorded_acquisitions':200,'round_zero_same_output_cases':zero_equal,'rows':all_results}
 comparison=out/'comparison.json'
 if comparison.exists():
  a=read(comparison);assert a['rows']==all_results
  gain=lambda ref,value,direction:(ref-value)/ref if direction=='-' else (value-ref)/ref
  def contrast(v):return {'mean':statistics.mean(v),'wins':sum(x>1e-12 for x in v),'ties':sum(abs(x)<=1e-12 for x in v),'losses':sum(x< -1e-12 for x in v)}
  for group in sorted({r['system_group'] for r in all_results}):
   rs=[r for r in all_results if r['system_group']==group];g={}
   for mode in ['feedback','masked']:
    for ref in ['prefix','historical_sequential','historical_batch']:g[f'{mode}_vs_{ref}']=contrast([gain(r[ref],r[mode],r['direction']) for r in rs])
   g['feedback_vs_masked']=contrast([gain(r['masked'],r['feedback'],r['direction']) for r in rs]);assert a['groups'][group]==g
  assert a['diagnostics']=={'valid_rounds':valid,'fallback_rounds':fallback,'projected_proposals':projected,'repeated_within_round':repeated,'proposals_matching_acquired':matches,'proposals_with_diagnostics':valid*2,'same_round_zero_output_cases':zero_equal}
  cost=a['actual_collection_cost'];assert all(cost[k]==v for k,v in ledger.items());assert math.isclose(cost['evaluation_seconds'],evaluation_seconds,abs_tol=1e-9)
  assert cost['new_recorded_acquisitions']==200 and cost['total_collection_seconds']==summary['total_seconds']
  for field in ['tokens_predicted','tokens_evaluated']:
   values=[r['response'].get(field) for r in responses];assert cost['usage'][field]=={'observed_sum':sum(v for v in values if type(v) is int),'missing_intended_responses':100-sum(type(v) is int for v in values)}
  for j in jobs:
   for m in ['feedback','masked']:
    rs=[r for r in responses if r['identity'].startswith(f"{j['key']}_{m}_")];assert cost['per_arm'][f"{j['key']}_{m}"]=={'observed_request_seconds':sum(r['wall_seconds'] for r in rs),'requests_returned':len(rs)}
  assert a['estimated_deployment']['objective_evaluations']==20 and a['estimated_deployment']['prefix']==10 and a['estimated_deployment']['model_requests_per_escalation']==5 and a['estimated_deployment']['allocated_output_tokens']==1280
 tracepath=out/'followup_trace.json'
 if tracepath.exists():
  trace=[]
  for j in jobs:
   for r in range(1,5):
    a=f"{j['key']}_feedback_{r}";b=f"{j['key']}_masked_{r}"
    trace.append({'key':j['key'],'system_group':j['system_group'],'round':r,'both_responses':a in raw and b in raw,'same_output':a in raw and b in raw and raw[a]['response']['content']==raw[b]['response']['content'],'same_selected_rows':read(out/'selections'/f'{a}.json')['rows']==read(out/'selections'/f'{b}.json')['rows']})
  assert read(tracepath)['pairs']==trace
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--compact',action='store_true');args=ap.parse_args();print(json.dumps(verify(args.root,args.compact),indent=2))
