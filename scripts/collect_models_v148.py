"""Real inference with a checked classical gate; never acquires hidden outcomes."""
import time
from runtime_models_v148 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,sha,now
from proposal_v128 import payload,parse,MAX_OUTPUT
from audit_output_capacity_v127 import vocab
def main():
 cfg=read(ROOT/'configs/study_v148.json');a=ROOT/'artifacts/study_v148';out=ROOT/'results/v148_models'
 assert cfg['total_request_cap']==30 and cfg['total_models']==2 and cfg['new_generation_request_cap']==15 and cfg['max_allocated_output_tokens']==15360
 for name in ['reports/protocol_v148.freeze.json','artifacts/study_v148/inputs.freeze.json']:
  for n,h in read(ROOT/name)['sha256'].items():assert sha(ROOT/n)==h,n
 from hadoop_v148 import classical_gate
 classical_gate();out.mkdir(exist_ok=False);t=time.monotonic();global_start=read(ROOT/'results/v148_hadoop/ledger.json')['collection_started_unix'];write(out/'collection_start.json',{'at':now(),'at_unix':time.time(),'total_seconds_cap':1800});jobs=read(a/'jobs.json');models=read(a/'models.json')
 for key in cfg['model_order']:
  if time.time()-global_start>1100:raise TimeoutError('Insufficient global reserve for second model block')
  active_jobs=jobs;sub=out/key;sub.mkdir();(sub/'responses.jsonl').touch();model=models[key];assert sha(ROOT/model['path'])==model['sha256'];vocabulary=vocab(ROOT/model['path']);rt=Runtime(sub,{**cfg,'model_key':key})
  try:
   rt.start();prepared=[]
   for j in active_jobs:
    msgs=read(ROOT/j['messages_path']);rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}});tokens=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
    proof=rt.authorize(payload(rendered['prompt'],j['sampling_seed'],j['domains']),j['domains'],vocabulary,len(tokens));write(sub/'preflight'/f"{j['key']}.json",{**j,'messages':msgs,'rendered':rendered,'prompt_tokens':tokens,'output_capacity':proof});prepared.append((j,rendered['prompt']))
   write(sub/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((sub/'preflight').glob('*.json'))}})
   for j,prompt in prepared:
    start=time.monotonic()
    response=rt.generate(payload(prompt,j['sampling_seed'],j['domains']),'scientific',j['key']);append(sub/'responses.jsonl',{'key':j['key'],'at':now(),'response':response,'wall_seconds':time.monotonic()-start})
    try:score=parse(response,j['domains']);status='valid';error=None
    except ValueError as e:score=None;status='invalid';error=str(e)
    write(sub/'scores'/f"{j['key']}.json",{**j,'model':key,'score':score,'status':status,'error':error});print(key,j['key'],status,flush=True)
  except Exception as e:rt.ledger['stop_reason']=repr(e);append(sub/'errors.jsonl',{'at':now(),'error':repr(e)})
  finally:rt.close()
 write(out/'summary.json',{'at':now(),'seconds':time.monotonic()-t,'intended_requests':30,'models':cfg['model_order'],'generation_requests':sum(read(out/k/'ledger.json')['generation_requests'] for k in cfg['model_order'])})
if __name__=='__main__':main()
