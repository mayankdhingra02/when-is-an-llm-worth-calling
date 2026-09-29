"""Conditional real local-model adapter; receives only features and acquired prefix."""
import json,random,time
from pathlib import Path
from collect_smollm_v47 import read,write,append,now,sha
from runtime_reasoning_v103 import Runtime
from reasoning_v102_common import payload,applied_settings
from escalation.transfer_v41 import rank
ROOT=Path(__file__).resolve().parents[1]

def prepare(c,prefix,rows,seed):
 available=[i for i in prefix.order if i not in prefix.ids]
 best=rank(c,prefix,available)[:20];extra=random.Random(112000+seed).sample([i for i in available if i not in best],20)
 shortlist=best+extra;random.Random(112100+seed).shuffle(shortlist)
 names=list(c.names)
 intro='Choose seven NGINX configurations likely to minimize the elapsed time of a fixed HTTP workload. Return only a JSON array of seven distinct candidate IDs, integers from0through39. No explanations. You have only the ten measured configurations below. All other performance is unknown. Lower seconds is better. Each proposed configuration will be run once; the best measured incumbent then receives three charged confirmation runs. Total budget20includes the ten prior evaluations.\n'
 semantics='System: NGINX1.28.3 on macOS arm64, kqueue. Immutable32768-byte file,16persistent connections driven by four validating C processes.1,048,576requests per batch. All response bytes are checked. workers=worker processes; cache=open_file_cache off/on; sendfile=off/on; buffer_count and buffer_size apply only if sendfile=0; sendfile_chunk applies only if sendfile=1; zero denotes an inactive branch setting; tcp_nodelay=off/on; postpone_output and sndbuf are bytes. tcp_nopush and multi_accept are fixed off. Socket/client and server costs both enter elapsed time. Candidate IDs do not imply a ranking.\n'
 measured=[dict(settings=[rows[i][k] for k in names],seconds=y[0]) for i,y in zip(prefix.ids,prefix.labels)]
 candidates=[dict(id=j,settings=[rows[i][k] for k in names]) for j,i in enumerate(shortlist)]
 text=intro+semantics+'Feature column order:'+json.dumps(names,separators=(',',':'))+'\nObserved:'+json.dumps(measured,separators=(',',':'))+'\nCandidates:'+json.dumps(candidates,separators=(',',':'))
 return {'messages':[{'role':'user','content':text}],'shortlist_row_ids':shortlist,'observed_row_ids':prefix.ids.copy(),'observed_labels':[y[:] for y in prefix.labels],'seed':seed}

def parse(response):
 if response.get('truncated') is not False or response.get('stop_type')!='eos':return None
 if type(response.get('tokens_predicted')) is not int or not 0<response['tokens_predicted']<=128:return None
 try:ids=json.loads(response['content'])
 except (ValueError,KeyError,TypeError):return None
 if not isinstance(ids,list) or len(ids)!=7 or any(type(x) is not int or not 0<=x<40 for x in ids) or len(set(ids))!=7:return None
 return ids

def collect(out,c,prefix,rows,seed,cfg):
 assert cfg['allow_paid_api'] is False and cfg['allow_cloud'] is False and cfg['max_external_spend_usd']==0
 assert cfg['new_generation_request_cap']==cfg['scientific_request_cap']==1 and cfg['max_allocated_output_tokens']==128 and cfg['compatibility_request_cap']==0
 out.mkdir();job=prepare(c,prefix,rows,seed);write(out/'input.json',job)
 manifest=read(ROOT/'artifacts/study_v91/model_manifest.json')
 if sha(ROOT/manifest['path'])!=manifest['sha256']:raise ValueError('model hash mismatch')
 write(out/'model_manifest.json',manifest)
 rt=Runtime(out,cfg);choice={'status':'fallback','reason':'not_started','selected_ids':[],'row_ids':[]}
 try:
  rt.start();base=rt.api('/apply-template',{'messages':job['messages']})
  if not base['prompt'].endswith('<|im_start|>assistant\n'):raise ValueError('unexpected model template')
  rendered=base['prompt']+'<think>\n\n</think>\n\n';tokens=rt.api('/tokenize',{'content':rendered,'add_special':False,'parse_special':True})['tokens']
  write(out/'preflight.json',dict(base_template=base,prompt=rendered,prompt_tokens=tokens,input_sha256=sha(out/'input.json')))
  if len(tokens)+128>cfg['context_tokens']:raise ValueError('context budget')
  p=payload(rendered,seed,'nonthinking','final');t=time.monotonic();response=rt.generate(p,'scientific','nginx_'+str(seed))
  write(out/'response.json',dict(at=now(),response=response,wall_seconds=time.monotonic()-t));applied_settings(response,p)
  ids=parse(response)
  if ids is not None:choice={'status':'valid','selected_ids':ids,'row_ids':[job['shortlist_row_ids'][j] for j in ids]}
  else:choice.update(reason='invalid_response')
 except Exception as e:choice.update(reason=repr(e))
 finally:
  rt.close();write(out/'choice.json',choice)
 # Caller applies a declared classical fallback; never describe fallback as LLM output.
 return choice
