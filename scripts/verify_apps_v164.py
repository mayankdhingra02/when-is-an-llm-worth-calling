"""Independent saved-data replay; performs no native execution or model call."""
import copy,json,random,statistics,hashlib
from pathlib import Path
from verify_apps_v163 import reference_choice,ei_reference,project_reference
from app_validation_v163 import Reference
from proposal_v128 import parse as numeric_parse
from catalog_v164 import make_payload
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v164';O=ROOT/'results/v164_native';M=ROOT/'results/v164_models';BASES=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal'];MODELS=['smollm3_3b','qwen3_8b'];ARMS=BASES+[m+'_'+c for m in MODELS for c in ['numeric','catalog']]
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prompt_check(j,c,p,body):
 examples=[{'settings':c['raw_features'][i],'loss_seconds':y[0]} for i,y in zip(p['ids'],p['labels'])]
 if j['condition']=='numeric':
  assert body['observed_examples']==examples and set(body)=={'feature_order','indexed_values','observed_examples','objective','direction','projection'}
 else:
  assert set(body)=={'feature_order','observed_examples','objective','direction','eligible_candidates_columns','eligible_candidates','duplicate_resolution'}
  assert body['observed_examples']==[{'id':f'{i:02d}',**x} for i,x in zip(p['ids'],examples)]
  assert body['eligible_candidates']==[[f'{i:02d}',*c['raw_features'][i]] for i in range(64) if i not in p['ids']]
  assert body['eligible_candidates_columns']==['id',*c['names']]
