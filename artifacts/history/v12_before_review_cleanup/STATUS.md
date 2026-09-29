# Status — 2026-09-24, quality feasibility and actual constrained controls complete

## Resume here

Latest reports: **reports/constrained_controls_v12.md** (actual new classical experiment) and **reports/quality_feasibility.md** (retrospective opportunity). This follows the request to continue until positive. A positive effect was not used as a stopping, tuning or case-selection rule. We now have a small **mixed classical result**, not a positive LLM or router result. Original negative findings remain intact.

The cheap quality-aware optimizer improved mean relative feasible runtime over random by **4.82% on lrzip**, worsened it **2.79% on Brotli**, and improved it **1.01% overall**. All ten cases and both families are reported. Measurement uncertainty does not support calling the small aggregate statistically reliable. No new inference was run, and no positive effect of a stronger model is claimed.

## Work actually completed this turn

### V11 retrospective runtime/size feasibility

Inspected the pinned owner READMEs for Brotli and lrzip. Both document compressed output size; Brotli specifies seconds and bytes, while lrzip units are unspecified. Froze a post-hoc analysis of all five seeds for both eligible development systems. MySQL has no relevant size objective, so it is inapplicable rather than excluded on performance.

Anchor each case's size cap to the fastest original prefix row. Within the old fixed shortlist, ideal feasible selection offers above10% runtime gains over the retrospectively size-feasible old static branch in two of ten cases: **Brotli seed23,16.5%**, also smaller output; **lrzip seed37,19.5%**, within the original cap but49 source-size units larger than the static incumbent. These are **nondeployable hindsight bounds**. Old optimizers had not acquired size; no claim that they used it. V11 makes0 new model calls or optimizer acquisitions.92 tests passed at this stage.

### V12 actual joint-outcome cheap controls

Completed **20/20 continuations** on the same ten development prefixes, paired deterministic joint-three-nearest-neighbor and random full-table search. Acquired runtime/size together through a charged oracle; each arm has10 prefix +10 continuation vectors. Newly charged totals:100 shared prefix vectors +100 nearest-neighbor continuation +100 random continuation = **300 configuration-vector accesses**. These are recorded-table reads, not unique new physical benchmarks. No old labels or outcomes are silently reassigned or free.

The policy uses only acquired joint vectors and feature distances; size feasibility is predicted, never prefiltered using hidden sizes. The cap stays fixed from the acquired prefix anchor. Both arms retain a feasible incumbent. Each acquired17 infeasible rows across its100 new continuation evaluations, all charged. No failures/fallbacks. Independent replay reproduced all decisions, source values, prefixes, caps, inclusive budgets and complete denominator. **95 tests passed**.

After this cheap control, ideal full-table feasible headroom averages **0.37% for lrzip** and **9.09% for Brotli**; above10% opportunities remain in only two cases, both Brotli. A broader cross-system LLM/router experiment still lacks established independent-system headroom.

## Executed commands and artifacts

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_quality_v11.py
.venv/bin/python scripts/verify_quality_v11.py
.venv/bin/python -u scripts/run_quality_controls_v12.py
.venv/bin/python scripts/analyze_verify_quality_controls_v12.py
```

- Reports: reports/quality_feasibility.md; reports/constrained_controls_v12.md.
- Versioned frozen protocols: reports/protocol_v11_quality.md/.freeze.json; reports/protocol_v12_controls.md/.freeze.json.
- V11 source-checked anchors, caps and all60 bound comparisons: results/v11_quality/summary.json and cases.csv; artifacts/study_v11/analysis.log, verification.json/.log, tests.log.
- V12 raw charged vectors: results/v12_controls/acquisitions.jsonl; prefixes/, joint_3nn/, random/, checkpoints/, starts/.
- V12 full20-branch denominator and summaries: results/v12_controls/progress.json, summary.json, outcomes.csv.
- V12 executed source snapshot: results/v12_controls/source_snapshot/.
- V12 collection/replay/tests: artifacts/study_v12/collection.log, analysis_verification.log, verification.json, tests.log.
- Final accounting/index: artifacts/study_v12/final_ledger_snapshot.json and evidence_complete.json.

All previous scientific freezes remain intact. Earlier STATUS is preserved in artifacts/history/v10_before_quality/. V8 first-half behavior, V9 exact random reference, V10 headroom and V6 held-out routing result remain historical facts; never relabel any of them positive LLM evidence.

## Costs and remaining authorization

This turn: **0 model calls**, **300 new charged joint-vector accesses**, **1.1474sec** recorded experiment/analysis time. Tests/forensic code inspection are not collection time. Historical charged configuration accesses are now **4508**, with V12 explicitly acquiring two fields per charged vector. Prior4208 mostly acquired the original primary target. Request ledger remains **128/128 follow-up**,228 including V1. Cumulative runtime **1671.4778/1800sec**, **128.5222sec remaining**, inactive. Downloads/model bytes unchanged, external spendUSD0. No background process, contact, push or publication.

The generic request to obtain a positive result does not authorize an unspecified cap increase or guarantee one. The exhausted request allowance prevents new LLM inference; the unblocked quality-feasibility and actual cheap controls were completed first. No stronger model was downloaded or called.

## Interpretation and single next action

There is positive **opportunity in recorded configurations** and a small positive **classical average**, but no demonstrated useful LLM continuation or learned router. Report the negative Brotli comparison and uncertainty alongside lrzip gains. Do not lower thresholds, omit failures or select cases until an LLM appears helpful.

**Single next research action: review whether to expand the task set using a prospectively defined runtime/size utility and headroom beyond quality-aware cheap controls before committing to stronger-model routing.** This requires a new versioned protocol and genuinely untouched evaluation groups. Candidate-order testing remains necessary for any future model. Additional inference would need a specific reviewed allowance; its outcome cannot be promised.

Still untested: a stronger local model, new candidate-order responses, live compression correctness, paired measurement uncertainty, other budgets/multiobjective tradeoffs and broad router generalization. Nothing is scheduled outside this session.
