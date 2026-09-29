"""Seal full-domain choices before separately charged paired evaluation."""
import json,time,statistics
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from prepare_proposal_v128 import candidates
from proposal_v128 import parse,project,random_proposals
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,rank,best,relative_gain
OUT=ROOT/'results/v129_analysis'

def frozen():
 for path in ['reports/protocol_v129.freeze.json','artifacts/study_v128/inputs.freeze.json']:
  for n,h in read(ROOT/path)['sha256'].items():assert sha(ROOT/n)==h,n

def choose():
 jobs=read(ROOT/'artifacts/study_v128/jobs.json');jm={j['key']:j for j in jobs};raw=[json.loads(x) for x in (ROOT/'results/v129_merged/responses.jsonl').read_text().splitlines()];assert len({r['key'] for r in raw})==len(raw);rm={r['key']:r for r in raw};selections={};diagnostics=[];choices=[]
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
 return choices,{'intended_requests':12,'responses':len(raw),'requests':diagnostics,'label_rotation_probes':probes,'scope':'Rotation diagnostics acquire no extra outcomes and are not optimization arms'}

def references(j,p,direction):
 refs={}
 version=j['classical_version']
 paths={m:f"results/v{version}_classical/arms/{j['base_key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full','single_portfolio']}
 paths['presentation_first10']=(f"results/v120_analysis/arms/{j['base_key']}.json" if version==119 else f"results/v121_classical/arms/{j['base_key']}_presentation_first10.json")
 for m,n in paths.items():
  s=read(ROOT/n)['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(s['ids'])==len(set(s['ids']))==20
  if m=='presentation_first10':assert s['ids'][10:]==[p['pool']['mapping'][i] for i in '0123456789']
  refs[m]=best(State(**s),direction)
 return refs

def evaluate():
 frozen();OUT.mkdir(exist_ok=False);choices,d=choose();assert len(choices)==30;write(OUT/'diagnostics.json',d)
 for c in choices:write(OUT/'choices'/f"{c['key']}.json",c)
 write(OUT/'selection_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'results/v129_merged/responses.jsonl',OUT/'diagnostics.json']+sorted((OUT/'choices').glob('*.json'))}})
 start=time.monotonic();count=0;arms=[];error=None
 try:
  for j in choices:
   p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);state=State(**p['state']).clone()
   if j['mode']!='model' or j['base_key']=='mongodb_twins_11':
    original=ROOT/'results/v128_analysis/arms'/f"{j['key']}.json";old=read(original)
    assert old['selected_rows']==j['selected_rows'] and old['prefix_sha256']==j['prefix_sha256'] and old['state']['ids'][:10]==p['state']['ids'] and old['state']['labels'][:10]==p['state']['labels']
    r={**old,**j,'reuse_source':str(original.relative_to(ROOT)),'reuse_sha256':sha(original),'new_accesses_this_stage':0};write(OUT/'arms'/f"{r['key']}.json",r);arms.append(r);continue
   oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'key':j['key'],**e}))
   for i in j['selected_rows']:
    if count>=90 or time.monotonic()-start>=180:raise RuntimeError('Evaluation stage limit')
    count+=1;state.observe(i,oracle.acquire(i),c.directions)
   refs=references(j,p,spec['direction']);target=best(state,spec['direction']);r={**j,'state':state.record(),'direction':spec['direction'],'target':target,'references':refs,'gains':{m:relative_gain(v,target,spec['direction']) for m,v in refs.items()}};write(OUT/'arms'/f"{r['key']}.json",r);arms.append(r)
 except Exception as e:error=repr(e)
 finally:write(OUT/'summary.json',{'complete':error is None and len(arms)==30,'error':error,'intended_arms':30,'actual_new_acquisitions':count,'combined_new_experimental_acquisitions':300+count,'reused_arms':sum('reuse_source' in a for a in arms),'stage_seconds':time.monotonic()-start,'arms':arms})
 if error:raise RuntimeError(error)
 print('Recovery evaluated with21exact-input arm reuses and90newacquisitions')

if __name__=='__main__':evaluate()
