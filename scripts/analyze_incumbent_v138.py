"""Descriptive replay of acquired observations; no new labels or inference."""
import json, statistics
from collect_smollm_v47 import ROOT,read,write
OUT=ROOT/'results/v138_incumbent'
MODES=['fixed_prefix_neighbor','adaptive_incumbent_neighbor']
def gain(ref,value,direction):return (ref-value)/ref if direction=='-' else (value-ref)/ref
def contrast(values):return {'mean':statistics.mean(values),'wins':sum(v>1e-12 for v in values),'ties':sum(abs(v)<=1e-12 for v in values),'losses':sum(v< -1e-12 for v in values)}
def main():
 jobs=read(ROOT/'artifacts/study_v138/jobs.json');summary=read(OUT/'summary.json');assert summary['complete'];rows=[]
 for j in jobs:
  spec=read(ROOT/f"artifacts/study_v138/candidates/{j['system_group']}.json")['spec'];direction=spec['direction'];best=lambda s:(min if direction=='-' else max)(y[0] for y in s['labels'])
  r={'key':j['key'],'system_group':j['system_group'],'seed':j['seed'],'direction':direction,'prefix':best(read(ROOT/j['prefix'])['state'])}
  for mode in MODES:r[mode]=best(read(OUT/'arms'/f"{j['key']}_{mode}.json")['state'])
  for mode,path in [('historical_model',j['model_arm']),('historical_sequential',j['classical_arm'])]:r[mode]=best(read(ROOT/path)['state'])
  if j['system_group'] in ['llvm','sac']:
   for mode in ['feedback','masked']:r['historical_'+mode]=best(read(ROOT/f"results/v136_feedback/arms/{j['key']}_{mode}.json")['state'])
  rows.append(r)
 groups={}
 for group in sorted({r['system_group'] for r in rows}):
  rs=[r for r in rows if r['system_group']==group];g={}
  refs=['prefix','historical_sequential','historical_model']+(['historical_feedback','historical_masked'] if group in ['llvm','sac'] else [])
  for mode in MODES:
   for ref in refs:g[f'{mode}_vs_{ref}']=contrast([gain(r[ref],r[mode],r['direction']) for r in rs])
  g['adaptive_vs_fixed']=contrast([gain(r[MODES[0]],r[MODES[1]],r['direction']) for r in rs]);groups[group]=g
 result={'scope':'Prospective control collection on six exposed families; descriptive development, not held out','rows':rows,'groups':groups,'actual_collection_cost':{'new_recorded_acquisitions':summary['new_acquisitions'],'model_requests':0,'seconds':summary['seconds'],'note':'Both arms collected; original B10 prefixes and historical comparators retain prior collection costs. Recorded table access is not native workload execution.'},'estimated_deployment':{'total_evaluations':20,'prefix_evaluations':10,'continuation_evaluations':10,'model_requests':0,'note':'One chosen heuristic; no monetary or native runtime saving inferred.'}}
 write(OUT/'comparison.json',result)
 text=['# V138: cheap incumbent-neighbor controls','','Actual execution: 30 saved B10 cases, six exposed software families, five fixed seeds (11, 23, 37, 53, 71), two B20 continuations per case. The fixed control searches around the best prefix setting; the adaptive control follows its current best observed setting. Both use Hamming distance, deterministic prefix-order tie breaking, and ten charged new evaluations. No LLM is used by either new control.','','Positive percentages favor the named cheap control. W/T/L counts describe five repeated seeds within one system, not five independent systems.','','| Family | Control | Mean gain vs sequential3NN | W/T/L | Mean gain vs valid one-shot Qwen3-8B | W/T/L |','|---|---|---:|---:|---:|---:|']
 for group,g in groups.items():
  for mode in MODES:
   a=g[f'{mode}_vs_historical_sequential'];b=g[f'{mode}_vs_historical_model'];text.append(f"| {group} | {mode} | {100*a['mean']:.4f}% | {a['wins']}/{a['ties']}/{a['losses']} | {100*b['mean']:.4f}% | {b['wins']}/{b['ties']}/{b['losses']} |")
 text+=['','Historical one-shot comparators use V127 normal responses for five families and V135 capacity-repaired SAC responses. These were real local Qwen3-8B calls, not regenerated or fabricated for this extension. Original failed SAC attempts remain in the historical denominator and collection costs; this table explicitly compares the repaired valid treatment. Historical sequential controls are V41. Same B10 identities and acquired values are checked. Old source manifests may retain their original split names; all six families are exposed development here.','','Optional previously declared feedback comparison covers only LLVM and SAC (ten cases):','','| Family | Control | Gain vs V136 feedback | W/T/L |','|---|---|---:|---:|']
 for group in ['llvm','sac']:
  for mode in MODES:
   a=groups[group][f'{mode}_vs_historical_feedback'];text.append(f"| {group} | {mode} | {100*a['mean']:.4f}% | {a['wins']}/{a['ties']}/{a['losses']} |")
 text+=['','V136 masked and feedback final incumbents coincide in all ten cases, so their contrasts coincide. This does not imply the search paths coincide.','','All individual outcomes (raw units; compare within a family only):','','| Family / seed | B10 | Fixed | Adaptive | Historical sequential | Historical model |','|---|---:|---:|---:|---:|---:|']
 for r in rows:text.append(f"| {r['system_group']} / {r['seed']} | {r['prefix']:.9g} | {r[MODES[0]]:.9g} | {r[MODES[1]]:.9g} | {r['historical_sequential']:.9g} | {r['historical_model']:.9g} |")
 text+=['',f"Actual new collection: 600 recorded outcomes, 60 completed arms, zero new model requests or native executions, {summary['seconds']:.6f}s collector runtime. Includes repeated historical rows as new charges in each arm. Table-access runtime is not native software cost. Modeled deployment selects one arm: B10 plus ten evaluations, B20 total, no model tokens/requests. Historical inference/prefix costs are not erased or attributed to this new collector.",'','These controls were frozen before their outcomes were acquired, but designed after earlier LLM/projection findings. This is a development extension, not a confirmatory holdout or novel optimizer. Neither the six systems nor the repeated seeds provide a fresh learned-router test. Hamming geometry, fixed recorded targets, unknown per-row noise/correctness, and historical one-shot prompt differences limit causal attribution. A control matching an LLM does not prove it generated the model behavior. No threshold, router, significance-driven retry or outcome-selected subgroup is fitted here.','','Protocol and freeze: reports/protocol_v138.md and protocol_v138.freeze.json. Raw evidence: results/v138_incumbent/selections, acquisitions.jsonl, arms and summary.json. Reproduce with `.venv/bin/python scripts/analyze_incumbent_v138.py`; independently verify with `.venv/bin/python scripts/verify_incumbent_v138.py`. Neither command acquires new outcomes.']
 (ROOT/'reports/incumbent_v138.md').write_text('\n'.join(text)+'\n')
 import matplotlib;matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v138-incumbent'
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
 for ax,ref,title in zip(axes,['historical_sequential','historical_model'],['Historical sequential3NN','Historical one-shot Qwen3-8B']):
  for offset,mode,label,color in [(-.17,MODES[0],'Fixed prefix neighbor','#2166ac'),(.17,MODES[1],'Adaptive incumbent neighbor','#b35806')]:
   ax.bar([i+offset for i in range(6)],[100*groups[g][f'{mode}_vs_{ref}']['mean'] for g in groups],.32,label=label,color=color)
  ax.axhline(0,color='black',linewidth=.7);ax.set_xticks(range(6),list(groups),rotation=30,ha='right');ax.set_title('Compared with '+title,fontsize=10);ax.set_ylabel('Mean relative gain (%) over five seeds');ax.legend(fontsize=8)
 fig.suptitle('Cheap B10 → B20 controls: six exposed systems (descriptive)',fontsize=12)
 fig.savefig(OUT/'comparison.png',dpi=170);fig.savefig(OUT/'comparison.svg',metadata={'Date':None});plt.close(fig)
 print(json.dumps(groups,indent=2))
if __name__=='__main__':main()
