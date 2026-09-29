"""Seal full-domain choices before separately charged paired evaluation."""
import json,time,statistics
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from analyze_pointwise_v123 import candidates
from proposal_v127 import parse,project,random_proposals
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,rank,best,relative_gain
OUT=ROOT/'results/v127_analysis'

def frozen():
 for path in ['reports/protocol_v127.freeze.json','artifacts/study_v127/inputs.freeze.json']:
  for n,h in read(ROOT/path)['sha256'].items():assert sha(ROOT/n)==h,n

def choose():
 jobs=read(ROOT/'artifacts/study_v127/jobs.json');jm={j['key']:j for j in jobs};raw=[json.loads(x) for x in (ROOT/'results/v127_proposals/responses.jsonl').read_text().splitlines()];assert len({r['key'] for r in raw})==len(raw);rm={r['key']:r for r in raw};selections={};diagnostics=[];choices=[]
 for j in jobs:
  p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);r=rm.get(j['key']);error=None;rows=None;projection=[]
  try:
   if r is None:raise ValueError('No returned response')
   proposals=parse(r['response'],j['domains']);rows,projection=project(proposals,c.x,p['state'])
  except ValueError as e:error=str(e)
  selections[j['key']]=rows;diagnostics.append({'key':j['key'],'condition':j['condition'],'status':'valid' if error is None else 'missing' if r is None else 'invalid','error':error,'selected_rows':rows,'projection':projection})
  if j['condition']=='normal':
   batch=rank(c,State(**p['state']).clone(),p['state']['order'])[:10];random_rows,random_d=project(random_proposals(j['domains'],j['random_proposal_seed']),c.x,p['state'])
   for mode,selected,detail in [('model',rows if rows is not None else batch,projection),('random_projection',random_rows,random_d),('full_batch_3nn',batch,[])]:
    choices.append({**j,'request_key':j['key'],'key':j['base_key']+'_'+mode,'mode':mode,'selected_rows':selected,'projection':detail,'fallback':mode=='model' and rows is None,'prefix_sha256':sha(ROOT/j['prefix'])})
 probes=[]
 for j in jobs:
  if j['condition']=='rotated_labels':
   a=selections[j['base_key']+'_normal'];b=selections[j['key']];probes.append({'key':j['base_key'],'both_valid':a is not None and b is not None,'selection_set_overlap':None if a is None or b is None else len(set(a)&set(b)),'same_order':None if a is None or b is None else a==b})
 return choices,{'intended_requests':36,'responses':len(raw),'requests':diagnostics,'label_rotation_probes':probes,'scope':'Rotation diagnostics acquire no extra outcomes and are not optimization arms'}

