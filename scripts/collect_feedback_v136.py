"""Bounded real local feedback experiment. Selection is saved before acquisition."""
import time
from runtime_feedback_v136 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,sha,now
from analyze_pointwise_v123 import candidates,State,IndexedOracle,rank
from feedback_v136 import messages,payload,parse,project
from audit_output_capacity_v127 import vocab
def main():
 cfg=read(ROOT/'configs/study_v136.json')
 assert cfg['new_generation_request_cap']==100 and cfg['max_recorded_acquisitions']==200
 for n,h in read(ROOT/'reports/protocol_v136.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 model=read(ROOT/'artifacts/study_v91/model_manifest.json');assert sha(ROOT/model['path'])==model['sha256'];vocabulary=vocab(ROOT/model['path']);rss(-1)
 out=ROOT/'results/v136_feedback';out.mkdir(exist_ok=False);(out/'responses.jsonl').touch();start=time.monotonic();rt=Runtime(out,cfg);count=0;stop=None;error=None;completed=[]
 try:
  try:rt.start()
  except Exception as e:stop=repr(e)
  for job in read(ROOT/'artifacts/study_v136/jobs.json'):
   spec,c=candidates(job['dataset']);prefix=read(ROOT/job['prefix'])['state'];states={m:State(**prefix).clone() for m in ['feedback','masked']}
   oracles={m:IndexedOracle(spec,c,prefix,lambda e,m=m:append(out/'acquisitions.jsonl',{'key':job['key'],'arm':m,'at_unix':time.time(),**e})) for m in states}
   for step in job['schedule']:
    for mode in step['arm_order']:
     if time.monotonic()-start>cfg['max_total_stage_seconds']-5:raise TimeoutError('Total stage cap')
     state=states[mode];identity=f"{job['key']}_{mode}_{step['round']}";before=state.record();msgs=messages(c.names,c.x,prefix,before,spec['meaning'],spec['direction'],mode)
     base={'identity':identity,'key':job['key'],'arm':mode,'round':step['round'],'sampling_seed':step['sampling_seed'],'before':before,'messages':msgs,'at_unix':time.time()};write(out/'decisions'/f'{identity}.json',base)
     invalid=stop;response=None;diag=[];request_seconds=None
     if stop is None:
      try:
       rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
       tokens=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens'];p=payload(rendered['prompt'],step['sampling_seed'],job['domains']);proof=rt.authorize(p,job['domains'],vocabulary,len(tokens))
       write(out/'preflight'/f'{identity}.json',{'rendered':rendered,'prompt_tokens':tokens,'payload':p,'capacity':proof,'decision_sha256':sha(out/'decisions'/f'{identity}.json'),'at_unix':time.time()})
       t=time.monotonic();response=rt.generate(p,'scientific',identity);request_seconds=time.monotonic()-t;append(out/'responses.jsonl',{'identity':identity,'at_unix':time.time(),'wall_seconds':request_seconds,'response':response})
      except Exception as e:
       stop=repr(e);invalid=stop;append(out/'errors.jsonl',{'identity':identity,'error':stop,'at_unix':time.time()})
     if response is not None:
      try:proposals=parse(response,job['domains']);rows,diag=project(proposals,c.x,before)
      except ValueError as e:invalid=repr(e)
     if invalid is not None:rows=rank(c,state,range(len(c.x)))[:2]
     selection={'identity':identity,'rows':rows,'diagnostics':diag,'fallback':invalid is not None,'reason':invalid,'decision_sha256':sha(out/'decisions'/f'{identity}.json'),'at_unix':time.time()};write(out/'selections'/f'{identity}.json',selection)
     t=time.monotonic()
     for row in rows:
      if count>=200 or time.monotonic()-start>cfg['max_total_stage_seconds']-5:raise RuntimeError('Acquisition cap')
      count+=1;state.observe(row,oracles[mode].acquire(row),c.directions)
     write(out/'rounds'/f'{identity}.json',{'identity':identity,'state':state.record(),'evaluation_seconds':time.monotonic()-t,'selection_sha256':sha(out/'selections'/f'{identity}.json'),'at_unix':time.time()})
     print(identity,'fallback' if invalid else 'valid','acquisitions',count,flush=True)
   for mode,state in states.items():
    write(out/'arms'/f"{job['key']}_{mode}.json",{'key':job['key'],'arm':mode,'state':state.record(),'new_acquisitions':oracles[mode].new_accesses});completed.append([job['key'],mode])
 except Exception as e:error=repr(e)
 finally:
  rt.close();write(out/'summary.json',{'at':now(),'complete':len(completed)==20 and count==200 and error is None,'completed_arms':completed,'intended_arms':20,'intended_requests':100,'new_acquisitions':count,'generation_stop_reason':stop,'error':error,'total_seconds':time.monotonic()-start})
 if error:raise RuntimeError(error)
if __name__=='__main__':main()
