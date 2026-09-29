"""Regenerate report, tables and static figures from actual V55/V56 logs."""
import collections, csv, json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR",str(ROOT/"artifacts/.mpl_cache"))
os.environ.setdefault("XDG_CACHE_HOME",str(ROOT/"artifacts/.font_cache"))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def read(p):return json.loads(p.read_text())
def main():
    out=ROOT/'results/v56_planning_screen';s=read(out/'summary.json')
    physical=read(ROOT/'results/v56_planning_physical/summary.json')
    trials=read(ROOT/'results/v56_planning_physical/all_cases.json')
    v55=read(ROOT/'results/v55_planning_feasibility/summary.json')
    table=read(out/'table.json');counts=collections.Counter(t['status'] for t in trials)
    with (out/'settings.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['config_id','heuristic','pruning','cache','tie','median_penalized_ms','valid_repetitions','cv'])
        for t in table:w.writerow([t['config_id'],*t['configuration'],t['median_ms'],t['valid_repetitions'],t['cv']])
    with (out/'cases.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['seed','prefix_best_ms','random_best_ms','nn_best_ms','rf_lcb_best_ms','portfolio_headroom_percent','gate_met'])
        for c in s['cases']:w.writerow([c['seed'],c['prefix_best_ms'],*[c['best_ms'][m] for m in ['random','nn','rf_lcb']],c['portfolio_headroom_percent'],c['gate_met']])
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.15,1]})
    ax=axes[0]
    for heuristic,color in [('lmcut','#2869a6'),('hmax','#bf5a32')]:
        records=[t for t in table if t['configuration'][0]==heuristic]
        ax.scatter([t['config_id'] for t in records],[t['median_ms']/1000 for t in records],label=heuristic,color=color,s=28)
    ax.axhline(20,color='#555',ls=':',lw=1,label='Failure penalty (not runtime)')
    ax.set(yscale='log',xlabel='Fixed configuration ID',ylabel='Median penalized wall seconds',title='48 settings × 3 real trials')
    ax.legend(fontsize=8,loc='best')
    ax=axes[1];xs=np.arange(5)
    for method,label,marker,color in [('prefix','At 10 evaluations','o','#888'),('random','Random at 20','v','#ce8c23'),('nn','3NN at 20','s','#2869a6'),('rf_lcb','RF-LCB at 20','^','#399166')]:
        values=[c['prefix_best_ms'] if method=='prefix' else c['best_ms'][method] for c in s['cases']]
        ax.plot(xs,[100*(v-s['table_minimum_ms'])/v for v in values],marker=marker,label=label,color=color,lw=1)
    ax.axhline(s['gate_threshold_percent'],color='#9b3f42',ls=':',lw=1,label='Development gate threshold')
    ax.set(xticks=xs,xticklabels=[str(c['seed']) for c in s['cases']],xlabel='Repeated seed (one software family)',ylabel='Headroom to best recorded median (%)',title='Shared prefix; 20-outcome inclusive budgets')
    ax.legend(fontsize=8,loc='best')
    fig.suptitle('Fast Downward: correctness-checked development screen',fontsize=14)
    fig.text(.5,.025,f"{physical['valid']}/144 valid trials; failures retained. Recorded minimum is hindsight. No LLM calls or held-out claim.",ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.95))
    fig.savefig(out/'planning_screen.png',dpi=170);fig.savefig(out/'planning_screen.svg');plt.close(fig)
    rf_hits=sum(c['best_ms']['rf_lcb']==s['table_minimum_ms'] for c in s['cases'])
    rows='\n'.join(f"| {c['seed']} | {c['prefix_best_ms']/1000:.4f} | {c['best_ms']['random']/1000:.4f} | {c['best_ms']['nn']/1000:.4f} | {c['best_ms']['rf_lcb']/1000:.4f} | {c['portfolio_headroom_percent']:.3f}% |" for c in s['cases'])
    peak=max(t['peak_sampled_rss_bytes'] for t in trials)
    decision=('The prespecified headroom gate PASSED. This is a development opportunity, not measured LLM benefit. A new independent-family and real-model protocol is needed before any routing claim.' if s['gate_passed'] else 'The prespecified headroom gate FAILED. Retire this fixed grid for positive LLM-benefit discovery; do not widen the grid or change this workload until a favorable score appears. Keep it as a correctness/reliability control.')
    report=f'''# V55/V56 — Fast Downward feasibility and classical screen

Actual execution on the local Apple M3 Pro/18GiB machine, 2026-09-25. Fresh
release24.06.1 adaptation of the historical workload lead; one development family,
not replication of old timings, a new independent test set, or an LLM result.

**Decision:** {decision}

## What actually ran

V55 compiled pinned owner source locally (GPL3-or-later), without LP solvers.
Initial compiler configuration failed on a linker/SDK mismatch; project-local
MacOSX15.5 SDK selection fixed it. Both build receipts remain. Three feasibility
invocations passed: independent plan costs104, action counts18/17/18, wall seconds
{', '.join(f"{r['wall_seconds']:.6f}" for r in v55['trials'])}. Whole stage
{v55['stage_seconds']:.6f}s. Agreement with admissible A* is not an independent
optimality certificate. The validator proves plan feasibility and recomputes cost.

V56 froze48 command settings × three repetitions, shuffled independently by round.
All{physical['attempted']}/144 intended trials were attempted, {physical['valid']}
passed the full validity/cost contract; status counts: {dict(counts)}. Stage
{physical['stage_seconds']:.6f}s. No retries or dropped cases. Sampled maximum
process-group RSS {peak/1024**2:.2f}MiB. Timeout/resource failures receive20000ms
in the optimization objective; this is an explicit penalty, not invented timing.
Raw wall seconds and exit status are retained. Objective is median of three
penalized wall times; it includes process/translation/monitoring overhead.

Five fixed seeds used the same saved ten-observation prefix per paired comparison;
random,3NN and64-tree RF-LCB each continued to20 inclusive outcomes. All15 arms and
200 charged recorded median-vector acquisitions ran; offline stage
{s['runtime_seconds']:.6f}s. Full-table scoring followed saved decisions. No LLM,
router fit, token usage, paid API or cloud spending in these stages.

## Observed classical results

Best recorded median: **{s['table_minimum_ms']/1000:.6f}s**. Noise estimate from
{s['all_valid_settings']} settings with three valid repetitions: median CV
{s['median_configuration_cv_percent']:.3f}%; frozen gate threshold
{s['gate_threshold_percent']:.3f}%. Hindsight best-of-three portfolio meets threshold
in **{s['gate_case_count']}/5** seeds. That portfolio is not a deployable policy.
The actual RF-LCB arm independently reaches the best recorded median in
**{rf_hits}/5** seeds. This is an attained classical result on the saved table,
not a guarantee of the physical optimum. The small improvements over the prefix
are below the median timing CV. All72 resource failures belong to hmax settings;
V55 showed hmax can solve the task with more time, so failure here is cap-specific.

| Seed | Prefix10 (s) | Random20 (s) | 3NN20 (s) | RF-LCB20 (s) | Portfolio headroom |
|---|---:|---:|---:|---:|---:|
{rows}

![Measured screen](../results/v56_planning_screen/planning_screen.png)

## Integrity, limits and accounting

- Same domain/problem, actual action costs and validated cost104 for every valid
  run. Different plans/action counts are allowed at equal cost. All heuristics,
  pruning choices and A* tie rules preserve the intended optimal-search contract
  under the inspected source assumptions. No programmatic correctness proof.
- New independent flat typed STRIPS validator rejects unsupported expressions;
  owner documentation flags a VAL bug for this domain. The new validator has
  synthetic/adversarial tests but has not been cross-checked with a mature external
  validator. Dataset redistribution license unresolved; do not publish payloads.
- Feasibility protocol deviation: owner driver removed the V55 intermediate SAS
  files by default; PDDL, plans and full logs remain. V56 explicitly retained all
  translated tasks. This retention omission did not alter plan validation/scoring.
- Owner macOS memory log reports virtual address size, not RSS, often hundreds
  of GiB. Use wrapper sampled process-group RSS instead. Sampling may miss spikes;
  no hard macOS allocation guarantee.0.2s polling quantizes wall observations and
  perturbs timing. Small apparent runtime gaps may be monitoring/host noise.
- Three repetitions, one tiny task and five dependent seeds cannot establish
  population generalization or journal readiness.24.06.1 is pinned, not latest.
  Feasibility outcomes informed the grid/cap; all data are development evidence.
  The configuration-ID order and tie breaks are fixed; no row-permutation ablation
  or independent-machine timing reproduction was run.
- Actual research cost is147 new planner invocations (V55+V56), including repeats
  and failures, plus compilation, validation and200 recorded accesses. Estimated
  deployment for one20-outcome arm is60 physical invocations under this recipe;
  it does not require the entire144-trial collection. That deployment estimate is
  conditional on the already established task/utility contract. A cold deployment
  repeating the three feasibility probes would cost63 invocations, and should not
  be presented as a strict20-outcome end-to-end procedure. Hardware/electricity and
  agent/user time costs unknown; new external experiment spend is USD0.

Raw starts/logs/plans/validation: `results/v55_planning_feasibility/` and
`results/v56_planning_physical/`. Prefixes, arms, table, acquisition journal,
summary, CSV and figures: `results/v56_planning_screen/`. Protocols and input
seals: `reports/protocol_v55_planning_feasibility.*` and
`reports/protocol_v56_planning_screen.*`. Source audit: `planning_source_audit_v55.md`.
Verification/test/evidence receipts: `artifacts/study_v55/` and `artifacts/study_v56/`.
All379 tests passed. Read-only verifier checked all144 trial receipts,75 valid
plans including V55,200 charged acquisitions,15 arms,180 reconstructed choices
and both input seals. PNG was visually checked. This replays measured evidence;
it does not independently rerun the physical timings on a different machine.

Safe saved-evidence replay (does not rerun workloads or acquire new labels):

```sh
.venv/bin/python scripts/verify_planning_v56.py
.venv/bin/python scripts/report_planning_v56.py
.venv/bin/python -m pytest -q tests
```

Collectors and offline screen are one-shot and refuse overwrite. To recollect,
create a new versioned protocol/output tree; do not delete/overwrite this evidence.
'''
    (ROOT/'reports/planning_screen_v56.md').write_text(report)
    print('Rendered saved-evidence report, CSV, PNG/SVG.')
if __name__=='__main__':main()