def references(j,p,direction):
 refs={}
 paths={**{m:f"results/v41_transfer/arms/{j['base_key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full']},'presentation_first10':f"results/v41_models/0.5/arms/{j['base_key']}.json",'single_portfolio':f"results/v115_portfolio/arms/{j['base_key']}.json"}
 for m,n in paths.items():
  if not (ROOT/n).exists():assert m=='single_portfolio';continue
  s=read(ROOT/n)['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(s['ids'])==len(set(s['ids']))==20
  if m=='presentation_first10':assert s['ids'][10:]==[p['pool']['mapping'][i] for i in '0123456789']
  refs[m]=best(State(**s),direction)
 return refs

def evaluate():
 frozen();OUT.mkdir(exist_ok=False);choices,d=choose();assert len(choices)==90;write(OUT/'diagnostics.json',d)
 for c in choices:write(OUT/'choices'/f"{c['key']}.json",c)
 write(OUT/'selection_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'results/v127_proposals/responses.jsonl',OUT/'diagnostics.json']+sorted((OUT/'choices').glob('*.json'))}})
 start=time.monotonic();count=0;arms=[];error=None
 try:
  for j in choices:
   p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'key':j['key'],**e}))
   for i in j['selected_rows']:
    if count>=900 or time.monotonic()-start>=180:raise RuntimeError('Evaluation stage limit')
    count+=1;state.observe(i,oracle.acquire(i),c.directions)
   refs=references(j,p,spec['direction']);target=best(state,spec['direction']);r={**j,'state':state.record(),'direction':spec['direction'],'target':target,'references':refs,'gains':{m:relative_gain(v,target,spec['direction']) for m,v in refs.items()}};write(OUT/'arms'/f"{r['key']}.json",r);arms.append(r)
 except Exception as e:error=repr(e)
 finally:write(OUT/'summary.json',{'complete':error is None and len(arms)==90,'error':error,'intended_arms':90,'actual_new_acquisitions':count,'stage_seconds':time.monotonic()-start,'arms':arms})
 if error:raise RuntimeError(error)
 print('Acquired900recorded outcomes across90B20arms')

def report():
 frozen();s=read(OUT/'summary.json');assert s['complete'];arms=s['arms'];am={a['key']:a for a in arms};d=read(OUT/'diagnostics.json');ledger=read(ROOT/'results/v127_proposals/ledger.json');raw=[json.loads(x) for x in (ROOT/'results/v127_proposals/responses.jsonl').read_text().splitlines()];rows=[]
 for a in arms:
  if a['mode']!='model':continue
  refs={**a['references'],**{m:am[a['base_key']+'_'+m]['target'] for m in ['random_projection','full_batch_3nn']}};rows.append({'key':a['base_key'],'dataset':a['dataset'],'system_group':a['system_group'],'seed':a['seed'],'target':a['target'],'fallback':a['fallback'],'references':refs,'gains':{m:relative_gain(v,a['target'],a['direction']) for m,v in refs.items()},'outside_old_shortlist':len(set(a['selected_rows'])-set(read(ROOT/a['prefix'])['pool']['mapping'].values()))})
 modes=sorted({m for r in rows for m in r['gains']});families=[];groups=sorted({r['system_group'] for r in rows});contrasts={}
 for g in groups:
  rs=[r for r in rows if r['system_group']==g];families.append({'system_group':g,'cases':len(rs),'means':{m:statistics.mean(r['gains'][m] for r in rs if m in r['gains']) for m in modes if any(m in r['gains'] for r in rs)}})
 for m in modes:
  rs=[r for r in rows if m in r['gains']];contrasts[m]={'cases':len(rs),'equal_family_mean':statistics.mean(f['means'][m] for f in families if m in f['means']),'wins':sum(r['gains'][m]>1e-12 for r in rs),'ties':sum(abs(r['gains'][m])<=1e-12 for r in rs),'losses':sum(r['gains'][m]<-1e-12 for r in rs)}
 primary=['full_sequential_3nn','random_projection','full_batch_3nn'];joint=sum(all(r['gains'][m]>=.05 for m in primary) for r in rows);valid=sum(r['condition']=='normal' and r['status']=='valid' for r in d['requests']);positive_families=sum(f['means']['full_sequential_3nn']>0 for f in families)
 gate=valid==30 and all(contrasts[m]['equal_family_mean']>0 for m in primary) and positive_families>=2 and joint>=1
 usage={}
 for field in ['tokens_predicted','tokens_evaluated']:
  vals=[r['response'].get(field) for r in raw];usage[field]={'observed_sum':sum(v for v in vals if type(v) is int),'missing_responses':len(vals)-sum(type(v) is int for v in vals)}
 model_diags=[x for x in d['requests'] if x['condition']=='normal'];projection=[p for x in model_diags for p in x['projection']]
 result={'scope':'Full-domain proposal exploratory development,not held-out routing or a source-method replication','cases':rows,'families':families,'contrasts':contrasts,'joint_5pct_cases':joint,'normal_valid':valid,'positive_families_vs_sequential':positive_families,'development_screen_met':gate,'projection':{'proposals_with_diagnostics':len(projection),'nonzero_projection_distance':sum(p['hamming_distance']>0 for p in projection),'repeated_proposals':sum(p['repeated_proposal'] for p in projection),'matches_observed':sum(p['matches_initial_observation'] for p in projection),'selected_outside_old_pool':sum(r['outside_old_shortlist'] for r in rows)},'actual_cost':{'ledger':ledger,'usage':usage,'new_recorded_acquisitions':s['actual_new_acquisitions'],'historical_prefixes_reused':30,'scope':'Research collection of3paired arms,not deployment budget'},'label_rotation_probes':d['label_rotation_probes'],'estimated_deployment':{'requests_per_escalation':1,'max_allocated_output_tokens':512,'objective_evaluations':20,'new_objective_evaluations':10,'scope':'Projection overhead and per-run startup/objective time not measured as end-to-end deployment'}};write(OUT/'comparison.json',result)
 lines=['# V127: full-domain feature proposals, exposed development','','Qwen3-8B proposes ten feature-setting strings from ten acquired examples and feature domains. Feature-only nearest-Hamming projection chooses valid unobserved configurations with frozen-order ties, sequentially excluding projected rows. No old shortlist or candidate IDs enter the model prompt. Matched random feature proposals use the identical projection. A new full-domain batch3NN arm and historical sequential/other controls share the same saved prefix. This is a constrained batch adaptation, not a complete SNAP2/LLAMBO reproduction.','','| Comparator | Cases | Equal-family mean gain | Wins/ties/losses |','|---|---:|---:|---|']
 for m,v in contrasts.items():lines.append(f"| {m} | {v['cases']} | {v['equal_family_mean']*100:.3f}% | {v['wins']}/{v['ties']}/{v['losses']} |")
 lines+=['',f"Normal valid responses: {valid}/30; six extra label-rotation probes retain their own validity status and acquire no new outcomes. Joint≥5%cases against sequential, random projection and full batch3NN: {joint}/30. Positive family means versus sequential: {positive_families}/6. Predeclared exploratory development screen met: {gate}. Even passing would not establish generalization, novelty or journal readiness.",'','| Family | Gain vs sequential3NN | Gain vs random projection | Gain vs full batch3NN |','|---|---:|---:|---:|']
 for f in families:lines.append(f"| {f['system_group']} | {100*f['means']['full_sequential_3nn']:.3f}% | {100*f['means']['random_projection']:.3f}% | {100*f['means']['full_batch_3nn']:.3f}% |")
 lines+=['',f"Projection audit: {len(projection)}decoded proposals, {result['projection']['nonzero_projection_distance']}with nonzero distance, {result['projection']['repeated_proposals']}repeated proposals, {result['projection']['matches_observed']}matching acquired configurations. Actual model-arm selections outside the old shortlist: {result['projection']['selected_outside_old_pool']}/300 (includes declared fallback selections where any occur). Projection/duplicate behavior is preserved, not repaired by free model retries.",'',f"Actual cost: {ledger['generation_requests']}new real generation attempts, {len(raw)}returned; {usage['tokens_predicted']['observed_sum']}observed generated tokens with {usage['tokens_predicted']['missing_responses']}missing receipts; {ledger['allocated_output_tokens']}allocated. Lifecycle {ledger['stage_seconds']:.3f}s, peak sampled serverRSS {ledger['peak_server_rss_bytes']:,}bytes.900new recorded accesses across90pairedB20arms; all intended arms retained. Prefix/control costs remain historical. No retries, downloads, paid/cloud inference or new native execution.",'','Estimated deployment uses one model request (≤512output tokens) and ten new objective evaluations per escalation, plus projection/startup costs. The six rotation requests and extra paired research arms are collection overhead; they are not free deployment. No dollar or native-runtime savings are inferred. Missing usage is unknown, not zero.','','All six families and all five seeds were retained, but are extensively exposed development data; seeds are grouped by family. V126hindsight maps and ranks never enter model/projection/baseline inputs. Prior wider-domain bounds motivated this intervention without selecting only favorable cases. Repeated proposals, projection constraints and tie-order can produce apparent gains without meaningful learned optimization; the matched cheap controls address that possibility in this assay. Rotation differences diagnose dependence on label assignment, not correctness or held-out benefit. No controller was fitted or held-out threshold tuned. Original correctness/equal-utility/noise and redistribution qualifications remain.','','Source: existing owner model/runtime and V41data manifests; artifacts/study_v127freezes; results/v127_proposalsrawrequests; results/v127_analysischoices,chargedjournals,andcomparisons.']
 (ROOT/'reports/proposals_v127.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'contrasts':contrasts,'normal_valid':valid,'joint_5pct_cases':joint,'development_screen_met':gate},indent=2))
if __name__=='__main__':report() if '--report' in __import__('sys').argv else evaluate()
