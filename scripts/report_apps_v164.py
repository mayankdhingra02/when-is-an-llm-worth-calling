"""Descriptive development interface contrasts from measured, provenance-bound records."""
import json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v164';O=ROOT/'results/v164_native';M=ROOT/'results/v164_models';MODELS=['smollm3_3b','qwen3_8b'];CONDITIONS=['numeric','catalog'];CONTROLS=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal']
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def robust(b,a):
 return (b['median']-a['median'])/b['median']>.1 and b['row_id']!=a['row_id'] and all(x['valid'] and x['mad']<=.05 and x['median']>=.01 for x in [a,b])
def aggregate(selections,acq):
 arms={}
 for s in selections:
  rr=[r for r in acq if r['case']==s['case'] and r['arm']==s['arm'] and r['phase']=='validation'];assert len(rr)==3;vals=[r['value'] for r in rr];med=statistics.median(vals);arms[s['case'],s['arm']]={**s,'median':med,'mad':statistics.median(abs(v-med) for v in vals)/med,'valid':all(r['status']=='correct' for r in rr),'values':vals}
 contrasts=[];secondary=[]
 for j in read(A/'jobs.json'):
  for model in MODELS:
   n=arms[j['key'],model+'_numeric'];c=arms[j['key'],model+'_catalog'];contrasts.append({'case':j['key'],'engine':j['engine'],'model':model,'gain':(n['median']-c['median'])/n['median'],'same_setting':n['row_id']==c['row_id'],'catalog_robust_win':robust(n,c),'catalog_robust_loss':robust(c,n)})
   for condition in CONDITIONS:
    arm=model+'_'+condition;x=arms[j['key'],arm];g={b:(arms[j['key'],b]['median']-x['median'])/arms[j['key'],b]['median'] for b in CONTROLS};secondary.append({'case':j['key'],'engine':j['engine'],'model':model,'condition':condition,'gains':g,'joint_robust_win':all(robust(arms[j['key'],b],x) for b in CONTROLS[:3])})
 return arms,contrasts,secondary

