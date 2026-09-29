"""Independent stdlib verification; imports no model adapter or optimizer."""
import argparse,csv,hashlib,json,math,random
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
from datetime import datetime
ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def verify(root,compact=False):
 def read(n):return json.loads((root/n).read_text())
 def sha(n):
  h=hashlib.sha256()
  with (root/n).open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  return h.hexdigest()
 def lines(n):return [json.loads(x) for x in (root/n).read_text().splitlines()]
 def gain(a,b,d):return (F(str(a))-F(str(b)))/F(str(a)) if d=='-' else (F(str(b))-F(str(a)))/F(str(a))
 def stats(gs):return {'cases':len(gs),'mean_fraction':str(sum(gs)/len(gs)),'mean_percent':float(100*sum(gs)/len(gs)),'wins':sum(v>0 for v in gs),'ties':sum(v==0 for v in gs),'losses':sum(v<0 for v in gs),'benefit_over_1pct':sum(v>F(1,100) for v in gs),'harm_over_1pct':sum(v< -F(1,100) for v in gs)}
 if not compact:
  for n,h in read('reports/protocol_v142.freeze.json')['sha256'].items():assert sha(n)==h,n
 for n,h in read('artifacts/study_v141/inputs.freeze.json')['sha256'].items():assert sha(n)==h,n
 cfg=read('configs/study_v141.json');modeldirs=read('artifacts/study_v142/model_paths.json');models=read('artifacts/study_v141/models.json');jobs=read('artifacts/study_v141/jobs.json');summary=read('results/v141_analysis/summary.json');seal=read('results/v141_analysis/selection_seal.json');result=read('results/v141_analysis/comparison.json');journal=lines('results/v141_analysis/acquisitions.jsonl')
 assert len(jobs)==30 and len({j['system_group'] for j in jobs})==6 and set(models)=={'qwen3_8b','smollm3_3b'}
 ordered=sorted(jobs,key=lambda j:(j['system_group'],j['seed']));random.Random(141100).shuffle(ordered);assert jobs==ordered
 modelorder=sorted(models);random.Random(141000).shuffle(modelorder);assert cfg['model_order']==modelorder
 assert summary['complete'] and summary['error'] is None and len(summary['arms'])==summary['intended_arms']==60 and len(journal)==summary['new_recorded_acquisitions']==cfg['total_new_recorded_acquisitions']==600
 assert summary['seconds']<=180 and summary['combined_collection_seconds']<=1800
 for n,h in seal['sha256'].items():assert sha(n)==h,n
 assert all(x['at_unix']>=seal['at_unix'] for x in journal) and [x['at_unix'] for x in journal]==sorted(x['at_unix'] for x in journal)
 source={};verified_rows=[];verified_arms=[];cur=0;responses={};totalrequests=0
 for m in modelorder:
  path=modeldirs[m];ledger=read(path+'/ledger.json');runtime=read(path+'/runtime.json');raw=lines(path+'/responses.jsonl');gens=lines(path+'/generation_starts.jsonl') if (root/path/'generation_starts.jsonl').exists() else []
  assert len(gens)==ledger['generation_requests']<=30 and ledger['allocated_output_tokens']==1024*len(gens)<=30720 and ledger['retries']==ledger['compatibility_requests']==ledger['external_spend_usd']==0
  assert ledger['stage_seconds']<=800 and ledger['peak_server_rss_bytes']<=8589934592 and runtime['config']==({**cfg,'model_key':m} if m=='qwen3_8b' else read('configs/study_v142.json')) and runtime['model']==models[m]
  cmd=runtime['command'];assert cmd[cmd.index('-m')+1].endswith('/'+models[m]['path']) and cmd[cmd.index('--host')+1]=='127.0.0.1' and '--offline' in cmd and cmd[cmd.index('-c')+1]=='4096' and cmd[cmd.index('--reasoning')+1]=='off'
  assert len({x['key'] for x in raw})==len(raw)<=len(gens);responses[m]=raw;totalrequests+=len(gens)
  if gens:
   pfseal=read(path+'/preflight_seal.json')
   for n,h in pfseal['sha256'].items():assert sha(n)==h,n
   assert len(pfseal['sha256'])==30 and datetime.fromisoformat(pfseal['at']).timestamp()<=min(g['at_unix'] for g in gens)
  for j in jobs:
   c=read(f"artifacts/study_v141/candidates/{j['system_group']}.json");xs=c['x'];sp=c['spec'];p=read(j['prefix'])['state'];ds=[sorted({x[i] for x in xs}) for i in range(len(xs[0]))];assert ds==j['domains'] and sha(j['prefix'])==j['prefix_sha256'] and len(p['ids'])==len(p['labels'])==len(set(p['ids']))==10 and set(p['order'])==set(range(len(xs)))
   msg=read(j['messages_path']);assert msg==read(j['old_messages_path']);body=json.loads(msg[1]['content']);assert set(body)=={'feature_order','symbol_to_value','observed_examples','performance_meaning','direction'} and body['feature_order']==c['names'] and body['symbol_to_value']==ds and body['direction']==('minimize' if sp['direction']=='-' else 'maximize')
   expected=[{'settings':''.join(ALPHABET[d.index(v)] for d,v in zip(ds,xs[i])),'performance':f'{y[0]:.6f}'} for i,y in zip(p['ids'],p['labels'])];assert body['observed_examples']==expected
   if sp['path'] not in source:
    ex=read(f"artifacts/study_v141/source_extracts/{j['system_group']}.json");assert ex['source_path']==sp['path'] and ex['source_sha256']==sp['sha256'];source[sp['path']]=ex['lines']
    if not compact:
     assert sha(sp['path'])==sp['sha256'];full=(root/sp['path']).read_text().splitlines()
     for n,t in ex['lines'].items():assert full[int(n)-1]==t
   sl=source[sp['path']];header=next(csv.reader([sl['1']],delimiter=sp['delimiter']))
   def checkrow(row,y):
    cells=dict(zip(header,next(csv.reader([sl[str(c['source_ids'][row])]],delimiter=sp['delimiter']))));assert [float(cells[k]) for k in c['names']]==xs[row] and float(cells[sp['primary_objective']])==y[0] and math.isfinite(y[0]) and y[0]>0;return cells[sp['primary_objective']]
   for i,y in zip(p['ids'],p['labels']):checkrow(i,y)
   rr=next((x for x in raw if x['key']==j['key']),None);gg=next((x for x in gens if x['identity']==j['key']),None);props=None;status='unattempted'
   if gg is not None:
    pf=read(path+f"/preflight/{j['key']}.json");pp=gg['payload'];assert set(pp)=={'prompt','n_predict','temperature','top_p','top_k','min_p','repeat_penalty','seed','grammar','stream','cache_prompt','return_tokens'};assert pp['seed']==141000+j['seed'] and pp['prompt']==pf['rendered']['prompt'] and pf['messages']==msg
    for n,v in {'n_predict':1024,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'stream':False,'cache_prompt':False,'return_tokens':True}.items():assert pp[n]==v
    row=' '.join('['+ALPHABET[:len(d)]+']' for d in ds);gram='root ::= "[" row '+' '.join('\",\" row' for _ in range(9))+' "]"\nrow ::= "\\\"" '+row+' "\\\""\n';assert pp['grammar']==gram
    proof=pf['output_capacity'];assert proof['constructive_token_upper_bound_including_eos']==10*(len(ds)+3)+2<=1024 and len(pf['prompt_tokens'])+1024<=4096 and proof['prompt_tokens']==len(pf['prompt_tokens'])
   if rr is not None:
    assert gg is not None;resp=rr['response'];status='invalid'
    try:
     coded=json.loads(resp['content']);assert resp['truncated'] is False and resp['stop_type']=='eos' and type(resp['tokens_predicted']) is int and 0<resp['tokens_predicted']<=1024
     assert type(coded) is list and len(coded)==10 and resp['content']==json.dumps(coded,separators=(',',':')) and all(type(x) is str and len(x)==len(ds) and all(ch in ALPHABET[:len(d)] for ch,d in zip(x,ds)) for x in coded)
     props=[tuple(d[ALPHABET.index(ch)] for d,ch in zip(ds,x)) for x in coded];status='valid'
    except (AssertionError,ValueError,KeyError,TypeError):props=None
    score=read(path+f"/scores/{j['key']}.json");assert score['status']==status and score['score']==(None if props is None else [list(x) for x in props])
   selected=[];diag=[];seen=set(p['ids']);prior=[]
   if props is not None:
    for x in props:
     i=min((i for i in p['order'] if i not in seen),key=lambda i:sum(a!=b for a,b in zip(x,xs[i])));selected.append(i);seen.add(i);diag.append({'proposal':list(x),'row_id':i,'hamming_distance':sum(a!=b for a,b in zip(x,xs[i])),'repeated_proposal':x in prior,'matches_initial_observation':any(x==tuple(xs[k]) for k in p['ids'])});prior.append(x)
   else:
    def predict(i):
     near=sorted(range(10),key=lambda k:sum(a!=b for a,b in zip(xs[i],xs[p['ids'][k]])))[:3];v=sum(Decimal(str(p['labels'][k][0])) for k in near)/3;return v if sp['direction']=='-' else -v
    selected=sorted((i for i in p['order'] if i not in seen),key=predict)[:10]
   key=m+'_'+j['key'];choice=read(f'results/v141_analysis/choices/{key}.json');arm=read(f'results/v141_analysis/arms/{key}.json');assert choice['selected_rows']==selected and choice['projection']==diag and choice['fallback']==(props is None) and choice['model_status']==status
   events=journal[cur:cur+10];cur+=10;assert [e['row_id'] for e in events]==selected and all(e['key']==key for e in events)
   ys=[]
   for i,e in zip(selected,events):
    y=[float(e['raw_target'])];assert e['source_line']==c['source_ids'][i] and checkrow(i,y)==e['raw_target'];ys.append(y)
   state=arm['state'];assert state['ids']==p['ids']+selected and state['labels']==p['labels']+ys and state['order']==p['order'] and len(set(state['ids']))==20 and arm['new_accesses']==10 and all(arm[k]==v for k,v in choice.items())
   best=lambda st:(min if sp['direction']=='-' else max)(y[0] for y in st['labels'])
   assert arm['direction']==sp['direction'] and arm['target']==best(state) and arm['prefix_best']==best(p)
   refs={}
   for name,ref in arm['references'].items():
    st=read(ref['path'])['state'];assert len(st['ids'])==len(set(st['ids']))==len(st['labels'])==20 and st['ids'][:10]==p['ids'] and st['labels'][:10]==p['labels'] and st['order']==p['order']
    for i,y in zip(st['ids'],st['labels']):checkrow(i,y)
    assert ref['target']==best(st);refs[name]=best(st)
   assert set(refs)=={'sequential_3nn','random_full','fixed_prefix_neighbor','adaptive_incumbent_neighbor'};refs['prefix']=best(p)
   verified_rows.append({'key':key,'case_key':j['key'],'model':m,'system_group':j['system_group'],'seed':j['seed'],'target':best(state),'direction':sp['direction'],'references':refs,'fallback':props is None,'gains':{name:str(gain(v,best(state),sp['direction'])) for name,v in refs.items()}});verified_arms.append(arm)
 assert cur==600 and result['rows']==verified_rows and summary['arms']==[r['key'] for r in verified_rows]
 groups=sorted({j['system_group'] for j in jobs});refs=['sequential_3nn','adaptive_incumbent_neighbor','fixed_prefix_neighbor','random_full','prefix']
 for g in groups:
  assert sorted(j['seed'] for j in jobs if j['system_group']==g)==[11,23,37,53,71]
  for m in models:
   for ref in refs:assert result['groups'][g][m][ref]==stats([F(r['gains'][ref]) for r in verified_rows if r['model']==m and r['system_group']==g])
 for m in models:
  for ref in refs:assert result['totals'][m][ref]==stats([F(r['gains'][ref]) for r in verified_rows if r['model']==m])
  raw=responses[m];cost=result['cost']['actual'][m];assert cost['ledger']==read(modeldirs[m]+'/ledger.json') and cost['new_recorded_acquisitions']==300 and cost['request_wall_seconds']==sum(x['wall_seconds'] for x in raw)
  for field in ['tokens_predicted','tokens_evaluated']:
   vs=[r['response'].get(field) for r in raw];assert cost['usage'][field]=={'observed_sum':sum(v for v in vs if type(v) is int),'missing_intended':30-sum(type(v) is int for v in vs)}
  subset=[r for r in verified_arms if r['model']==m];di=[d for r in subset for d in r['projection']]
  assert result['reliability'][m]=={'valid':sum(not r['fallback'] for r in subset),'fallbacks':sum(r['fallback'] for r in subset),'intended':30,'projection_records':len(di),'positive_distance':sum(d['hamming_distance']>0 for d in di),'repeated_proposal':sum(d['repeated_proposal'] for d in di),'matches_prefix':sum(d['matches_initial_observation'] for d in di),'joint_over_1pct_vs_sequential_and_adaptive':sum(all(F(r['gains'][c])>F(1,100) for c in refs[:2]) for r in verified_rows if r['model']==m)}
 pair=[]
 for j in jobs:
  q=next(r for r in verified_rows if r['case_key']==j['key'] and r['model']=='qwen3_8b');s=next(r for r in verified_rows if r['case_key']==j['key'] and r['model']=='smollm3_3b');pair.append({'case_key':j['key'],'system_group':j['system_group'],'seed':j['seed'],'qwen':q['target'],'smol':s['target'],'smol_gain':str(gain(q['target'],s['target'],q['direction']))})
 assert result['smol_vs_qwen']['rows']==pair and result['smol_vs_qwen']['total']==stats([F(r['smol_gain']) for r in pair])
 for g in groups:assert result['smol_vs_qwen']['groups'][g]==stats([F(r['smol_gain']) for r in pair if r['system_group']==g])
 assert result['cost']['new_recorded_acquisitions']==600 and result['cost']['evaluation_seconds']==summary['seconds'] and result['cost']['combined_collection_seconds']==summary['combined_collection_seconds']
 assert result['cost']['estimated_deployment']=={'B':20,'prefix':10,'new_evaluations':10,'model_requests':1,'allocated_output_tokens':1024,'loading':'separate cold-start amortization, no dollar or native-time conversion'}
 failed=read('results/v141_models/smollm3_3b/ledger.json');assert failed['generation_requests']==failed['http_requests']==0 and failed['server_exit_code'] is None and result['cost']['failed_startup']==failed and result['cost']['startup_repairs']==1
 assert failed['stage_seconds']+read(modeldirs['smollm3_3b']+'/ledger.json')['stage_seconds']<=800
 assert read('results/v141_models/summary.json')['generation_requests']+read(modeldirs['smollm3_3b']+'/ledger.json')['generation_requests']==totalrequests<=60
 return {'verified':True,'compact':compact,'real_model_requests':totalrequests,'intended_requests':60,'recorded_acquisitions':600,'B20_arms':60,'exposed_groups':6,'models':2,'new_collection':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--compact',action='store_true');a=p.parse_args();print(json.dumps(verify(a.root,a.compact)))
