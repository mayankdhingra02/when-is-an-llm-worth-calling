"""Bounded fresh numeric/catalog model calls on the same saved prefixes."""
import time
from runtime_models_v164 import ROOT,Runtime
from collect_smollm_v47 import read,write,append,sha,now
from catalog_v164 import make_payload,parse,authorize
from audit_output_capacity_v127 import vocab

def main():
 cfg=read(ROOT/'configs/study_v164.json');a=ROOT/'artifacts/study_v164';out=ROOT/'results/v164_models'
 assert cfg['total_request_cap']==40 and cfg['new_generation_request_cap']==20 and cfg['max_allocated_output_tokens']==20480
 for n,h in read(a/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 from native_apps_v164 import classical_gate
 classical_gate();out.mkdir(exist_ok=False);t=time.monotonic();global_start=read(ROOT/'results/v164_native/ledger.json')['start_unix'];write(out/'collection_start.json',{'at':now(),'at_unix':time.time(),'total_seconds_cap':1800});jobs=read(a/'model_jobs.json');models=read(a/'models.json')
 for key in cfg['model_order']:
  if time.time()-global_start>1000:raise TimeoutError('Global reserve')
  sub=out/key;sub.mkdir();(sub/'responses.jsonl').touch();model=models[key];assert sha(ROOT/model['path'])==model['sha256'];tokens=vocab(ROOT/model['path']);rt=Runtime(sub,{**cfg,'model_key':key})
  try:
   rt.start();prepared=[]
   for j in jobs:
    msgs=read(ROOT/j['messages_path']);rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}});ids=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens'];p=make_payload(rendered['prompt'],j)
    proof=authorize(rt,p,j,tokens,len(ids));write(sub/'preflight'/f"{j['request_key']}.json",{**j,'messages':msgs,'rendered':rendered,'prompt_tokens':ids,'output_capacity':proof});prepared.append((j,p))
   write(sub/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((sub/'preflight').glob('*.json'))}})
   for j,p in prepared:
    start=time.monotonic();response=rt.generate(p,'scientific',j['request_key']);append(sub/'responses.jsonl',{'key':j['request_key'],'at':now(),'response':response,'wall_seconds':time.monotonic()-start})
    try:score=parse(response,j);status='valid';error=None
    except ValueError as e:score=None;status='invalid';error=str(e)
    write(sub/'scores'/f"{j['request_key']}.json",{**j,'model':key,'score':score,'status':status,'error':error});print(key,j['request_key'],status,flush=True)
  except Exception as e:rt.ledger['stop_reason']=repr(e);append(sub/'errors.jsonl',{'at':now(),'error':repr(e)})
  finally:rt.close()
 write(out/'summary.json',{'at':now(),'seconds':time.monotonic()-t,'intended_requests':40,'models':cfg['model_order'],'generation_requests':sum(read(out/k/'ledger.json')['generation_requests'] for k in cfg['model_order'])})
if __name__=='__main__':main()
