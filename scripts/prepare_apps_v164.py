"""Prepare/freeze the complete intervention before any new application/model call."""
import copy,json,random,time
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,sha
from catalog_v164 import messages

def main():
 a=ROOT/'artifacts/study_v164';old=ROOT/'artifacts/study_v163';assert not (a/'freeze.json').exists();assert sha(old/'evidence_manifest.json')=='2cdc943e0440d63dd7e093a55c37b865d4cac30470e65333a4681839182ed017'
 jobs=[];model_jobs=[];reuse=[]
 write(a/'models.json',read(old/'models.json'))
 for e in ['ripgrep','hnswlib']:write(a/'candidates'/f'{e}.json',read(old/'candidates'/f'{e}.json'))
 for j0 in read(old/'jobs.json'):
  j=copy.deepcopy(j0);s=read(ROOT/j['prefix']);c=read(a/'candidates'/f"{j['engine']}.json");j['source_prefix']=j['prefix'];j['source_prefix_sha256']=sha(ROOT/j['prefix']);j['prefix']=f"artifacts/study_v164/prefixes/{j['key']}.json";write(ROOT/j['prefix'],s);j['prefix_sha256']=sha(ROOT/j['prefix']);j['sampling_seed']=164000+j['seed'];j.pop('messages_path');jobs.append(j)
  for cond in ['numeric','catalog']:
   k={**j,'condition':cond,'request_key':j['key']+'__'+cond,'eligible':[i for i in range(64) if i not in s['ids']],'messages_path':f"artifacts/study_v164/prompts/{j['key']}__{cond}.json"};msg=messages(j['engine'],c,s,cond)
   if cond=='numeric':assert msg==read(ROOT/j0['messages_path'])
   write(ROOT/k['messages_path'],msg);model_jobs.append(k)
 for p in sorted((ROOT/'results/v163_native/acquisitions').glob('*.json')):
  x=read(p)
  if x['phase']=='prefix':reuse.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'case':x['case'],'row_id':x['row_id'],'historical_charge':x['charge'],'native_invocations':x['measurement']['native_invocations']})
 assert len(reuse)==100 and sum(x['native_invocations'] for x in reuse)==300
 random.Random(164).shuffle(model_jobs);write(a/'jobs.json',jobs);write(a/'model_jobs.json',model_jobs);write(a/'prefix_reuse.json',{'outcomes':100,'native_invocations':300,'not_new_collection':True,'records':reuse})
 used={**read(old/'freeze.json')['sha256'],**read(old/'inputs.freeze.json')['sha256']}
 for n,h in used.items():assert sha(ROOT/n)==h,n
 for p in list((a/'prefixes').glob('*.json'))+list((a/'prompts').glob('*.json'))+list((a/'candidates').glob('*.json'))+[a/x for x in ['jobs.json','model_jobs.json','models.json','prefix_reuse.json']]:used[str(p.relative_to(ROOT))]=sha(p)
 for n in ['reports/protocol_v164.md','configs/study_v164.json','scripts/catalog_v164.py','scripts/runtime_models_v164.py','scripts/native_apps_v164.py','scripts/collect_models_v164.py','scripts/run_apps_v164.py','scripts/prepare_apps_v164.py','tests/synthetic/test_catalog_v164.py']:used[n]=sha(ROOT/n)
 for x in reuse:used[x['path']]=x['sha256']
 write(a/'freeze.json',{'at_unix':time.time(),'scope':'Development interface intervention on existing exposed cases; all new collection follows this freeze','sha256':used});print('Frozen10prefixes/20interfacejobs/40modelstarts/900newoutcomecap')
if __name__=='__main__':main()
