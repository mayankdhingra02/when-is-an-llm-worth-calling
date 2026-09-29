"""Seal all model selections before acquiring any new recorded outcome."""
import time
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from analyze_pointwise_v123 import candidates
from proposal_v128 import project
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,rank,best
def main():
 for n,h in read(ROOT/'reports/protocol_v142.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 modeldirs=read(ROOT/'artifacts/study_v142/model_paths.json')
 a=ROOT/'artifacts/study_v141';out=ROOT/'results/v141_analysis';out.mkdir(exist_ok=False);choices=[];cfg=read(ROOT/'configs/study_v141.json');start_global=read(ROOT/'results/v141_models/collection_start.json')['at_unix']
 for model in cfg['model_order']:
  for j in read(a/'jobs.json'):
   spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])['state'];path=ROOT/modeldirs[model]/'scores'/f"{j['key']}.json";score=read(path) if path.exists() else {'status':'unattempted'}
   if score['status']=='valid':ids,diags=project(score['score'],c.x,p)
   else:ids,diags=rank(c,State(**p),p['order'])[:10],[]
   r={**j,'case_key':j['key'],'key':model+'_'+j['key'],'model':model,'selected_rows':ids,'projection':diags,'fallback':score['status']!='valid','model_status':score['status']};write(out/'choices'/f"{r['key']}.json",r);choices.append(r)
 paths=list((out/'choices').glob('*.json'))+[ROOT/v/'responses.jsonl' for v in modeldirs.values()];write(out/'selection_seal.json',{'at':now(),'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 t=time.monotonic();count=0;arms=[];error=None
 try:
  for j in choices:
   spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])['state'];s=State(**p).clone();oracle=IndexedOracle(spec,c,p,lambda e:append(out/'acquisitions.jsonl',{'at_unix':time.time(),'key':j['key'],**e}))
   for i in j['selected_rows']:
    if count>=600 or time.monotonic()-t>=180 or time.time()-start_global>=1800:raise RuntimeError('Acquisition/time cap')
    count+=1;s.observe(i,oracle.acquire(i),c.directions)
   refs={}
   for mode,path in {'sequential_3nn':j['classical_arm'],'random_full':f"results/v41_transfer/arms/{j['base_key']}_random_full.json",**{m:f"results/v138_incumbent/arms/{j['case_key']}_{m}.json" for m in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor']}}.items():
    state=read(ROOT/path)['state'];assert state['ids'][:10]==p['ids'] and state['labels'][:10]==p['labels'] and len(set(state['ids']))==20;refs[mode]={'path':path,'target':best(State(**state),spec['direction'])}
   r={**j,'state':s.record(),'direction':spec['direction'],'target':best(s,spec['direction']),'prefix_best':best(State(**p),spec['direction']),'references':refs,'new_accesses':oracle.new_accesses};write(out/'arms'/f"{j['key']}.json",r);arms.append(j['key'])
 except Exception as e:error=repr(e)
 finally:write(out/'summary.json',{'at':now(),'complete':error is None and len(arms)==60 and count==600,'intended_arms':60,'arms':arms,'new_recorded_acquisitions':count,'seconds':time.monotonic()-t,'combined_collection_seconds':time.time()-start_global,'error':error})
 if error:raise RuntimeError(error)
 print('Completed',len(arms),'arms;',count,'charged outcomes')
if __name__=='__main__':main()
