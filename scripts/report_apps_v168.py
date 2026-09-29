"""Read-only analysis of measured paired application outcomes; no policy fitting."""
import json,math,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v168';O=ROOT/'results/v168_native';M=ROOT/'results/v168_models'
MODELS=['smollm3_3b','qwen3_8b'];ENGINES=['polars','xgboost'];CONTROLS=['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal']
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def summaries(rows,validations,acquisitions):
 arms={}
 for r in rows:
  vv=[x['value'] for x in validations if x['case']==r['case'] and x['arm']==r['arm']];assert len(vv)==3
  median=statistics.median(vv);mad=statistics.median(abs(x-median) for x in vv)/median;ms=[x for x in acquisitions if x['case']==r['case'] and x['arm']==r['arm'] and x['phase']=='validation'];assert len(ms)==3
  arms[r['case'],r['arm']]={**r,'validation_values':vv,'median':median,'relative_mad':mad,'quality_feasible':all(x['status']=='correct' for x in ms),'minimum_accuracy_or_exact_quality':min(x['measurement']['quality'] for x in ms),'stable':mad<=.05,'above_floor':median>=.01}
 cases=[]
 for model in MODELS:
  for key in sorted({r['case'] for r in rows}):
   a=arms[key,model];g={};wins={};same={}
   for control in CONTROLS:
    b=arms[key,control];g[control]=(b['median']-a['median'])/b['median'];same[control]=a['row_id']==b['row_id'];wins[control]=g[control]>.1 and not same[control] and all(x['stable'] and x['quality_feasible'] and x['above_floor'] for x in [a,b])
   cases.append({'case':key,'engine':a['engine'],'model':model,'gains':g,'same_configuration':same,'robust_practical_wins':wins,'joint_robust_win':all(wins[c] for c in ['sequential_3nn','adaptive_neighbor','gp_ei'])})
 return arms,cases
