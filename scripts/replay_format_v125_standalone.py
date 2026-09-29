"""Standard-library format-probe replay; no objective table needed or queried."""
from pathlib import Path
import hashlib,json,re,math
ROOT=Path(__file__).resolve().parent

def read(n):return json.loads((ROOT/n).read_text())
def lines(n):return [json.loads(x) for x in (ROOT/n).read_text().splitlines()]
def valid(r):
 if r is None:return False
 o=r['response'];text=o.get('content');n=o.get('tokens_predicted');m=None if not isinstance(text,str) else re.fullmatch(r'\s*## (-?(?:\d+(?:\.\d*)?|\.\d+)) ##\s*',text)
 return bool(m and type(n) is int and 0<n<=32 and o.get('truncated') is False and o.get('stop_type')=='eos' and math.isfinite(float(m[1])))

def main():
 for n,m in read('manifest.json')['files'].items():
  b=(ROOT/n).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],n
 jobs=read('artifacts/study_v125/jobs.json');starts=lines('results/v125_format/generation_starts.jsonl');raw=lines('results/v125_format/responses.jsonl');old={r['key']:r for r in lines('results/v124_surrogate/responses.jsonl')};ledger=read('results/v125_format/ledger.json');sm={s['identity']:s for s in starts};rm={r['key']:r for r in raw}
 assert len(starts)==len(sm)==ledger['generation_requests']<=18 and len(raw)==len(rm)<=len(starts);assert ledger['allocated_output_tokens']==32*len(starts)<=576 and ledger['stage_seconds']<=500 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['retries']==ledger['external_spend_usd']==0
 assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]]
 counts={k:{'intended':9,'valid':0,'original_valid_same9':0} for k in ['marked_json','reference_text']}
 for j in jobs:
  original=read(f"results/v124_surrogate/preflight/{j['original_request_key']}.json")['messages'];base=json.loads(original[1]['content']);expected=read(j['messages_path']);pre=read(f"results/v125_format/preflight/{j['key']}.json");assert pre['messages']==expected and len(pre['prompt_tokens'])+32<=4096
  if j['condition']=='marked_json':
   for o in base['observed_examples']:o['performance']='## '+o['performance']+' ##'
   assert expected[0]==original[0] and json.loads(expected[1]['content'])==base
  else:
   names=base['feature_order']
   def settings(xs):return ', '.join(f'{k} is {int(v) if float(v).is_integer() else v}' for k,v in zip(names,xs))
   meaning=read('data/manifest_v41.json')['datasets'];meaning=next(s['meaning'] for s in meaning if s['id']==j['dataset'])
   text=f'The following are software configurations and the corresponding performance measured in {meaning}. Your response should only contain the predicted {meaning} in the format ## performance ##.'
   for o in base['observed_examples']:text+='\nHyperparameter configuration: '+settings(o['settings'])+'\nPerformance: ## '+o['performance']+' ##'
   text+='\nHyperparameter configuration: '+settings(base['new_configuration'])+'\nPerformance: ';assert expected==[original[0],{'role':'user','content':text}]
  if j['key'] in sm:
   assert sm[j['key']]['payload']=={'prompt':pre['rendered']['prompt'],'n_predict':32,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.,'seed':j['sampling_seed'],'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
  if j['key'] in rm:assert rm[j['key']]['response']['prompt']==pre['rendered']['prompt']
  counts[j['condition']]['valid']+=valid(rm.get(j['key']));counts[j['condition']]['original_valid_same9']+=valid(old.get(j['original_request_key']))
 comparison=read('results/v125_analysis/comparison.json');assert counts==comparison['conditions'] and comparison['new_objective_acquisitions']==0
 print(json.dumps({'verified':True,'new_requests_replayed':len(starts),'original_scheduled_references':9,'conditions':counts,'new_inference':0,'new_objective_acquisitions':0}))
if __name__=='__main__':main()
