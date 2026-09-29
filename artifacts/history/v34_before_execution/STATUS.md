# Status — 2026-09-25: V33 model-request recovery analysis completed

## Resume here

**Next concrete result:** against fixed sequential3NN, the fifteen assigned-ID LLM outcomes have **1 improvement,8 ties,6 harms**. The improving MySQL/53 case has a hypothetical request-time recovery threshold of **444.06 seconds of future baseline work**, using its observed5.23933-second request and1.17987% recorded target reduction. That case ties after ID reassignment. **No case has a finite threshold under all three observed presentations.**

Read [V33 report](reports/amortization_v33.md), [frozen protocol](reports/protocol_v33_amortization.md), and relevant code. This is exploratory arithmetic over real cached model outcomes, not measured deployment savings, new inference or learned routing. Three families remain exposed. Do not interpret the threshold as an application-approved cost/quality tradeoff.

## What actually ran

- Fresh read-only provenance/token/cache replay of all60 historical V22 calls and150 paired arms, without inference.
- Four fixed classical comparators ×45 unique real presentation outcomes =180 paired comparisons,60 case/comparator scenarios and56 fixed work-grid rows.
- Primary baseline sequential3NN; secondary original full-space centroid, static shortlist rank, adaptive shortlist centroid. Primary presentation assigned_ids. All gains/ties/harms retained.
- **224 tests passed in1.44seconds**, with synthetic arithmetic fixtures separated from research data.
- 199 inputs frozen before scenario calculation, after prior outcome exposure.
- Independent Decimal reconstruction from original CSV targets and request logs verified1,457 numeric values,20 aggregate counts and all56 grid rows.
- Read-only scenario replay passed; all2,512 frozen historical/current input references passed. Figure visually inspected. No active or scheduled job remains.

## Scenario and result limits

Assume S seconds of future classical-baseline work, relative gain g=(classical_target−LLM_target)/classical_target and observed request time C. Modeled saving is S*g−C, with equality S=C/g only if g>0. This assumes the recorded ratio transfers linearly, acceptable configuration quality and persistent outcomes. Startup, controller computation, differing evaluation costs and future retries are excluded; this is recovery of one cost component, not total deployment net cost or a lower bound.

Equal future work per case and equal-family weighting: always calling has no finite mean recovery threshold against sequential3NN or static rank. Against original classical it crosses at275.83seconds/case; against adaptive shortlist centroid at597.59seconds/case. Preserve these favorable secondary comparisons. The hypothetical uniform one-presentation thresholds are315.81 and812.92seconds respectively, still nonfinite against3NN/static. This is one call with a random presentation, not a three-call ensemble.

At1000baseline-work seconds/case, fixed-presentation always-call versus3NN models−16.0709seconds/case. Hindsight selects only the one helpful case and models+0.4373seconds/case averaged across all15; it is nondeployable and not a router result. The MySQL case mean-presentation threshold is691.65seconds; no all-three threshold exists because reassigned IDs tie. Different work distributions or future observations could change these scenarios.

Unvalidated application utility, public-data exposure, measurement noise and only three exposed families remain. V32 timing noise is on different tasks and is not an uncertainty interval for V22. New LLM behavior, unseen-system routing and real deployment benefit remain untested.

## Commands and evidence

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
.venv/bin/python scripts/analyze_amortization_v33.py
.venv/bin/python scripts/analyze_amortization_v33.py --verify-only
.venv/bin/python scripts/verify_amortization_v33.py
.venv/bin/python scripts/render_amortization_v33.py
.venv/bin/python scripts/audit_history_v30.py
```

Analysis refuses completed outputs. Verification commands require no inference/acquisition.

- `results/v33_amortization/`:180 comparison rows with request/cache IDs,60 case scenarios,56 grid rows,summary,corrected PNG/SVG figure; initial figures preserved.
- `artifacts/study_v33/`:tests,full real-model provenance replay,analysis log,Decimal verification,read-only replay,accounting,historical integrity,render correction and final checks.
- `src/escalation/amortization_v33.py`:explicit scenario arithmetic only,no router/provider.
- `reports/protocol_v33_amortization.freeze.json`:all frozen inputs.
- `artifacts/history/v33_before_analysis/`:prior STATUS/README and ledgers.
- V26 ZIP unchanged; historical V25 reconstruction,not V33.

No experiment/verification failure occurred. Figure inspection caught default signed-log autoscaling extending into negative work; a separate renderer fixed the display domain without changing frozen analysis or numeric outputs. Original figure versions remain archived.

## Costs and next action

Actual V22 historical collection remains60 requests,95,720 input/1,200 output tokens,431.694863request-seconds including15 repeats. Single startup8.565649seconds includes model loading4.493516seconds; do not add them or multiply by60. Cached reuse does not erase collection cost.

V33 added **zero model calls,objective acquisitions,physical trials or downloads**. Analysis/initial figure0.700935375seconds; rendering correction0.321947125; total **1.022882500seconds**. Global ledger **2,277.118491629 /3,600seconds**, **1,322.881508371remaining**,active_since null. Historical recorded acquisitions8,308;physical trials1,274 unchanged. Model allowance remains200/200follow-up,300including initial stage. External spendUSD0;no cloud,push,publication or contact.

**Single next action:** specify the application quality constraint,expected configuration reuse and practical gain margin before new paired collection. Use development measurements to establish repetition/cost estimates,freeze strong controls and reserve untouched software groups. Fresh LLM evidence needs a new bounded allowance or compatible provenance-checked cache. Further post-hoc arithmetic on these same cases will not establish generalizable routing success.
