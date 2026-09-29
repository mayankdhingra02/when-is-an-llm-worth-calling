"""Regenerate V59 scientific tables/figures/report from completed measured records."""
import collections,csv,json,os,statistics
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
    physical=ROOT/'results/v59_workload_physical';out=ROOT/'results/v59_workload_screen'
    raw=read(physical/'all_cases.json');p=read(physical/'summary.json');assert p['complete_table']
    s=read(out/'summary.json');verified=read(ROOT/'artifacts/study_v59/verification.json');assert verified['verified']
    stats=[]
    for w in s['workloads']:
        key=w['family']+'/'+w['workload'];folder=out/f"{w['family']}_{w['workload']}";table=read(folder/'table.json')
        rows=[r for r in raw if (r['family'],r['workload'])==(w['family'],w['workload'])]
        valid_cv=[r['cv'] for r in table if r['valid_repetitions']==3]
        item={**w,'valid_trials':sum(r['status']=='valid' for r in rows),'failed_trials':sum(r['status']!='valid' for r in rows),
              'median_valid_cv_percent':100*statistics.median(valid_cv) if valid_cv else None,
              'all_valid_settings':len(valid_cv),'max_sampled_rss_bytes':max(r['sampled_maxima'].get('rss_bytes',0) for r in rows),
              'exact_minimum_counts':{m:sum(c['best_ms'][m]==w['minimum_ms'] for c in w['cases']) for m in ['random','nn','rf_lcb']},
              'arm_headroom_percent':{m:[100*(c['best_ms'][m]-w['minimum_ms'])/c['best_ms'][m] for c in w['cases']] for m in ['random','nn','rf_lcb']},
              'prefix_headroom_percent':[100*(c['prefix_best_ms']-w['minimum_ms'])/c['prefix_best_ms'] for c in w['cases']]}
        stats.append(item)
        with (folder/'settings.csv').open('w') as f:
            writer=csv.writer(f);writer.writerow(['config_id','configuration','median_ms','valid_repetitions','cv'])
            for t in table:writer.writerow([t['config_id'],json.dumps(t['configuration']),t['median_ms'],t['valid_repetitions'],t['cv']])
    (out/'descriptive_summary.json').write_text(json.dumps(stats,indent=2)+'\n')
    with (out/'cases.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['family','workload','seed','prefix_best_ms','random_best_ms','nn_best_ms','rf_lcb_best_ms','portfolio_headroom_percent','gate_met'])
        for w in s['workloads']:
            for c in w['cases']:writer.writerow([w['family'],w['workload'],c['seed'],c['prefix_best_ms'],*[c['best_ms'][m] for m in ['random','nn','rf_lcb']],c['portfolio_headroom_percent'],c['gate_met']])
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(2,2,figsize=(11,7.4))
    for ax,w in zip(axs.flat,stats):
        folder=out/f"{w['family']}_{w['workload']}";table=read(folder/'table.json')
        for valid,label,marker,color in [(True,'3 valid repetitions','o','#2869a6'),(False,'Includes resource failure','x','#b44f3b')]:
            ts=[t for t in table if (t['valid_repetitions']==3)==valid]
            if ts:ax.scatter([t['config_id'] for t in ts],[t['median_ms']/1000 for t in ts],s=18,marker=marker,color=color,label=label)
        ax.set(yscale='log',xlabel='Fixed configuration ID',ylabel='Median objective seconds',title=f"{w['family']} / {w['workload']}: {w['valid_trials']}/144 valid")
        ax.legend(fontsize=8)
    fig.suptitle('Four-workload physical screen: fixed utility, retained failures')
    fig.text(.5,.015,'Java: final harness iteration. Planning: whole-process wall. Failure penalties are scores, not measured runtimes.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.95));fig.savefig(out/'physical_tables.png',dpi=170);fig.savefig(out/'physical_tables.svg');plt.close(fig)
    fig,axs=plt.subplots(2,2,figsize=(11,7.4))
    for ax,w in zip(axs.flat,stats):
        xs=range(5)
        for m,label,marker,color in [('prefix','Prefix10','o','#888'),('random','Random20','v','#bb852d'),('nn','3NN20','s','#2869a6'),('rf_lcb','RF-LCB20','^','#399166')]:
            vals=[c['prefix_best_ms'] if m=='prefix' else c['best_ms'][m] for c in w['cases']]
            ax.plot(xs,[100*(v-w['minimum_ms'])/v for v in vals],marker=marker,lw=1,color=color,label=label)
        if w['threshold_percent'] is not None:ax.axhline(w['threshold_percent'],ls=':',color='#994444',label='Frozen gate threshold')
        ax.set(xticks=list(xs),xticklabels=[str(c['seed']) for c in w['cases']],xlabel='Seed (not independent family)',ylabel='Headroom to recorded minimum (%)',title=w['family']+' / '+w['workload'])
        ax.legend(fontsize=7,ncol=2)
    fig.suptitle('Same ten-outcome prefix; 20-inclusive-outcome continuations')
    fig.text(.5,.015,'Four workloads are two software families. Minima/portfolio are hindsight references, not deployed policies.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.95));fig.savefig(out/'classical_headroom.png',dpi=170);fig.savefig(out/'classical_headroom.svg');plt.close(fig)
    def fmt(x):return 'undefined' if x is None else f'{x:.3f}'
    table_text='\n'.join(f"| {w['family']} / {w['workload']} | {w['valid_trials']}/144 | {w['minimum_ms']:.3f} | {fmt(w['median_valid_cv_percent'])}% | {fmt(w['threshold_percent'])}% | {w['gate_case_count']}/5 | {'PASS' if w['gate_passed'] else 'FAIL' if w['threshold_percent'] is not None else 'UNDEFINED'} |" for w in stats)
    counts='\n'.join(f"| {w['family']} / {w['workload']} | {w['exact_minimum_counts']['random']}/5 | {w['exact_minimum_counts']['nn']}/5 | {w['exact_minimum_counts']['rf_lcb']}/5 | {min(w['prefix_headroom_percent']):.3f}–{max(w['prefix_headroom_percent']):.3f}% |" for w in stats)
    remaining='\n'.join(f"| {w['family']} / {w['workload']} | "+' | '.join(f"{min(w['arm_headroom_percent'][m]):.3f}–{max(w['arm_headroom_percent'][m]):.3f}%" for m in ['random','nn','rf_lcb'])+' |' for w in stats)
    passed=[w['family']+'/'+w['workload'] for w in stats if w['gate_passed']]
    decision=('The frozen opportunity screen passed for '+', '.join(passed)+'. This is development headroom only, not evidence an LLM can achieve it. Do not authorize inference implicitly; a new paired-model protocol and request allowance are required.' if passed else 'No workload passed the frozen opportunity screen. Do not retune these exposed grids or launch additional model calls on them under this protocol. This is a bounded negative development result, not proof that LLM optimization cannot work.')
    text=f'''# V59 — expanded, correctness-checked classical screen

Actual local execution after explicit user approval of a 7200 s collection cap.
**{decision}** Four workloads belong to two software families; there is no new
independent-system or held-out router claim. V57's failed p20 admission remains
reported (three CPU timeouts) and is not relabeled as a negative LLM result.

## Execution and evidence

All {p['attempted']} / 576 intended invocations attempted, {p['valid']} valid,
{576-p['valid']} resource failures, {p['unattempted']} unattempted; no retries or
outcome-driven exclusions. Stage {p['stage_seconds']:.6f} s / 7200 s. Workload/configuration
order, three repetitions, correctness checks and penalties were frozen before
collection. Plan validity and recomputed cost 105 checked independently; Java output
hashes match the predeclared workload-specific reference streams. The full grid
uses unchanged V54/V56 configuration choices on V57-admitted new workloads.

Completed 60 classical arms: five seeds per workload, shared 10-observation prefix,
random/3NN/RF-LCB continuations to 20 inclusive aggregate outcomes.800 actual recorded
acquisitions, offline {s['runtime_seconds']:.6f} s / 180 s. All labels charged; own acquired
labels/features only. Full-table scores computed after all choices were saved.
No LLM output, inference requests, downloads, cloud resources or external spending.

| Workload | Valid trials | Best recorded median (ms) | Median valid-setting CV | Gate threshold | Cases meeting gate | Decision |
|---|---:|---:|---:|---:|---:|---|
{table_text}

Gate compares the hindsight best-of-three classical portfolio with recorded minimum;
it is deliberately conservative and NOT a deployable policy. Its success cannot be
attributed to a single 20-evaluation arm without checking that arm's own results:

| Workload | Random exact minimum | 3NN exact minimum | RF-LCB exact minimum | Prefix headroom range |
|---|---:|---:|---:|---|
{counts}

The actual arms retain different amounts of opportunity. These ranges cover all
five fixed seeds; they are descriptive, not confidence intervals:

| Workload | Random20 remaining headroom | 3NN20 remaining headroom | RF-LCB20 remaining headroom |
|---|---:|---:|---:|
{remaining}

In particular, p10's best-of-three result must not be reported as success of every
cheap optimizer. No arm reaches the recorded minimum in all five seeds. The shared-prefix
research ledger charges 40 aggregate acquisitions per case (10 prefix plus three
10-outcome continuations), while each individual arm uses 20. Selecting the best
arm after observing outcomes uses hindsight; the screen does not supply a reliable
pre-decision method selector. A failed conservative gate therefore does not rule
out selective gains over one fixed baseline, nor establish that an LLM can supply
them. All measured responses in this stage are classical.

![Physical records](../results/v59_workload_screen/physical_tables.png)

![Actual classical continuations](../results/v59_workload_screen/classical_headroom.png)

## Validation, interpretation and limits

Independent saved-evidence verifier checks 358 frozen inputs, approval/protocol binding,
576 raw trial receipts and schedule, {verified['valid_plans']} valid plans,
{verified['java_invocations']} JVM invocations / {verified['java_completed_iterations']} completed
harness iterations, retained actual Java output hashes, all 800 charged labels,
60 shared-prefix/budget traces and 720 reconstructed choices. It recomputes every
median/CV/threshold/headroom/case decision. This is verification of saved evidence,
not independent-machine reproduction of physical timings.

Java objective is the final timed harness iteration (warmup overhead charged as
collection cost). Planning objective includes process/translation/search/monitoring
wall time. Each objective is median of three repetitions. Resource penalties are
120000 ms Java / 60000 ms planning, explicitly scores rather than fabricated runtimes.
Raw wall/exit/status and failures remain available. Do not pool these raw objectives
across workloads or pretend repeated seeds/tasks are independent systems.

Only two families, two measured grid workloads each; selection follows V57 admission,
which itself used metadata-selected five workloads. The hardest planning task p20
lacks a completed reference under its cap. One host, limited repeats/one warmup,
no independent external VAL, limited STRIPS validator, and noisy recorded minima
constrain claims. Validity/cost equality is not an independently certified optimality
proof. RSS 2 GiB watchdog is sampled, not a hard macOS memory bound. Exit timestamps
avoid watchdog tick rounding; monitoring/OS load can still perturb timings. A gate
failure is not a statistical proof of equivalence or an upper bound beyond this grid.

## Cost and reproducibility

New actual research collection: 576 physical trials, including all repetitions,
failures, Java warmups and validation; 800 recorded aggregate accesses for four-workload
counterfactual replay. Reference-admission probes from V57 are prior additional cost.
Estimated one 20-outcome deployed arm needs 60 physical trials under this recipe,
conditional on a known utility contract; include separate admission/setup cost if
needed. No new model calls; local electricity/hardware and agent/user time costs
unknown. External experiment spend USD 0. Paid inference remains disabled.

Raw logs/plans/SAS/validation and complete case denominator:
results/v59_workload_physical/. Medians/repeats, prefixes, arms, acquisition journals,
CSV, figures and summaries: results/v59_workload_screen/. Exact runtime/task
provenance is inherited from the 358-input freeze; approval and verification in
artifacts/study_v59/. Sources/data-specific redistribution limits remain unchanged.
The immutable protocol title reflects its pre-approval state; approval_receipt.json
and STATUS record actual authorization/execution without rewriting frozen inputs.

Safe saved-evidence reproduction:

```sh
.venv/bin/python scripts/verify_workloads_v59.py
.venv/bin/python scripts/report_workloads_v59.py
.venv/bin/python -m pytest -q tests
```

Collector and primary analysis are one-shot: preserve outputs; do not delete to
rerun, silently extend caps or retune thresholds after outcomes. Detailed source
and experimental decisions remain in STATUS. No publication, push or contact.
'''
    (ROOT/'reports/workload_screen_v59.md').write_text(text)
    print(json.dumps({'gate_passed_workloads':passed,'physical_valid':p['valid'],'report':'reports/workload_screen_v59.md'},indent=2))
if __name__=='__main__':main()
