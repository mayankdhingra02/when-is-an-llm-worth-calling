"""Deterministic descriptive paired contrasts; never acquires labels or infers."""
from fractions import Fraction as F
from collect_smollm_v47 import ROOT,read,write,sha
import json
MODELS=['qwen3_8b','smollm3_3b'];REFS=['sequential_3nn','adaptive_incumbent_neighbor','fixed_prefix_neighbor','random_full','prefix']
def gain(ref,v,d):
 ref=F(str(ref));v=F(str(v));return (ref-v)/ref if d=='-' else (v-ref)/ref
def stats(v):
 return {'cases':len(v),'mean_fraction':str(sum(v)/len(v)),'mean_percent':float(100*sum(v)/len(v)),'wins':sum(x>0 for x in v),'ties':sum(x==0 for x in v),'losses':sum(x<0 for x in v),'benefit_over_1pct':sum(x>F(1,100) for x in v),'harm_over_1pct':sum(x< -F(1,100) for x in v)}
def main():
 a=ROOT/'artifacts/study_v141';modeldirs=read(ROOT/'artifacts/study_v142/model_paths.json');o=ROOT/'results/v141_analysis';s=read(o/'summary.json');assert s['complete'];arms=[read(o/'arms'/f'{k}.json') for k in s['arms']];groups=sorted({r['system_group'] for r in arms});rows=[]
 for r in arms:
  refs={m:v['target'] for m,v in r['references'].items()};refs['prefix']=r['prefix_best'];rows.append({'key':r['key'],'case_key':r['case_key'],'model':r['model'],'system_group':r['system_group'],'seed':r['seed'],'target':r['target'],'direction':r['direction'],'references':refs,'fallback':r['fallback'],'gains':{m:str(gain(v,r['target'],r['direction'])) for m,v in refs.items()}})
 groupstats={g:{m:{ref:stats([F(r['gains'][ref]) for r in rows if r['model']==m and r['system_group']==g]) for ref in REFS} for m in MODELS} for g in groups}
 totals={m:{ref:stats([F(r['gains'][ref]) for r in rows if r['model']==m]) for ref in REFS} for m in MODELS}
 paired=[]
 for j in read(a/'jobs.json'):
  q=next(r for r in rows if r['case_key']==j['key'] and r['model']==MODELS[0]);b=next(r for r in rows if r['case_key']==j['key'] and r['model']==MODELS[1]);paired.append({'case_key':j['key'],'system_group':j['system_group'],'seed':j['seed'],'qwen':q['target'],'smol':b['target'],'smol_gain':str(gain(q['target'],b['target'],q['direction']))})
 pairgroups={g:stats([F(r['smol_gain']) for r in paired if r['system_group']==g]) for g in groups};cost={};quality={}
 for m in MODELS:
  raw=[json.loads(l) for l in (ROOT/modeldirs[m]/'responses.jsonl').read_text().splitlines()];ledger=read(ROOT/modeldirs[m]/'ledger.json');usage={}
  for field in ['tokens_predicted','tokens_evaluated']:
   vals=[r['response'].get(field) for r in raw];usage[field]={'observed_sum':sum(v for v in vals if type(v) is int),'missing_intended':30-sum(type(v) is int for v in vals)}
  subset=[r for r in arms if r['model']==m];diag=[d for r in subset for d in r['projection']];cost[m]={'ledger':ledger,'usage':usage,'request_wall_seconds':sum(r['wall_seconds'] for r in raw),'new_recorded_acquisitions':sum(r['new_accesses'] for r in subset)};quality[m]={'valid':sum(not r['fallback'] for r in subset),'fallbacks':sum(r['fallback'] for r in subset),'intended':30,'projection_records':len(diag),'positive_distance':sum(d['hamming_distance']>0 for d in diag),'repeated_proposal':sum(d['repeated_proposal'] for d in diag),'matches_prefix':sum(d['matches_initial_observation'] for d in diag),'joint_over_1pct_vs_sequential_and_adaptive':sum(all(F(r['gains'][c])>F(1,100) for c in REFS[:2]) for r in rows if r['model']==m)}
 result={'scope':'six exposed families; no fitted router, no held-out claim','rows':rows,'groups':groupstats,'totals':totals,'smol_vs_qwen':{'rows':paired,'groups':pairgroups,'total':stats([F(r['smol_gain']) for r in paired])},'reliability':quality,'cost':{'actual':cost,'failed_startup':read(ROOT/'results/v141_models/smollm3_3b/ledger.json'),'startup_repairs':1,'new_recorded_acquisitions':s['new_recorded_acquisitions'],'evaluation_seconds':s['seconds'],'combined_collection_seconds':s['combined_collection_seconds'],'estimated_deployment':{'B':20,'prefix':10,'new_evaluations':10,'model_requests':1,'allocated_output_tokens':1024,'loading':'separate cold-start amortization, no dollar or native-time conversion'}}}
 write(o/'comparison.json',result)
 lines=['# V141–V142: matched local-model replication with preserved startup repair','','Both models actually ran on the same 30 original B10 prefixes: six previously exposed software families, five seeds each. Byte-identical messages, canonical ten-proposal grammar, output budget1024, thinking off, same sampling seed per case. Each continuation acquired ten recorded outcomes, retaining the prefix incumbent. Native software was not executed. Model templates/tokenizers differ; this is a comparison of complete model treatments, not a causal parameter-count experiment.','','Positive percentages favor the named model over the control. Seeds within a family are dependent; no population significance or held-out claim.','','| Family | Model | Gain vs sequential | W/T/L | Gain vs adaptive neighbor | W/T/L |','|---|---|---:|---|---:|---|']
 for g in groups:
  for m in MODELS:
   b=groupstats[g][m]['sequential_3nn'];c=groupstats[g][m]['adaptive_incumbent_neighbor'];lines.append(f"| {g} | {m} | {b['mean_percent']:+.4f}% | {b['wins']}/{b['ties']}/{b['losses']} | {c['mean_percent']:+.4f}% | {c['wins']}/{c['ties']}/{c['losses']} |")
 lines+=['','Equal-seed family means receive equal weight here (five seeds each); do not confuse 30 cases with 30 systems. All secondary controls and individual cases are in comparison.json.','','| Model | Control | Mean gain | W/T/L | >1% benefit / harm |','|---|---|---:|---|---|']
 for m in MODELS:
  for ref in REFS:
   c=totals[m][ref];lines.append(f"| {m} | {ref} | {c['mean_percent']:+.4f}% | {c['wins']}/{c['ties']}/{c['losses']} | {c['benefit_over_1pct']}/{c['harm_over_1pct']} |")
 lines+=['','| Family | SmolLM gain vs Qwen | W/T/L |','|---|---:|---|']
 for g,c in pairgroups.items():lines.append(f"| {g} | {c['mean_percent']:+.4f}% | {c['wins']}/{c['ties']}/{c['losses']} |")
 lines+=['','## Reliability and actual cost','','SmolLM initially failed its local pre-start socket check after Qwen exited; no SmolLM process, HTTP request or generation occurred in that attempt. Before any new objective acquisition, V142 froze one startup repair on a distinct loopback port, retaining the original60-request/600-acquisition/1800-second limits. Original failed startup cost0.763504625s is additional to the per-model lifecycle figures below; startup repairs1, model-request retries0. Original failure receipts remain unchanged.','']
 for m in MODELS:
  c=cost[m];q=quality[m];l=c['ledger'];u=c['usage'];lines.append(f"{m}: {l['generation_requests']}/30 requests, {q['valid']} valid, {q['fallbacks']} fallback; {l['retries']} retries. Generated/prefill observed tokens {u['tokens_predicted']['observed_sum']}/{u['tokens_evaluated']['observed_sum']}, missing intended usage {u['tokens_predicted']['missing_intended']}/{u['tokens_evaluated']['missing_intended']}. Lifecycle {l['stage_seconds']:.3f}s; request-only sum {c['request_wall_seconds']:.3f}s; peak sampled RSS {l['peak_server_rss_bytes']:,}bytes. Projected away from proposed setting {q['positive_distance']}/{q['projection_records']}; repeated proposals {q['repeated_proposal']}; proposals matching prefix {q['matches_prefix']}. Joint >1% benefit over both sequential and adaptive neighbor: {q['joint_over_1pct_vs_sequential_and_adaptive']}/30.\n")
 lines+=[f"Actual new collection: {s['new_recorded_acquisitions']} recorded acquisitions, {s['seconds']:.3f}s evaluation stage, {s['combined_collection_seconds']:.3f}s combined collection. Historical prefixes and four comparator arms per case are reused with verified identities and original costs retained. Estimated deployment chooses one model, one request and B20 total; collecting both arms costs twice the new-label budget. Zero paid/cloud use or new downloads. Model-block order and cache/thermal effects limit latency comparisons; missing usage is not zero.",'','## Scope and interpretation','','This fixed replication assesses whether cheap-control comparisons depend on the model. It does not fit or validate a benefit-aware controller, create new independent test families, establish model reasoning, or reproduce SNAP2 exactly. Frozen practical margin is1%; all cases including failures remain in the denominator. Recorded-source correctness/noise/utility qualifications persist. Older SAC failures and earlier conflicting results are not replaced. Two differently trained models and quantized templates are not a model-size scaling study. Repeatedly exposed families and protocol development rule out confirmatory generalization claims.','','Next priority remains a coherent prospective independent-family evaluation. Do not choose its families, prompts or thresholds because of favorable outcomes here. Cross-host/native and further model replication address distinct gaps; no journal acceptance guarantee.','','Artifacts: reports/protocol_v141.md and protocol_v142.md with their freezes; artifacts/study_v141 (jobs, models, inputs, source extracts, tests); results/v141_models and results/v142_smollm (actual payloads/preflight/raw responses/ledgers); results/v141_analysis (sealed selections,600 acquisition receipts,60 arms,comparison.json and figures).']
 (ROOT/'reports/models_v141.md').write_text('\n'.join(lines)+'\n')
 import matplotlib;matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v141'
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
 for ax,ref in zip(axes,REFS[:2]):
  for k,m in enumerate(MODELS):ax.bar([i+(k-.5)*.38 for i in range(len(groups))],[groupstats[g][m][ref]['mean_percent'] for g in groups],.38,label=m)
  ax.axhline(0,color='black',linewidth=.7);ax.axhline(1,color='grey',linestyle=':',linewidth=.7);ax.axhline(-1,color='grey',linestyle=':',linewidth=.7);ax.set_xticks(range(len(groups)),groups,rotation=20,ha='right');ax.set_ylabel('Mean model gain (%)');ax.set_title('Versus '+ref);ax.legend(fontsize=8)
 fig.suptitle('Two local models; six exposed software families (five seeds each)')
 fig.savefig(o/'comparison.png',dpi=160);fig.savefig(o/'comparison.svg',metadata={'Date':None});plt.close(fig)
 print(json.dumps({'totals':totals,'reliability':quality},indent=2))
if __name__=='__main__':main()
