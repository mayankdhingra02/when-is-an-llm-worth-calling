"""In-memory semantic mutations of saved evidence; original files untouched."""
import copy,json,sys,time
from pathlib import Path
import verify_spark_v145 as v
read,jl=v.read,v.jl
cases=['reported_gain','request_undercount','acquired_target','late_selection']
results=[]
for case in cases:
 def changed_read(path):
  d=read(path)
  if case=='reported_gain' and path=='results/v145_spark/comparison.json':d['models']['qwen3_8b']['contrasts']['sequential_3nn']['equal_workload_mean_complete_pairs']+=.02
  if case=='request_undercount' and path=='results/v145_models/qwen3_8b/ledger.json':d['generation_requests']-=1
  if case=='late_selection' and path=='results/v145_spark/selection_seal.json':d['at_unix']+=86400
  return d
 def changed_jl(path):
  d=jl(path)
  if case=='acquired_target' and path=='results/v145_spark/acquisitions.jsonl':d[-1]['value']+=1
  return d
 v.read,v.jl=changed_read,changed_jl
 try:v.verify()
 except AssertionError:results.append({'mutation':case,'rejected':True})
 else:raise RuntimeError('Mutation escaped: '+case)
 finally:v.read,v.jl=read,jl
out={'all_rejected':True,'scope':'In-memory decoded semantic mutations; original files unchanged and transport hashes still pass','cases':results}
(v.ROOT/'artifacts/study_v145/semantic_mutations.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
