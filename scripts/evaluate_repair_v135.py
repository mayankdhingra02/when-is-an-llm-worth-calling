"""Freeze feature-only model selections, then acquire exactly50 recorded labels."""
import time
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from analyze_pointwise_v123 import candidates
from analyze_proposal_v127 import references
from proposal_v128 import project
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,rank,best,relative_gain

def main():
 for n,h in read(ROOT/'reports/protocol_v135.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 a=ROOT/'artifacts/study_v135';out=ROOT/'results/v135_analysis';out.mkdir(exist_ok=False);choices=[]
 for j in read(a/'jobs.json'):
  spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);path=ROOT/f'results/v135_proposals/scores/{j["key"]}.json';score=read(path) if path.exists() else {'status':'unattempted'}
  if score['status']=='valid':ids,diags=project(score['score'],c.x,p['state'])
  else:ids,diags=rank(c,State(**p['state']),p['state']['order'])[:10],[]
  r={**j,'selected_rows':ids,'projection':diags,'fallback':score['status']!='valid','model_status':score['status']};write(out/'choices'/f"{j['key']}.json",r);choices.append(r)
 paths=list((out/'choices').glob('*.json'))+[ROOT/'results/v135_proposals/responses.jsonl'];write(out/'selection_seal.json',{'at':now(),'scope':'All choices before any new outcome','sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 start=time.monotonic();count=0;arms=[];error=None
 try:
  for j in choices:
   spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(out/'acquisitions.jsonl',{'at':now(),'key':j['key'],**e}))
   for row in j['selected_rows']:
    if count>=50 or time.monotonic()-start>=180:raise RuntimeError('Repair acquisition cap')
    count+=1;state.observe(row,oracle.acquire(row),c.directions)
   refs=references(j,p,spec['direction']);old=read(ROOT/f"results/v127_analysis/arms/{j['base_key']}_model.json");target=best(state,spec['direction']);r={**j,'state':state.record(),'direction':spec['direction'],'target':target,'prefix_best':best(State(**p['state']),spec['direction']),'references':refs,'gains':{m:relative_gain(v,target,spec['direction']) for m,v in refs.items()},'old_failed_contract_target':old['target'],'old_fallback':old['fallback']};write(out/'arms'/f"{j['key']}.json",r);arms.append(r)
 except Exception as e:error=repr(e)
 finally:write(out/'summary.json',{'complete':error is None and len(arms)==5,'intended_arms':5,'new_recorded_acquisitions':count,'evaluation_seconds':time.monotonic()-start,'error':error,'arms':arms})
 if error:raise RuntimeError(error)
if __name__=='__main__':main()