def main():
 assert read(O/'completion.json')['acquisitions']==800;acq=[read(O/'acquisitions'/f'{i:03d}.json') for i in range(1,801)];arms,cases=summaries(read(O/'selections.json'),lines(O/'validation.jsonl'),acq);decisions=read(A/'decisions.json')['rows'];modelcost={};policies=[]
 for model in MODELS:
  ledger=read(M/model/'ledger.json');rr=lines(M/model/'responses.jsonl');starts=lines(M/model/'generation_starts.jsonl');lookup={r['key']:r for r in rr}
  used={k:sum(r['response'][k] for r in rr if type(r['response'].get(k)) is int) for k in ['tokens_evaluated','tokens_predicted']};unknown={k:len(starts)-sum(type(r['response'].get(k)) is int for r in rr) for k in used}
  modelcost[model]={'ledger':ledger,'responses':len(rr),'observed_usage':used,'unknown_usage_requests':unknown,'request_wall_seconds':sum(r['wall_seconds'] for r in rr)}
  ds=[d for d in decisions if d['model']==model];names=list(ds[0]['policies'])+['rank_expected_adaptation','hindsight_oracle']
  for name in names:
   rows=[]
   for d in ds:
    key=d['case'];case=next(c for c in cases if c['case']==key and c['model']==model);g=case['gains']['sequential_3nn'];prob=d['rank_expected_call'] if name=='rank_expected_adaptation' else (float(g>0) if name=='hindsight_oracle' else float(d['policies'][name]))
    prefix=sum(x['collection_seconds'] for x in acq if x['case']==key and x['phase']=='prefix');bc={b:sum(x['collection_seconds'] for x in acq if x['case']==key and x['arm']==b) for b in ['sequential_3nn',model]};request=lookup.get(key);rt=request['wall_seconds'] if request else None
    proxy=prefix+(1-prob)*bc['sequential_3nn']+prob*bc[model]+(prob*rt if rt is not None else 0)
    rows.append({'case':key,'engine':d['engine'],'call_probability':prob,'gain':prob*g,'deployment_collection_proxy_seconds':proxy if rt is not None or prob==0 else None})
   means={e:statistics.mean(r['gain'] for r in rows if r['engine']==e) for e in ENGINES};policies.append({'model':model,'policy':name,'calls_or_expected_calls':sum(r['call_probability'] for r in rows),'group_mean_gains':means,'equal_group_mean_gain':statistics.mean(means.values()),'deployment_configuration_evaluations':200,'deployment_native_invocations':400,'collection_time_proxy_seconds':sum(r['deployment_collection_proxy_seconds'] for r in rows) if all(r['deployment_collection_proxy_seconds'] is not None for r in rows) else None,'rows':rows})
 native={'configuration_outcomes':800,'native_workload_invocations':sum(x['measurement']['native_invocations'] for x in acq),'quality_feasible':sum(x['status']=='correct' for x in acq),'quality_penalties':sum(x['status']=='quality_penalty' for x in acq),'subprocess_collection_seconds':sum(x['collection_seconds'] for x in acq),'native_objective_seconds':sum(x['measurement']['objective_seconds'] for x in acq),'end_to_end_seconds':read(O/'completion.json')['seconds'],'minimum_xgboost_accuracy':min(x['measurement']['quality'] for x in acq if x['engine']=='xgboost')}
 result={'cases':cases,'arms':list(arms.values()),'policies':policies,'model_costs':modelcost,'actual_collection':native};write(O/'comparison.json',result)
 plt.rcParams['svg.hashsalt']='v168';fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True);fig.subplots_adjust(left=.09,right=.98,bottom=.25,top=.77,wspace=.3)
 vals=[100*c['gains']['sequential_3nn'] for c in cases];axes[0].set_ylim(min(-15,math.floor(min(vals)/10)*10-5),max(15,math.ceil(max(vals)/10)*10+5))
 for ax,e in zip(axes,ENGINES):
  for mi,m in enumerate(MODELS):
   cs=[c for c in cases if c['engine']==e and c['model']==m];color=['#156e91','#b55d2d'][mi]
   for k,c in enumerate(cs):
    x=mi+(k-2)*.06;y=100*c['gains']['sequential_3nn'];same=c['same_configuration']['sequential_3nn'];ax.scatter([x],[y],s=32,facecolors='none' if same else color,edgecolors=color)
    if not (arms[c['case'],m]['stable'] and arms[c['case'],'sequential_3nn']['stable']):ax.scatter([x],[y],s=65,marker='x',color='black')
  ax.axhline(0,color='gray',lw=.8);ax.axhline(10,color='gray',lw=.8,ls=':');ax.set_xticks([0,1],['SmolLM3-3B','Qwen3-8B']);ax.set_title(e);ax.set_ylabel('Gain vs sequential 3NN (%)');ax.grid(axis='y',alpha=.2)
 fig.text(.5,.075,'Hollow: same configuration as sequential. Black cross: unstable comparison. Dotted line: 10% margin.',ha='center',fontsize=8)
 fig.suptitle('Real-input application workloads: fresh validation\nFive seeds per family; positive values favor the local model',fontsize=11);fig.savefig(O/'paired_gains.png',dpi=160,metadata={'Software':'V168'});fig.savefig(O/'paired_gains.svg',metadata={'Date':None});plt.close(fig)
 text=['# V168: paired Polars and XGBoost study','','Prospective paired development comparison on two additional native implementations. Polars reuses a flight workload previously exposed with DuckDB; XGBoost uses real Covertype data. Feasibility exposed both tasks. This is not independent production or unseen-system router validation.','','800 new configuration outcomes, 1600 query/training executions, 70 logical B20 arms (10 shared prefix +7 search +3 fresh validation), five fixed seeds per application. Model calls use the two existing pinned local quantized models.','','## Fresh validation results','','Positive gain favors the model. Quality utility uses actual runtime when valid; XGBoost accuracy below75% receives the frozen60-second penalty. Robust joint win requires >10% improvement over sequential, adaptive and GP-EI, different setting IDs, all quality-valid, MAD<=5% and medians>=10ms. All unfiltered gains remain included.','','| Application | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins |','|---|---|---:|---:|---:|---:|']
 for e in ENGINES:
  for m in MODELS:
   cs=[c for c in cases if c['engine']==e and c['model']==m];gg=[100*statistics.mean(c['gains'][b] for c in cs) for b in ['sequential_3nn','adaptive_neighbor','gp_ei']];text.append(f"| {e} | {m} | {gg[0]:+.3f}% | {gg[1]:+.3f}% | {gg[2]:+.3f}% | {sum(c['joint_robust_win'] for c in cs)}/5 |")
 text+=['',f"Quality-valid acquisitions: {native['quality_feasible']}/800; penalties: {native['quality_penalties']}. Minimum acquired XGBoost accuracy: {100*native['minimum_xgboost_accuracy']:.3f}%. Unstable validation cells: {sum(not a['stable'] for a in arms.values())}/70. Below10ms: {sum(not a['above_floor'] for a in arms.values())}/70. Same configuration as sequential: {sum(c['same_configuration']['sequential_3nn'] for c in cases)}/20. These flags do not exclude cases from means.",'','## Frozen routing policies','','Benefit/uncertainty thresholds were transported unchanged from historical development groups. No refitting on these outcomes. Hindsight is a non-deployable reference; BORA/rank are checkpoint adaptations, not full original implementations.','','| Model | Policy | Calls / 10 | Equal-family mean gain vs never |','|---|---|---:|---:|']
 for p in policies:text.append(f"| {p['model']} | {p['policy']} | {p['calls_or_expected_calls']:.2f} | {100*p['equal_group_mean_gain']:+.3f}% |")
 text+=['','## Actual research cost and deployment estimates','',f"Native collection: {native['subprocess_collection_seconds']:.3f} subprocess-seconds including {native['native_objective_seconds']:.3f} objective-seconds. End-to-end paired collection {native['end_to_end_seconds']:.3f}s. Earlier source/preparation work and60feasibility attempts (including20failed Polars attempts) are additional costs. No paid/cloud requests.",'']
 for m,v in modelcost.items():
  l=v['ledger'];text.append(f"- {m}: {l['generation_requests']} starts, {v['responses']} responses; observed input/output tokens {v['observed_usage']['tokens_evaluated']}/{v['observed_usage']['tokens_predicted']}; unknown usage {v['unknown_usage_requests']}; requests {v['request_wall_seconds']:.3f}s; entire model stage {l['stage_seconds']:.3f}s; peak RSS {l['peak_server_rss_bytes']}bytes; server exit {l['server_exit_code']}.")
 text+=['','One selected deployment branch per case would use200configuration outcomes and400query/training executions across ten cases. comparison.json estimates time by selecting recorded prefix/branch/request costs. This is a retrospective proxy, not an actual deployment; cold model startup is separate. Actual study collection includes every counterfactual branch and therefore costs more.','','## Limitations','','Two software implementations, one host, five seeds each. Repeated seeds are not independent systems. Polars shares its data/query contract with earlier DuckDB work. XGBoost quality-validation labels constrain optimization, not classifier-generalization evaluation. Native threading, warmed filesystem caches, constrained proposals, projection, fixed seeds, small finite grids and quantized models limit scope. Historical router calibration used a different budget/target and may not transfer. Quality penalties alter the loss distribution. No journal quartile or population-level benefit follows from these measurements. Both applications are development-exposed for future work.','','All failed V166 Polars attempts remain visible. V167 repaired only NA null parsing under a new freeze; no threshold or workload was selected by LLM benefit. Source provenance and admission reports: reports/protocol_v166.md, reports/feasibility_v166.md, reports/feasibility_v167.md. Frozen V168 code, prompts, prefixes, models and router decisions: artifacts/study_v168. All native records and validations: results/v168_native; real model requests/responses/costs: results/v168_models. Safe report replay: .venv/bin/python scripts/report_apps_v168.py.']
 (ROOT/'reports/apps_v168.md').write_text('\n'.join(text)+'\n');print(json.dumps({'collection':native,'joint_robust_wins':{m:sum(c['joint_robust_win'] for c in cases if c['model']==m) for m in MODELS},'models':modelcost},indent=2))
if __name__=='__main__':main()
