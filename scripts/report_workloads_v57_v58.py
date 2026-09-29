"""Render completed V57/V58 evidence; no new measurements or objective queries."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'artifacts/.mpl_cache'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'artifacts/.font_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def read(p):return json.loads(p.read_text())
def main():
    out=ROOT/'results/v57_workload_matrix';rows=read(out/'all_cases.json');summary=read(out/'summary.json')
    s58=read(ROOT/'results/v58_order_sensitivity/summary.json');cases=read(ROOT/'results/v58_order_sensitivity/cases.json')
    groups=[];projection=0
    for w in summary['workloads']:
        group=[r for r in rows if r['family']==w['family'] and r['workload']==w['workload']]
        reference=[r['wall_seconds'] for r in group if r['round'] in [0,2] and r['status']=='valid']
        estimate=statistics.median(reference)*144 if len(reference)==2 else None
        if w['admitted']:projection+=estimate
        groups.append({**w,'wall_seconds':[r['wall_seconds'] for r in group],'final_java_ms':[r.get('final_ms') for r in group],
                       'reference_projection_144_seconds':estimate,'projection_is_a_guarantee':False,'all_timeout_cap_scenario_144_seconds':(60 if w['family']=='javagc' else 30)*144})
    (out/'capacity_estimates.json').write_text(json.dumps({'admitted_workload_reference_projection_seconds':projection,'workloads':groups,'scope':'Illustrative extrapolation from two repeated reference trials, not an observed full grid or runtime bound'},indent=2)+'\n')
    with (out/'workloads.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['family','workload','admitted','valid','reference_wall_0','contrast_wall','reference_wall_2','reference_projection_144_seconds'])
        for w in groups:writer.writerow([w['family'],w['workload'],w['admitted'],w['valid'],*w['wall_seconds'],w['reference_projection_144_seconds']])
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
    fig,ax=plt.subplots(figsize=(10,4.5));xs=np.arange(5)
    for rep,label,color in [(0,'Reference 1','#316b9b'),(1,'Contrast','#b87425'),(2,'Reference 2','#55977f')]:
        values=[w['wall_seconds'][rep] for w in groups]
        ax.bar(xs+(rep-1)*.24,values,.23,label=label,color=color)
        for j,w in enumerate(groups):
            row=next(r for r in rows if r['workload']==w['workload'] and r['round']==rep)
            if row['status']!='valid':ax.scatter(j+(rep-1)*.24,values[j],marker='x',color='black',s=55,zorder=5)
    ax.set(yscale='log',xticks=xs,xticklabels=['Xalan\nsmall','Planning\np01','Xalan\nlarge','Planning\np10','Planning\np20'],ylabel='Whole-process exit-based wall seconds',title='Five preselected workloads: 12 valid runs, 3 CPU timeouts')
    ax.legend(ncol=3,fontsize=9);fig.text(.5,.02,'Black crosses: failed runs, not valid solutions. Three runs per workload; two software families.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,1));fig.savefig(out/'workload_feasibility.png',dpi=170);fig.savefig(out/'workload_feasibility.svg');plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(11,4.7))
    rng=np.random.default_rng(58000)
    for ax,f in zip(axs,s58['families']):
        group=[c for c in cases if c['family']==f['family']]
        for i,m in enumerate(['prefix','random','nn','rf_lcb']):
            values=[c['headroom_percent'][m] for c in group]
            ax.scatter(i+rng.uniform(-.13,.13,len(values)),values,s=12,alpha=.45,color=['#888','#b87425','#316b9b','#55977f'][i])
            ax.plot([i-.22,i+.22],[statistics.median(values)]*2,color='black',lw=2)
        ax.axhline(f['threshold_percent'],ls=':',color='#a24747',label='Original gate threshold')
        ax.set(xticks=range(4),xticklabels=['Prefix10','Random20','3NN20','RF-LCB20'],ylabel='Headroom to best recorded median (%)',title='Java / default' if f['family']=='javagc' else 'Planning / p05',yscale='symlog',ylim=(-.1,75 if f['family']=='fastdownward' else 12))
        ticks=[0,1,5,10,50] if f['family']=='fastdownward' else [0,.5,1,5,10]
        ax.set_yticks(ticks);ax.set_yticklabels([str(t) for t in ticks])
        ax.set_ylabel('Headroom to best recorded median (%)\nSymmetric-log scale')
        ax.legend(fontsize=8)
    fig.suptitle('ID-order sensitivity: poor prefixes can recover through cheap continuation')
    fig.text(.5,.02,'100 dependent cases per family (20 ID orders × 5 seeds). Exposed tables; no new physical trials or LLM calls.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,.95));dest=ROOT/'results/v58_order_sensitivity'
    fig.savefig(dest/'order_sensitivity.png',dpi=170);fig.savefig(dest/'order_sensitivity.svg');plt.close(fig)
    wrows='\n'.join(f"| {w['family']} / {w['workload']} | {w['valid']}/3 | {' / '.join(f'{v:.3f}' for v in w['wall_seconds'])} | {', '.join(w['costs']) or '—'} | {'Yes' if w['admitted'] else 'No'} |" for w in groups)
    sr='\n'.join(f"| {f['family']} | {f['methods']['prefix']['max_headroom_percent']:.3f}% | {f['methods']['prefix']['threshold_crossings']}/100 | {f['methods']['rf_lcb']['exact_minimum_count']}/100 | {f['portfolio_max_headroom_percent']:.3f}% | {f['permutations_passing_gate']}/20 |" for f in s58['families'])
    text=f'''# V57/V58 — broader workloads and a stronger order-sensitivity check

Two completed experiments, local only, 2026-09-25. **Four of five preselected
workloads passed admission.** A retrospective robustness study also found that poor
ten-evaluation prefixes can recover with cheap continuation: planning RF-LCB reaches
the best recorded result in100/100 ID-permuted cases. This is not new LLM evidence.

## Broader physical workload matrix (V57)

Selected Xalan's released non-default sizes and the first/lower-middle/last task
from the pinned20-task planning suite before new timings. All15 intended invocations
ran;12 valid,3 CPU-limit failures,0 dropped/unattempted/retried. Stage
{summary['stage_seconds']:.6f}s. Six JVM invocations include six warmups and six timed
iterations. Nine planner invocations, six independently valid plans. Same owner
versions/hardware as V53/V55, no new models/runtimes. All five workloads remain in
the denominator; they form TWO software families, not five independent systems.

| Family / workload | Valid | Reference / contrast / repeat wall seconds | Plan cost | Admitted |
|---|---:|---|---|---|
{wrows}

Xalan actual final outputs match precomputed reference hashes:2,390,100bytes small,
239,010,000bytes large. These reference hashes were derived before execution from
100 identical batches in the retained real V53 output; no generated stream is
reported as a measured result. First new actual output per size is retained; later
validated scratch is removed with hashes retained. Warmup gets owner validation,
not separate byte equality. Equivalence is to released implementation, not a formal
XSLT correctness proof. All new valid planning plans have independently recomputed
cost105 (not old p05's104). Validator remains a limited independent subset checker;
external VAL and an independent optimality certificate remain untested.

A lead worth replication: p10's hmax contrast completed in4.123s, versus two lmcut
references6.283/5.846s; old p05 had the opposite ordering. This is ONE contrast,
not a statistically established speedup, configuration optimum or LLM opportunity.
Xalan small also shows timing variation; no policy was selected from these15runs.
p20 timed out on all three attempts with owner exit23; its absence of a completed
reference prevents admission, not evidence that the task is unsolvable.

![Actual workload matrix](../results/v57_workload_matrix/workload_feasibility.png)

New timestamping uses a blocking process-exit waiter, independently of0.1s memory
watchdog polls. Both timings retained; it removes the old polling-interval rounding
but still includes process startup/monitor interference. Do not pool changed outer
wall timings with old protocols as if identical instruments. Memory cap is sampled
RSS2GiB, not a hard macOS allocation cap. Total scratch cap2GiB; per-JVM60s wall,
per-planner30s wall/27s CPU; stage750s. No cap increased during execution.

## Retrospective ID-order sensitivity (V58)

Used existing V54 Java/default and V56 planning/p05 tables, no physical reruns.
Twenty seeded ID permutations per family × five seeds =200dependent cases,
600 actual recorded-data arms,8,000 charged aggregate-vector acquisitions. Physical
initial four settings are held fixed under relabeling. Same encoders/3NN/RF-LCB
parameters; each arm uses20 inclusive outcomes from its shared10 prefix. No tuning.
Collection{s58['collection']['runtime_seconds']:.6f}s, complete. Full-table scoring
runs only after choices are saved. This is exposed development data, not confirmation.

| Family | Worst prefix headroom | Prefixes crossing threshold | RF exact recorded minimum | Worst portfolio headroom | Permutations passing gate |
|---|---:|---:|---:|---:|---:|
{sr}

**Qualification to V56:** the original ordering's nearly-optimal ten-label prefix
is not robust to arbitrary ID order. Five planning cases have poor prefixes, with
worst remaining headroom63.487%. Nevertheless, RF-LCB recovers the best recorded
planning result in all100 cases; no final classical arm crosses its5% opportunity
threshold. Java's largest final-arm headroom is1.263%, below its9.476% noise-aware
threshold. Both original final headroom decisions survive every tested permutation.
Thus poor current progress alone does not establish a need for an LLM; further
cheap search can recover. This observation is conditional on these finite tables,
these budgets/controls and the sampled orderings. It is not a general theorem.

![Saved-table order diagnostic](../results/v58_order_sensitivity/order_sensitivity.png)

All acquisition values map to source rows; shared prefixes/20budgets/8000charges
verified. Independent replay reconstructs7,200 recommendations from each own acquired
state, including RF fits. This costs replay compute, not new objective acquisition.
100cases are not100software systems; no population p-values or held-out learning claim.
The recorded minimum is noise-sensitive and not a certified physical optimum.

## Resources and next concrete experiment

Reference-wall extrapolation for48×3measurements on all four admitted workloads is
**{projection/60:.1f}minutes**. This is an illustrative cost projection, not a bound:
two tested configurations cannot predict a full grid. It exceeds the current
30-minute default; the larger Xalan workload alone drives much of that estimate.
p20 remains explicitly unadmitted with a separate timeout-cap scenario in
capacity_estimates.json; it is not silently dropped to claim a representative suite.

A concrete, frozen V59 collector and offline screen are prepared for all four
admitted workloads:576physical invocations,60classical arms,800recorded acquisitions,
up to120minutes local collection, zero model calls/downloads/spending. Authorization
is FALSE and the guard was exercised before any workload process/output directory.
Approval must bind reports/protocol_v59_workload_screen.freeze.json and the exact
resource envelope; generic continuation is not treated as an increased runtime cap.
The collector may still stop incomplete at its cap. V59 has NOT run.

Completed costs:15new physical invocations;8000new recorded accesses;0LLM requests,
0new runtime/model downloads, USD0 new external spend. Source downloads:three pinned
PDDL files34,033bytes. Actual collection includes failures, repeats and warmups;
replay costs are separate. Electricity/agent/user time unknown. V57 admission probes
are real prior cost, not free initialization in a later20-outcome arm.

Primary data/source identities: artifacts/sources/v57/manifest.json and
artifacts/study_v57/workload_metadata.json. Runtime/source audit fromV53/V55 remains
applicable. New PDDL redistribution permission unresolved, sources local only.
V57freeze349inputs; V58freeze9inputs; V59 prepared freeze358inputs. Raw logs/results:
results/v57_workload_matrix/, results/v58_order_sensitivity/. Verification receipts:
artifacts/study_v57/, artifacts/study_v58/. STATUS contains resume instructions.

Safe commands (no application/model reruns):

```sh
.venv/bin/python scripts/verify_workload_matrix_v57.py
.venv/bin/python scripts/verify_order_choices_v58.py
.venv/bin/python scripts/report_workloads_v57_v58.py
.venv/bin/python -m pytest -q tests
```

The primary collectors/analyzer are one-shot. These results improve measurement and
robustness evidence, but do not establish useful LLM routing, enough independent
families, novelty or Q2 readiness. No publication, push, cloud resource or author
contact occurred. Next action is approval of the bounded V59 local runtime extension.
'''
    (ROOT/'reports/workloads_v57_v58.md').write_text(text)
    print(json.dumps({'admitted_projection_seconds':projection,'report':'reports/workloads_v57_v58.md'},indent=2))
if __name__=='__main__':main()
