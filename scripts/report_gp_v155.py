"""Complete-denominator comparison with independently acquired GP-EI branches."""
import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v155';O=ROOT/'results/v155_gp'
def read(p):return json.loads(p.read_text())
def main():
 rows=read(ROOT/'artifacts/study_v151/inputs.json')['rows'];jobs=read(A/'jobs.json');completion=read(O/'completion.json');arms={j['key']:read(O/'arms'/(j['key']+'.json')) for j in jobs};events=[json.loads(x) for x in (O/'acquisitions.jsonl').read_text().splitlines()];cases=[];summary={}
 for grouping in ['ecosystem','engine']:
  summary[grouping]={}
  for length in ['1.0','0.2']:
   summary[grouping][length]={}
   for model in ['smollm3_3b','qwen3_8b']:
    data=[]
    for r in rows:
     if r['model']!=model:continue
     arm=arms[r['key']+'::gp_'+length];group='spark_hadoop_ecosystem' if grouping=='ecosystem' and r['group'] in ['spark','hadoop_mapreduce'] else r['group'];sign=1 if r['direction']=='minimize' else -1;gp=arm['target'];gain=None if gp is None else sign*(gp-r['target'])/gp
     data.append({'key':r['key'],'group':group,'model':model,'kernel_length':length,'gp_status':arm['status'],'gp_target':gp,'llm_target':r['target'],'gain_vs_gp':gain,'gain_vs_adaptive':r['adaptive_gain'],'gp_gain_vs_sequential':None if gp is None else sign*(r['sequential']-gp)/r['sequential'],'gp_gain_vs_adaptive':None if gp is None else sign*(r['adaptive']-gp)/r['adaptive'],'fallback':r['fallback']})
    gs=[]
    for g in sorted({r['group'] for r in data}):
     rr=[r for r in data if r['group']==g];valid=[r for r in rr if r['gain_vs_gp'] is not None];full=len(valid)==len(rr)
     gs.append({'group':g,'intended':len(rr),'scorable':len(valid),'mean_gain':statistics.mean(r['gain_vs_gp'] for r in valid) if full else None,'gp_gain_vs_sequential':statistics.mean(r['gp_gain_vs_sequential'] for r in valid) if full else None,'gp_gain_vs_adaptive':statistics.mean(r['gp_gain_vs_adaptive'] for r in valid) if full else None,'useful':sum(r['gain_vs_gp']>.01 for r in valid),'harmful':sum(r['gain_vs_gp']<-.01 for r in valid),'joint_useful':sum(r['gain_vs_gp']>.01 and r['gain_vs_adaptive']>.01 for r in valid)})
    full=all(g['mean_gain'] is not None for g in gs);summary[grouping][length][model]={'intended':70,'scorable':sum(g['scorable'] for g in gs),'family_mean_gain':statistics.mean(g['mean_gain'] for g in gs) if full else None,'gp_family_gain_vs_sequential':statistics.mean(g['gp_gain_vs_sequential'] for g in gs) if full else None,'gp_family_gain_vs_adaptive':statistics.mean(g['gp_gain_vs_adaptive'] for g in gs) if full else None,'useful':sum(g['useful'] for g in gs),'harmful':sum(g['harmful'] for g in gs),'joint_useful':sum(g['joint_useful'] for g in gs),'groups':gs}
    if grouping=='ecosystem':cases+=data
 result={'exploratory':True,'new_model_requests':0,'completion':completion,'invalid_source_attempts':sum(e['status']=='invalid_source' for e in events),'failure_penalty_attempts':sum(e['status']=='incomplete_failure_penalty' for e in events),'unique_source_rows_acquired':len({(e.get('source'),e.get('source_line')) for e in events if e['status']!='invalid_source'}),'cases':cases,'summary':summary};(O/'comparison.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 lines=['# V155: GP expected-improvement continuation benchmark','','New real recorded-data acquisition, not new model inference or native software execution. Seventy saved B10prefixes ×two predeclared fixed kernels; same ten remaining labels per completed arm. No model prompt, response or branch was changed. Hyperparameters were not tuned to these outcomes. This is a bounded GP-EI comparator, not full BORA/LB-MCTS replication.','',f"**{completion['complete_arms']}/140arms complete**, {completion['unscorable_arms']}unscorable, {completion['acquisition_attempts']}charged attempts in{completion['wall_seconds']:.3f}seconds/600secondcap. No retries or new LLMrequests. One Spark TPCH/seed11/length0.2 arm selected an empty source duration on its third acquisition. That failed attempt is charged; seven later slots remain unattempted, not fabricated. The existing missing source is not repaired by inventing runtime. All70primary-length arms are complete; sensitivity has69/70, so its full-cohort mean remains null.",'',
 '| Grouping / length / model | Scorable /70 | Mean LLM gain vs GP | Useful / harmful >1% | Joint wins vs GP+adaptive | GP gain vs sequential | GP gain vs adaptive |','|---|---:|---:|---|---:|---:|---:|']
 fmt=lambda v:'unscorable' if v is None else f'{100*v:+.4f}%'
 for grouping,ls in summary.items():
  for length,models in ls.items():
   for m,s in models.items():lines.append(f"| {grouping} / {length} / {m} | {s['scorable']} | {fmt(s['family_mean_gain'])} | {s['useful']}/{s['harmful']} | {s['joint_useful']} | {fmt(s['gp_family_gain_vs_sequential'])} | {fmt(s['gp_family_gain_vs_adaptive'])} |")
 lines+=['','## Primary kernel: group detail','','| Ecosystem / model | Cases | LLM gain vs GP | Useful / harmful | Joint useful |','|---|---:|---:|---|---:|']
 for m,s in summary['ecosystem']['1.0'].items():
  for g in s['groups']:lines.append(f"| {g['group']} / {m} | {g['scorable']}/{g['intended']} | {fmt(g['mean_gain'])} | {g['useful']}/{g['harmful']} | {g['joint_useful']} |")
 lines+=['','All five seeds and workload variants remain in the same software/ ecosystem group. Seven-ecosystem summaries are primary; eight-engine grouping is a sensitivity. No population significance, equivalence, independent new-family transfer or journal-readiness claim. A changed classical counterfactual can expose different model opportunities; controllers trained against sequential gains must not be presented as trained GP-benefit predictors. Both kernel settings remain visible, including the missing sensitivity comparison.','',f"{result['failure_penalty_attempts']}acquisitions use the already declared Hadoop7200failurepenalty; these are utility scores, not measured failure durations. {result['unique_source_rows_acquired']}distinct valid source records were acquired; repeated requests across arms are independently charged. Raw receipts and saved choices preserve all1393attempts. Historical two-model calls/costs are reused, not zero-cost original collection. Deployment B20 uses one chosen continuation; research collected both kernel branches plus all prior paired data.",'',
 'Evidence: frozen code/protocol/source/prefix hashes, precollectiontests, feature-only EI selection logs, separate charged oracle journal, all arm states/errors, complete denominator and regenerable tables/figure. GP uses fixed mixed covariance, acquired-label-only normalization, and latent predictive uncertainty; no hidden target enters selection. Existing recorded-data correctness/noise and model-projection limitations persist.']
 (ROOT/'reports/gp_v155.md').write_text('\n'.join(lines)+'\n')
 import matplotlib
 matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v155'
 import matplotlib.pyplot as plt
 names=[g['group'] for g in summary['ecosystem']['1.0']['smollm3_3b']['groups']];fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
 for k,(m,label) in enumerate([('smollm3_3b','SmolLM3-3B'),('qwen3_8b','Qwen3-8B')]):ax.bar([i+(k-.5)*.38 for i in range(len(names))],[100*g['mean_gain'] for g in summary['ecosystem']['1.0'][m]['groups']],.38,label=label)
 ax.set_xticks(range(len(names)),names,rotation=20,ha='right');ax.set_ylabel('Mean LLM gain over GP-EI (%)');ax.axhline(0,color='black',lw=.8);ax.grid(axis='y',alpha=.2);ax.legend();ax.set_title('Paired B10→B20 continuations • primary fixed kernel\nNew GP acquisitions, existing real model responses; exploratory')
 fig.savefig(O/'comparison.png',dpi=150);fig.savefig(O/'comparison.svg',metadata={'Date':None});plt.close(fig)
 print(json.dumps(summary['ecosystem']['1.0'],indent=2))
if __name__=='__main__':main()