def main():
 ref=Reference();freeze=read(A/'freeze.json')
 for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
 cs={e:read(A/'candidates'/f'{e}.json') for e in ['ripgrep','hnswlib']};jobs=read(A/'jobs.json');mjobs=read(A/'model_jobs.json');assert len(jobs)==10 and len(mjobs)==20
 acq=[read(O/'acquisitions'/f'{i:03d}.json') for i in range(1,901)];assert [r['charge'] for r in acq]==list(range(1,901));assert read(O/'ledger.json')['acquisitions']==900 and sum(r['measurement']['native_invocations'] for r in acq)==2700
 def objective(r):
  v=r['measurement'];assert v['engine']==r['engine'] and v['config']==cs[r['engine']]['configs'][r['row_id']] and r['returncode']==0;assert ref.validate(v)==r['value'];assert r['status']==('correct' if v['quality']>=.95 else 'quality_penalty')
 for r in acq:objective(r)
 assert freeze['at_unix']<min(r['at_unix'] for r in acq)
 reuse=read(A/'prefix_reuse.json');assert reuse['outcomes']==100 and reuse['native_invocations']==300 and len(reuse['records'])==100
 historical=[]
 for r in reuse['records']:
  assert sha(ROOT/r['path'])==r['sha256'];h=read(ROOT/r['path']);assert h['phase']=='prefix' and h['charge']==r['historical_charge'];objective(h);historical.append(h)
 checked_gp=0;gaps=[]
 for j in jobs:
  p=read(ROOT/j['prefix']);c=cs[j['engine']];assert p==read(ROOT/j['source_prefix']) and sha(ROOT/j['source_prefix'])==j['source_prefix_sha256'] and sha(ROOT/j['prefix'])==j['prefix_sha256'];order=list(range(64));random.Random(j['seed']).shuffle(order);assert p['order']==order;old=[r for r in historical if r['case']==j['key']];ids=[];ys=[]
  for h in old:
   assert h['row_id']==reference_choice(c,ids,ys,order,'sequential_3nn');ids.append(h['row_id']);ys.append(h['value'])
  assert ids==p['ids'] and [[y] for y in ys]==p['labels']
  for arm in ARMS:
   rec=read(O/'search'/f"{j['key']}__{arm}.json");rows=[r for r in acq if r['case']==j['key'] and r['arm']==arm and r['phase']=='search'];assert len(rows)==7;ids=list(p['ids']);ys=[y[0] for y in p['labels']];props=rec['proposals'];projected=project_reference(c,p,props) if props is not None else None
   if arm=='random_proposal':
    rng=random.Random(164200+j['seed']);assert props==[[rng.randrange(len(d)) for d in c['domains']] for _ in range(10)]
   if props is not None:
    assert len(rec['projection'])==10
    for k,(prop,i,diag) in enumerate(zip(props,projected,rec['projection'])):
     x=[v/(len(d)-1) for v,d in zip(prop,c['domains'])];dist=lambda row:sum(abs(a-b) for a,b in zip(x,c['x'][row]))/len(x)
     assert diag=={'row_id':i,'distance':dist(i),'duplicate_proposal':prop in props[:k],'matches_prefix':any(dist(row)==0 for row in p['ids'])}
   for k,r in enumerate(rows):
    i=r['row_id'];assert i not in ids
    if projected is not None:assert i==projected[k]
    elif arm=='gp_ei':
     ei=ei_reference(c,ids,ys,order);gap=max(ei.values())-ei[i];assert gap<1e-8;gaps.append(gap);checked_gp+=1
    else:assert i==reference_choice(c,ids,ys,order,arm if arm in BASES else 'sequential_3nn')
    ids.append(i);ys.append(r['value'])
   assert rec['state']=={'ids':ids,'labels':[[y] for y in ys],'order':order} and len(set(ids))==17
 selections=read(O/'selections.json');assert len(selections)==90 and sha(O/'selections.json')==read(O/'selection_seal.json')['sha256'];assert read(O/'selection_seal.json')['at_unix']<min(r['at_unix'] for r in acq if r['phase']=='validation')
 for sel in selections:
  f=O/'search'/f"{sel['case']}__{sel['arm']}.json";s=read(f)['state'];best=min(range(17),key=lambda k:s['labels'][k][0]);assert sha(f)==sel['search_sha256'] and sel['row_id']==s['ids'][best] and sel['search_best']==s['labels'][best][0]
 plan=[]
 for block in range(3):
  order=list(range(90));random.Random(164900+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
 vs=lines(O/'validation.jsonl');assert len(vs)==270 and plan==read(O/'validation_plan.json')
 for v,x,r in zip(vs,plan,[r for r in acq if r['phase']=='validation']):assert {k:v[k] for k in x}==x and (v['case'],v['arm'],v['value'],v['row_id'])==(r['case'],r['arm'],r['value'],r['row_id'])
 starts_total=0
 for model in MODELS:
  ledger=read(M/model/'ledger.json');starts=lines(M/model/'generation_starts.jsonl');responses=lines(M/model/'responses.jsonl');starts_total+=len(starts);assert ledger['generation_requests']==len(starts)<=20 and ledger['allocated_output_tokens']<=20480 and ledger['retries']==0 and ledger['external_spend_usd']==0 and ledger['peak_server_rss_bytes']<=8*1024**3 and ledger['server_exit_code']==0
  assert [x['identity'] for x in starts]==[j['request_key'] for j in mjobs][:len(starts)]
  assert all(s['at_unix']>max(r['at_unix'] for r in acq if r['arm'] in BASES and r['phase']=='search') for s in starts)
  for n,h in read(M/model/'preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h
  for j in mjobs:
   p=read(ROOT/j['prefix']);c=cs[j['engine']];pre=read(M/model/'preflight'/f"{j['request_key']}.json");msg=read(ROOT/j['messages_path']);assert pre['messages']==msg;prompt_check(j,c,p,json.loads(msg[1]['content']))
   if j['condition']=='numeric':assert msg==read(ROOT/f"artifacts/study_v163/prompts/{j['key']}.json")
   hits=[r for r in responses if r['key']==j['request_key']]
   if not hits:continue
   assert len(hits)==1;r=hits[0];req=next(s for s in starts if s['identity']==j['request_key']);assert req['payload']==make_payload(pre['rendered']['prompt'],j)
   assert pre['output_capacity']['prompt_tokens']==len(pre['prompt_tokens']) and len(pre['prompt_tokens'])+1024<=4096
   sc=read(M/model/'scores'/f"{j['request_key']}.json");rec=read(O/'search'/f"{j['key']}__{model}_{j['condition']}.json")
   if sc['status']=='valid':
    response=r['response'];assert response['stop_type']=='eos' and response['truncated']is False
    if j['condition']=='numeric':parsed=[list(x) for x in numeric_parse(response,j['domains'])];props=parsed
    else:
     raw=json.loads(response['content']);assert len(raw)==10 and all(type(x)is str and x in {f'{i:02d}' for i in j['eligible']} for x in raw);parsed=[int(x) for x in raw];props=[c['indices'][i] for i in parsed]
    assert sc['score']==parsed and rec['proposals']==props and not rec['fallback']
   else:assert rec['fallback']
 comp=read(O/'comparison.json');arms={(x['case'],x['arm']):x for x in comp['arms']};assert len(arms)==90
 for k,x in arms.items():
  vals=[r['value'] for r in acq if (r['case'],r['arm'])==k and r['phase']=='validation'];med=statistics.median(vals);assert x['values']==vals and x['median']==med and x['mad']==statistics.median(abs(v-med) for v in vals)/med
 def win(b,a):return (b['median']-a['median'])/b['median']>.1 and b['row_id']!=a['row_id'] and all(x['valid'] and x['mad']<=.05 and x['median']>=.01 for x in [a,b])
 for r in comp['contrasts']:
  n=arms[r['case'],r['model']+'_numeric'];c=arms[r['case'],r['model']+'_catalog'];assert r['gain']==(n['median']-c['median'])/n['median'] and r['same_setting']==(n['row_id']==c['row_id']) and r['catalog_robust_win']==win(n,c) and r['catalog_robust_loss']==win(c,n)
 for r in comp['secondary']:
  a=arms[r['case'],r['model']+'_'+r['condition']];assert all(r['gains'][b]==(arms[r['case'],b]['median']-a['median'])/arms[r['case'],b]['median'] for b in BASES);assert r['joint_robust_win']==all(win(arms[r['case'],b],a) for b in BASES[:3])
 for r in comp['summary']:
  rr=[x for x in comp['contrasts'] if x['model']==r['model'] and x['engine']==r['engine']];assert len(rr)==5 and r['mean_catalog_gain']==statistics.mean(x['gain'] for x in rr)
 assert len(comp['contrasts'])==20 and len(comp['secondary'])==40 and len(comp['mechanisms'])==8
 for x in comp['arms']:
  rr=[r for r in acq if r['case']==x['case'] and r['arm']==x['arm'] and r['phase']=='validation'];assert x['valid']==all(r['status']=='correct' for r in rr) and all(r['row_id']==x['row_id'] for r in rr)
 for x in comp['mechanisms']:
  recs=[read(O/'search'/f"{j['key']}__{x['model']}_{x['condition']}.json") for j in jobs if j['engine']==x['engine']];ds=[d for r in recs for d in r['projection'][:7]];al=[d for r in recs for d in r['projection']]
  assert x['observed_evaluated_proposals']==len(ds) and x['evaluated_projected']==sum(d['distance']>0 for d in ds) and x['evaluated_duplicates']==sum(d['duplicate_proposal'] for d in ds)
  assert x['all_proposals']==len(al) and x['all_projected']==sum(d['distance']>0 for d in al) and x['all_duplicates']==sum(d['duplicate_proposal'] for d in al)
 for x in comp['model_costs']:
  rr=[r for r in lines(M/x['model']/'responses.jsonl') if r['key'].endswith('__'+x['condition'])];ss=[r for r in lines(M/x['model']/'generation_starts.jsonl') if r['identity'].endswith('__'+x['condition'])];assert x['responses']==len(rr) and x['starts']==len(ss) and x['request_seconds']==sum(r['wall_seconds'] for r in rr)
  for k in ['tokens_evaluated','tokens_predicted']:assert x['observed_usage'][k]==sum(r['response'].get(k,0) or 0 for r in rr) and x['unknown_usage_responses'][k]==sum(r['response'].get(k)is None for r in rr)
 rejected=[]
 for kind in ['objective','quality','identity']:
  r=copy.deepcopy(acq[0])
  if kind=='objective':r['value']*=2
  elif kind=='quality':r['measurement']['quality']=0.
  else:r['measurement']['engine']='wrong'
  try:objective(r)
  except AssertionError:rejected.append(kind)
  else:raise AssertionError('Mutation accepted')
 j=next(j for j in mjobs if j['condition']=='catalog');body=json.loads(read(ROOT/j['messages_path'])[1]['content']);body['hidden_outcomes']=[1.]
 try:prompt_check(j,cs[j['engine']],read(ROOT/j['prefix']),body)
 except AssertionError:rejected.append('hidden_prompt_field')
 else:raise AssertionError('Prompt leak accepted')
 receipt={'verified':True,'new_configuration_outcomes':900,'new_native_invocations':2700,'historical_prefixes_reused':10,'historical_prefix_outcomes':100,'B20_arms':90,'fresh_validations':270,'model_starts':starts_total,'independent_GP_choices':checked_gp,'max_EI_gap':max(gaps),'mutations_rejected':rejected,'scope':'Independent numerical/raw-data replay in same repository; not external replication'};(A/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
