"""Post-collection descriptive reporting; reads only already acquired outcomes."""
import json
from fractions import Fraction
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v148';O=ROOT/'results/v148_hadoop'
MODELS=['smollm3_3b','qwen3_8b'];APPS=['pagerank','terasort','wordcount'];CONTROLS=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal']
def read(p):return json.loads(Path(p).read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+'\n')
def gain(a,b):return float((Fraction(str(a))-Fraction(str(b)))/Fraction(str(a)))
def stats(values):return {'n':len(values),'mean_gain':mean(values),'wins':sum(x>0 for x in values),'ties':sum(x==0 for x in values),'losses':sum(x<0 for x in values),'practical_wins':sum(x>.01 for x in values),'practical_harms':sum(x<-.01 for x in values)}
def main():
    complete=read(O/'completion.json');assert complete['total_acquisitions']==1200
    jobs=read(A/'jobs.json');decisions=read(A/'decisions.json')['rows'];cases=[];summaries={}
    for m in MODELS:
        for j in jobs:
            arm=read(O/'models'/f"{m}_{j['key']}.json");controls={k:read(O/'classical'/f"{j['key']}_{k}.json") for k in CONTROLS};prefix=read(ROOT/j['prefix']);dec=next(d for d in decisions if d['model']==m and d['key']==j['key'])
            gs={k:gain(v['target'],arm['target']) for k,v in controls.items()}
            policy={'never':False,'always':True,**{p:dec[p] for p in ['benefit','uncertainty','random_development_rate','random_matched_rate','benefit_80pct','uncertainty_80pct']}}
            cases.append({'key':j['key'],'app':j['app'],'seed':j['seed'],'model':m,'target':arm['target'],'prefix_best':min(x[0] for x in prefix['labels']),
                          'references':{k:v['target'] for k,v in controls.items()},'gains':gs,'fallback':arm['fallback'],'status':arm['status'],'policies':policy,'support_extrapolation':dec['outside_training_range']})
        rs=[r for r in cases if r['model']==m];contrasts={k:stats([r['gains'][k] for r in rs]) for k in CONTROLS};policies={}
        for p in rs[0]['policies']:
            chosen=[r for r in rs if r['policies'][p]];g=[r['gains']['sequential_3nn'] if r['policies'][p] else 0. for r in rs]
            policies[p]={**stats(g),'calls':len(chosen),'missed_useful_calls':sum(not r['policies'][p] and r['gains']['sequential_3nn']>.01 for r in rs),
                         'harmful_calls':sum(r['gains']['sequential_3nn']<-.01 for r in chosen),'joint_useful_calls':sum(r['gains']['sequential_3nn']>.01 and r['gains']['adaptive_neighbor']>.01 for r in chosen),
                         'matched_random_expected_gain':len(chosen)/15*contrasts['sequential_3nn']['mean_gain'],
                         'mean_gain_vs_adaptive':mean(r['gains']['adaptive_neighbor'] if r['policies'][p] else gain(r['references']['adaptive_neighbor'],r['references']['sequential_3nn']) for r in rs)}
        base=ROOT/'results/v148_models'/m;ledger=read(base/'ledger.json');responses=[json.loads(s) for s in (base/'responses.jsonl').read_text().splitlines()];diags=[d for j in jobs for d in read(O/'models'/f"{m}_{j['key']}.json")['projection']]
        cost={'request_starts':ledger['generation_requests'],'responses':len(responses),'unattempted':15-ledger['generation_requests'],'unknown_usage_requests':ledger['generation_requests']-len(responses)+sum(type(r['response'].get('tokens_predicted')) is not int or type(r['response'].get('tokens_evaluated')) is not int for r in responses),
              'generated_tokens_lower_bound':sum(r['response'].get('tokens_predicted',0) for r in responses),'prefill_tokens_lower_bound':sum(r['response'].get('tokens_evaluated',0) for r in responses),
              'allocated_output_tokens':ledger['allocated_output_tokens'],'lifecycle_seconds':ledger['stage_seconds'],'startup_seconds':ledger.get('startup_seconds'), 'request_seconds':sum(r['wall_seconds'] for r in responses),'peak_server_rss_bytes':ledger['peak_server_rss_bytes'],'retries':ledger['retries'],'server_exit_code':ledger['server_exit_code']}
        summaries[m]={'contrasts':contrasts,'policies':policies,'workloads':{app:{k:stats([r['gains'][k] for r in rs if r['app']==app]) for k in CONTROLS} for app in APPS},
                      'joint_practical_wins':sum(r['gains']['sequential_3nn']>.01 and r['gains']['adaptive_neighbor']>.01 for r in rs),'prefix_improvements':sum(r['target']<r['prefix_best'] for r in rs),'fallbacks':sum(r['fallback'] for r in rs),
                      'hindsight_oracle_gain':mean(max(0,r['gains']['sequential_3nn']) for r in rs),'support_extrapolating_cases':sum(bool(r['support_extrapolation']) for r in rs),
                      'projection':{'proposals':len(diags),'nonzero_distance':sum(d['distance']>0 for d in diags),'repeated_prototypes':sum(d['repeated_proposal'] for d in diags),'matches_prefix':sum(d['matches_prefix'] for d in diags)},'cost':cost}
    events=[json.loads(s) for s in (O/'acquisitions.jsonl').read_text().splitlines()];counts={s:sum(e['status']==s for e in events) for s in sorted({e['status'] for e in events})}
    result={'scope':'One prospective Hadoop MapReduce family; cloud-configuration adaptation; three bigdata tasks, five seeds each','models':summaries,'cases':cases,'collection':complete,
            'acquisition_status_counts':counts,'unique_source_records_acquired':len({e['source'] for e in events}),'unique_incomplete_source_records':len({e['source'] for e in events if e['status']=='incomplete_failure_penalty'})}
    write(O/'comparison.json',result)
    lines=['# V148: new Hadoop family, frozen local-model transfer test','',result['scope']+'. This is one independent execution-engine group, not three independent systems, and shares the Hadoop/Spark ecosystem. No new Hadoop cluster jobs or cloud spending occurred.','',
           f"Executed {sum(s['cost']['request_starts'] for s in summaries.values())} real local generation starts, {sum(s['cost']['responses'] for s in summaries.values())} returned responses, 105 B20arms from15shared B10prefixes and1200charged recorded outcomes. Collection{complete['total_collection_seconds']:.3f}s /1800s. Acquired {result['unique_source_records_acquired']} distinct source records. Status counts:{counts}; unique incomplete records{result['unique_incomplete_source_records']}. Repeated rows across isolated arms still incur separate logical charges.",'',
           'Primary score is completed elapsed seconds capped at7200, or an explicit7200failure penalty for incomplete source runs. A penalty is **not measured runtime** and does not identify the failure cause. All intended cases and failures remain. No imputation/filtering, new target normalization or post-outcome threshold changes. The classical completion gate passed before inference.','',
           '| Model | Gain vs sequential | W/T/L | Gain vs adaptive | W/T/L | >1% win over both /15 |','|---|---:|---|---:|---|---:|']
    for m,s in summaries.items():
        q=s['contrasts']['sequential_3nn'];a=s['contrasts']['adaptive_neighbor'];lines.append(f"| {m} | {100*q['mean_gain']:+.4f}% | {q['wins']}/{q['ties']}/{q['losses']} | {100*a['mean_gain']:+.4f}% | {a['wins']}/{a['ties']}/{a['losses']} | {s['joint_practical_wins']} |")
    lines+=['','Positive favors the model. Means give the three workloads equal weight (five seeds each); they are descriptive within one family. No confidence interval over independent seeds or journal-readiness claim.','',
            '| Model / workload | Sequential gain | Adaptive gain | Random-prototype gain |','|---|---:|---:|---:|']
    for m,s in summaries.items():
        for app,x in s['workloads'].items():lines.append('| '+m+' / '+app+' | '+' | '.join(f"{100*x[k]['mean_gain']:+.4f}%" for k in ['sequential_3nn','adaptive_neighbor','random_proposal'])+' |')
    lines+=['','## Frozen routing and reliability','',
            'Routers were trained on the seven V147 development families and frozen before Hadoop acquisition. All workload variants/seeds stay in the new Hadoop group. Learned thresholds and fixed development80th-percentile diagnostics use no Hadoop outcome. Random matched-rate calls were selected before continuations; expected matched-random gains are descriptive after scoring.','',
            '| Model / policy | Calls /15 | Mean gain vs sequential | >1% harmful calls | Missed >1% wins | Joint useful calls |','|---|---:|---:|---:|---:|---:|']
    for m,s in summaries.items():
        for p,x in s['policies'].items():lines.append(f"| {m} / {p} | {x['calls']} | {100*x['mean_gain']:+.4f}% | {x['harmful_calls']} | {x['missed_useful_calls']} | {x['joint_useful_calls']} |")
        lines+=['',f"{m}: prefix improvements{s['prefix_improvements']}/15; fallbacks{s['fallbacks']}/15; hindsight oracle gain{100*s['hindsight_oracle_gain']:.4f}% (non-deployable). Feature-support extrapolation{s['support_extrapolating_cases']}/15. Projection:{s['projection']}.",'']
    lines+=['## Actual collection and deployment estimates','']
    for m,s in summaries.items():lines.append(m+': '+json.dumps(s['cost'],sort_keys=True)+'.')
    lines+=['','Actual1200charges comprise150prefix,750classical and300model/fallback acquisitions; all30model intents and both model startups belong to collection cost. Deploying one policy would use20total objective evaluations per case and at mostone model request after B10. Startup amortization, native measurement costs, energy and cloud-dollar costs are not estimated. Recorded author-run cloud experiments are not free historical computation, but our local query time is not their native execution time. Model blocks/templates differ, so timings are descriptive.','',
            '## Source and scope limits','',
            'Scout data revision e0dfc3a7d08ec4d441578565c0b7d4b24e56d5cb, MIT; original paper and linked measurement code checked in source_audit_v146.md. Variables are cluster VM count and nine VM types, extending software-configuration optimization to deployment resources. Utility is capped completion time, not economic cost; a larger cluster can consume more resources. Source Hadoop2.7 patch/binary identity, correctness, single-measurement noise and benchmark contamination remain unverified. Nominal bigdata class is fixed; reported input bytes vary slightly for PageRank/Wordcount and are not certified identical. Telemetry is excluded. These limits restrict a practical-system or generalization claim.','',
            'Reproduce the report with `MPLCONFIGDIR=/tmp/mpl-v148 .venv/bin/python scripts/report_hadoop_v148.py`; independent replay: `.venv/bin/python scripts/verify_hadoop_v148.py`. Do not rerun create-once collection. Raw responses/starts/preflight/runtime logs are in results/v148_models; every charged raw record and arm is in results/v148_hadoop; frozen candidates, prefixes, prompts, model manifests and router decisions are in artifacts/study_v148.']
    (ROOT/'reports/hadoop_v148.md').write_text('\n'.join(lines)+'\n')
    import matplotlib;matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v148'
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.5),layout='constrained')
    for ax,ref in zip(axes,['sequential_3nn','adaptive_neighbor']):
        for i,m in enumerate(MODELS):ax.bar([j+(i-.5)*.35 for j in range(3)],[100*summaries[m]['workloads'][app][ref]['mean_gain'] for app in APPS],.35,label=m)
        ax.axhline(0,color='black',lw=.8);ax.set_xticks(range(3),APPS);ax.set_ylabel('Mean relative gain in capped score (%)');ax.set_title('Versus '+ref);ax.grid(axis='y',alpha=.2)
    axes[0].legend(fontsize=8);fig.suptitle('One new Hadoop family • three workloads × five seeds\nReal local models; fixed capped-time / failure-penalty objective')
    fig.savefig(O/'comparison.png',dpi=160);fig.savefig(O/'comparison.svg',metadata={'Date':None});plt.close(fig)
    print(json.dumps({m:{'contrasts':s['contrasts'],'joint_wins':s['joint_practical_wins'],'cost':s['cost']} for m,s in summaries.items()},indent=2))
if __name__=='__main__':main()
