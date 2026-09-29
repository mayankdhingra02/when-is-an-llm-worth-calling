"""Prospectively frozen, zero-inference classical control extension."""
import sys,time
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from analyze_pointwise_v123 import candidates,State,IndexedOracle
from incumbent_v138 import choose
ART=ROOT/'artifacts/study_v138';OUT=ROOT/'results/v138_incumbent';MODES=['fixed_prefix_neighbor','adaptive_incumbent_neighbor']
def prepare():
 ART.mkdir(exist_ok=False);jobs=sorted([j for j in read(ROOT/'artifacts/study_v127/jobs.json') if j['condition']=='normal'],key=lambda j:(j['system_group'],j['seed']))
 assert len(jobs)==30 and len({j['system_group'] for j in jobs})==6
 for j in jobs:
  spec,c=candidates(j['dataset']);assert sha(ROOT/j['prefix'])==j['prefix_sha256'];write(ART/'candidates'/f"{j['system_group']}.json",{'names':c.names,'x':c.x,'source_ids':c.source_ids,'directions':c.directions,'spec':spec})
  j['model_arm']=f"results/v135_analysis/arms/{j['base_key']}_normal.json" if j['system_group']=='sac' else f"results/v127_analysis/arms/{j['base_key']}_model.json"
  j['classical_arm']=f"results/v41_transfer/arms/{j['base_key']}_full_sequential_3nn.json"
  p=read(ROOT/j['prefix'])['state']
  for name in ['model_arm','classical_arm']:
   s=read(ROOT/j[name])['state'];assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels'] and len(set(s['ids']))==20
 write(ART/'jobs.json',jobs)
def collect():
 cfg=read(ROOT/'configs/study_v138.json');assert cfg['new_model_requests']==0 and cfg['max_new_acquisitions']==600 and cfg['max_seconds']==180
 for n,h in read(ROOT/'reports/protocol_v138.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 OUT.mkdir(exist_ok=False);t=time.monotonic();count=0;arms=[];error=None
 try:
  for j in read(ART/'jobs.json'):
   spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])['state']
   for mode in MODES:
    s=State(**p).clone();key=f"{j['key']}_{mode}";oracle=IndexedOracle(spec,c,p,lambda e:append(OUT/'acquisitions.jsonl',{'key':key,'at_unix':time.time(),**e}))
    for step in range(10):
     if count>=600 or time.monotonic()-t>=180:raise RuntimeError('Collection limit')
     selected=choose(c.x,p,s.record(),spec['direction'],mode);path=OUT/'selections'/f'{key}_{step}.json';write(path,{'key':key,'step':step,'before':s.record(),'selected':selected,'at_unix':time.time()})
     count+=1;s.observe(selected['row_id'],oracle.acquire(selected['row_id']),c.directions)
    record={'key':key,'case_key':j['key'],'mode':mode,'state':s.record(),'new_acquisitions':oracle.new_accesses};write(OUT/'arms'/f'{key}.json',record);arms.append(key)
 except Exception as e:error=repr(e)
 finally:write(OUT/'summary.json',{'at':now(),'complete':error is None and len(arms)==60 and count==600,'error':error,'completed_arms':arms,'intended_arms':60,'new_acquisitions':count,'new_model_requests':0,'seconds':time.monotonic()-t})
 if error:raise RuntimeError(error)
 print('Collected',count,'recorded outcomes;',len(arms),'B20 arms; zero model requests')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--collect' in sys.argv:collect()
 else:raise SystemExit('Choose --prepare or --collect; both are create-once')