def main():
 acq=[read(O/'acquisitions'/f'{i:03d}.json') for i in range(1,901)];arms,contrasts,secondary=aggregate(read(O/'selections.json'),acq);summary=[];mechanisms=[];costs=[]
 for model in MODELS:
  led=read(M/model/'ledger.json');rs=lines(M/model/'responses.jsonl');starts=lines(M/model/'generation_starts.jsonl')
  for condition in CONDITIONS:
   responses=[r for r in rs if r['key'].endswith('__'+condition)];count=sum(s['identity'].endswith('__'+condition) for s in starts);usage={};unknown={}
   for k in ['tokens_evaluated','tokens_predicted']:
    usage[k]=sum(r['response'].get(k,0) or 0 for r in responses);unknown[k]=sum(r['response'].get(k)is None for r in responses)
   costs.append({'model':model,'condition':condition,'intended_calls':10,'starts':count,'responses':len(responses),'valid_responses':sum(read(M/model/'scores'/f"{r['key']}.json")['status']=='valid' for r in responses),'observed_usage':usage,'unknown_usage_responses':unknown,'request_seconds':sum(r['wall_seconds'] for r in responses),'whole_model_ledger':led})
  for engine in ['ripgrep','hnswlib']:
   cases=[r for r in contrasts if r['model']==model and r['engine']==engine];summary.append({'engine':engine,'model':model,'cases':len(cases),'mean_catalog_gain':statistics.mean(r['gain'] for r in cases),'same_setting_pairs':sum(r['same_setting'] for r in cases),'catalog_robust_wins':sum(r['catalog_robust_win'] for r in cases),'catalog_robust_losses':sum(r['catalog_robust_loss'] for r in cases)})
   for condition in CONDITIONS:
    recs=[read(O/'search'/f"{j['key']}__{model}_{condition}.json") for j in read(A/'jobs.json') if j['engine']==engine];d=[d for r in recs for d in r['projection'][:7]];all_d=[d for r in recs for d in r['projection']];prefix=sum(min(range(17),key=lambda k:r['state']['labels'][k][0])<10 for r in recs)
    mechanisms.append({'engine':engine,'model':model,'condition':condition,'intended_evaluated_proposals':35,'observed_evaluated_proposals':len(d),'evaluated_projected':sum(x['distance']>0 for x in d),'evaluated_duplicates':sum(x['duplicate_proposal'] for x in d),'all_proposals':len(all_d),'all_projected':sum(x['distance']>0 for x in all_d),'all_duplicates':sum(x['duplicate_proposal'] for x in all_d),'prefix_incumbents':prefix,'fallback_cases':sum(r['fallback'] for r in recs)})
 coll={'new_configuration_outcomes':len(acq),'new_native_invocations':sum(r['measurement']['native_invocations'] for r in acq),'reused_historical_prefix_outcomes':100,'reused_historical_prefix_invocations':300,'quality_penalties':sum(r['status']!='correct' for r in acq),'native_objective_seconds':sum(r['measurement']['objective_seconds'] for r in acq),'subprocess_seconds':sum(r['collection_seconds'] for r in acq),'stage_seconds':read(O/'completion.json')['seconds'],'unstable_validation_cells':sum(x['mad']>.05 for x in arms.values()),'below_floor_validation_cells':sum(x['median']<.01 for x in arms.values())}
 result={'scope':'Exploratory development comparison of compound interfaces on already exposed applications; not held-out routing evaluation','arms':list(arms.values()),'contrasts':contrasts,'summary':summary,'secondary':secondary,'mechanisms':mechanisms,'model_costs':costs,'collection':coll};(O/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
 text=['# V164: explicit-candidate interface experiment','','This development experiment compares fresh numeric-prototype and explicit-catalog calls on the same ten saved prefixes. Both small local models are real. Candidate enumeration, eligible-ID grammar and output representation change together; their individual effects are not identified. No new held-out system or learned-router improvement is claimed.','','## Primary interface comparison','','Positive gain means the catalog incumbent has lower median fresh-validation utility than the numeric incumbent. Practical wins require >10%, different settings, valid quality, MAD<=5% and both medians>=10ms. All intended cases remain.','','| Application | Model | Mean catalog gain vs numeric | Same setting / 5 | Robust catalog wins / losses |','|---|---|---:|---:|---:|']
 for r in summary:text.append(f"| {r['engine']} | {r['model']} | {100*r['mean_catalog_gain']:+.3f}% | {r['same_setting_pairs']} | {r['catalog_robust_wins']} / {r['catalog_robust_losses']} |")
 text+=['','## Proposal mechanism','','Counts below cover only the first seven evaluated proposals per case; all-ten counts are retained in comparison.json. Repeated proposals are resolved to distinct unseen evaluations with the same feature-distance rule. Missing/invalid responses use charged sequential fallback.','','| Application | Model / interface | Projected / 35 | Duplicate proposals / 35 | Prefix incumbent / 5 | Fallback cases |','|---|---|---:|---:|---:|---:|']
 for r in mechanisms:text.append(f"| {r['engine']} | {r['model']} / {r['condition']} | {r['evaluated_projected']} | {r['evaluated_duplicates']} | {r['prefix_incumbents']} | {r['fallback_cases']} |")
 text+=['','## Secondary comparison with fresh classical continuations','','| Application | Model / interface | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins / 5 |','|---|---|---:|---:|---:|---:|']
 for e in ['ripgrep','hnswlib']:
  for model in MODELS:
   for condition in CONDITIONS:
    rr=[x for x in secondary if x['engine']==e and x['model']==model and x['condition']==condition];g=[statistics.mean(x['gains'][b] for x in rr) for b in CONTROLS[:3]];text.append(f"| {e} | {model} / {condition} | {100*g[0]:+.3f}% | {100*g[1]:+.3f}% | {100*g[2]:+.3f}% | {sum(x['joint_robust_win'] for x in rr)} |")
 text+=['','## Accounting and reliability','',f"New collection: {coll['new_configuration_outcomes']} configuration outcomes / {coll['new_native_invocations']} native invocations / {sum(c['starts'] for c in costs)} model starts. Separately reused historical prefixes:100 outcomes/300 invocations; their collection cost was incurred in V163. Ninety logical B20 arms use10 shared prefix+7 new search+3 validation. All incumbents were fixed before270 randomized validation outcomes. Quality penalties:{coll['quality_penalties']}; unstable validation cells:{coll['unstable_validation_cells']}/90; below10ms:{coll['below_floor_validation_cells']}/90. These flags do not remove cases from descriptive means.", '', '| Model / interface | Starts / intended | Valid responses | Observed input / output tokens | Request seconds |','|---|---:|---:|---:|---:|']
 for c in costs:text.append(f"| {c['model']} / {c['condition']} | {c['starts']}/10 | {c['valid_responses']} | {c['observed_usage']['tokens_evaluated']} / {c['observed_usage']['tokens_predicted']} | {c['request_seconds']:.3f} |")
 text+=['',f"Native subprocess time{coll['subprocess_seconds']:.3f}s, including{coll['native_objective_seconds']:.3f}objective-seconds; total stage{coll['stage_seconds']:.3f}s/1800s. Model cold-start, whole-stage/RSS/exit and unknown-usage fields are retained in comparison.json and raw ledgers. No paid/cloud use, retry or new download. Research collection includes all interfaces and controls. A ten-case deployment would use one branch per case:200 logical outcomes/600 native invocations plus selected requests; that is an estimate, not measured deployment or a dollar/energy claim.", '', '## Interpretation boundaries','', 'Two exposed applications and one host cannot establish generalization. Equal prefix reuse makes the interface pairing explicit but does not remove temporal cache/load drift. Calls are interleaved by a fixed shuffled plan within each model; model order remains fixed. Seeds do not create independent systems. Historical numeric results were not reused as the fresh numeric comparator. Same-setting timing differences, small noisy effects and lowered projection counts do not establish optimizer benefit. No router is refitted; historical controller thresholds are not validated for this interface. Any further prompt selection uses these cases only as development data.','','Raw evidence: artifacts/study_v164/freeze.json binds protocol, code, prompts, model pins and reused prefix provenance. results/v164_models holds every request/response and resource ledger. results/v164_native holds900 charged records,90 branch states and270 validations. Analysis code: scripts/report_apps_v164.py.']
 (ROOT/'reports/apps_v164.md').write_text('\n'.join(text)+'\n')
 plt.rcParams['svg.hashsalt']='v164-interfaces';fig,axs=plt.subplots(1,2,figsize=(11,4),sharey=True);fig.subplots_adjust(left=.1,right=.98,top=.76,bottom=.17,wspace=.2)
 limit=max(15,5+max(abs(100*x['gain']) for x in contrasts))
 for ax,engine in zip(axs,['ripgrep','hnswlib']):
  for k,model in enumerate(MODELS):
   rows=[r for r in contrasts if r['engine']==engine and r['model']==model];ax.scatter([k+(i-2)*.055 for i in range(5)],[100*r['gain'] for r in rows],s=35,color=['#176d8c','#b95c2d'][k])
  ax.axhline(0,color='gray',lw=.8);ax.axhline(10,color='gray',ls=':');ax.axhline(-10,color='gray',ls=':');ax.set_xticks([0,1],['SmolLM3-3B','Qwen3-8B']);ax.set_xlim(-.3,1.3);ax.set_ylim(-limit,limit);ax.set_title(engine);ax.grid(axis='y',alpha=.2)
 axs[0].set_ylabel('Catalog gain vs fresh numeric (%)');fig.suptitle('Development interface intervention: fresh validation\nTwo exposed application groups; dots are paired seeds');fig.savefig(O/'interface_gains.png',dpi=160,metadata={'Software':'V164'});fig.savefig(O/'interface_gains.svg',metadata={'Date':None});plt.close(fig);print(json.dumps({'collection':coll,'summary':summary,'mechanisms':mechanisms},indent=2))
if __name__=='__main__':main()
