# Latest result: V93 decoder check completed with one preserved failure

All 53 returned native Qwen3 answers matched forced-decoder selection sets; all nine forced controls reproduced. One resource-failed request remains unknown. The conservative stability bounds still fail the frozen screen. See [actual result](reports/decoder_v93.md), [research readiness](reports/research_readiness_v93.md) and [resume status](STATUS.md). The combined portable saved-response audit is `output/diagnostics_v93_reproduction.zip`; it does not rerun model inference. This is a scoped negative result, not established journal readiness.

---

# Latest result: V92 Qwen3 sensitivity diagnostic

All 108 conditions and 1,080 real requests completed. Both representations failed the frozen responsiveness/stability screen; this is development evidence, not optimization benefit or journal readiness. See [report](reports/sensitivity_v92.md) and [resume status](STATUS.md). The portable saved-response replay is `output/sensitivity_v92_reproduction.zip`; it excludes model weights and does not rerun inference. V93 is specified but not yet executed.

---

# When Is an LLM Worth Calling?

A reproducible, bounded pilot on cost- and reliability-aware escalation in software-configuration optimization.

**Latest real-model result (V91):** [Qwen3-8B robustness comparison](reports/qwen_v91.md): 30 cases, 300 research plus three compatibility requests, 300 new recorded outcomes, zero fallbacks. Mean gain +1.22% versus SmolLM3, but −1.26% versus same-pool batch 3NN and −3.20% versus full-domain sequential 3NN. The frozen primary screen failed. Completed locally in 238.4 seconds; 685 tests pass. [Figure](results/v91_analysis/family_gains.png). Current integrity command: `.venv/bin/python scripts/seal_qwen_v91.py --verify-only`. No held-out routing or journal-readiness claim.

**Latest completed control screen (V90):** [Broader DuckDB comparison](reports/flights_v90.md):60validtrials,12,060exactanswers,0settingsmeetingthefrozenpractical-improvementrule. EarlierV89timeout and test-overlapconfound retained; no LLMbenefitclaim. Close this small domain for escalation. [Figure](results/v90_flights_analysis/grid.png). [Larger-model resource proposal](reports/resources_v91.md) pending explicit numeric-cap change. Current integrity: `.venv/bin/python scripts/seal_flights_v90.py --verify-only`.

**Latest actual native result (V88):** [Real-flight DuckDB feasibility](reports/flights_v88.md): 9/9 trials, 513 independently checked query answers, no LLM calls. Four threads reduced median query time by47.54%, but narrowly failed the frozen repeat-stability screen. This is configuration sensitivity, not LLM benefit or journal readiness. [Figure](results/v88_flights_analysis/feasibility.png). TPC generator unused; CC0 data avoids that terms blocker. Current integrity command: `.venv/bin/python scripts/seal_flights_v88.py --verify-only`.

**Latest cross-family analysis (V86):** [Exact control-aware opportunity](reports/frontier_v86.md) enumerates65,664 saved-outcome choices across RocksDB, Kanzi and H2. Against cheap controls, no choice improves RocksDB/Kanzi observed quality; H2’s maximum hindsight mean gain is0.262%. All25cases are included; three exposed families, no learned/held-out policy claim.630tests passed. [Portable stdlib replay](output/frontier_v86_1_reproduction.zip) reconstructs the analysis, not native/model trials. [Figure](results/v86_frontier/frontiers.png). V86 historical integrity entrypoint; use V87 above after later root-document changes.

**Latest real-model result (V85):** [H2 paired continuation](reports/h2_v85.md) completed with **35 real SmolLM3 calls, 115/115 valid native trials, five seeds and 625 passing tests**. No seed achieved the frozen 10% improvement margin over RF or the fixed prior. Mean paired gains: +0.13% versus RF, −1.53% versus prior; added selection time versus RF: 11.55 seconds/case. All final configurations used the prior’s index mask. One exposed H2 family; no learned-router/generalization or journal-readiness claim. [Figure](results/v85_h2_analysis/paired_results.png), [raw evidence](results/v85_h2_paired/), [validated analysis](results/v85_h2_analysis/).

V85 historical integrity entrypoint (use V86 above after later root-document changes): `.venv/bin/python scripts/seal_h2_v85_execution.py --verify-only`. The approved batch is complete and its inference allowance consumed. Preparation and synthetic tests remain separately preserved in [readiness](reports/readiness_v85.md) and [validation](reports/validation_v85.md).

**Latest classical result (V84):** [H2 budgeted comparison](reports/h2_v84.md),165/165valid native trials,five10-evaluation prefixes,608tests passed. RF had 0/5 and random 0/5 descriptive improvements of at least10% over the fixed prior. Gains also passing the repeat-precision screen: RF 0/5, random 0/5. No H2LLM or generalization claim.

**Latest native feasibility (V81–V83):** [H2 report](reports/h2_v83.md).19new physical charges,18validated,one retained validation failure. V83 passes the coarse same-host precision screen. No new model calls or H2 optimization evidence;604tests passed. Start at [STATUS](STATUS.md).

**Latest completed LLM experiment (V80):** [Real-model comparison against a cheap preset](reports/kanzi_v80.md): **105 genuine local SmolLM3 requests and 450 valid physical trials**. Against the preset: **0 wins, 10 ties, 5 losses**, with about **9.85 seconds extra decision time per case**. Against RF: 4 wins, 6 ties, 5 losses. All requests valid, no fallback. Three corpus inputs remain **one exposed development family**; no useful learned-router/generalization or Q2-readiness claim.

[Portable outcome-reconstruction ZIP](output/kanzi_v80_outcome_reconstruction.zip) passed isolated standard-library replay and three semantic corruption checks; see [reproduction scope](reports/reproduction_v80.md). It is not a fresh native/model replication. Pre-collection suite: **594 tests passed**. Start at [STATUS](STATUS.md).

Previous [V79](reports/kanzi_v79.md) prospectively tested the cheap preset on new inputs; [V78](reports/kanzi_v78.md) motivated that control. [V72 RocksDB](reports/rocksdb_v72.md) was also negative against both RF and a cheap domain rule. Older drafts and bundles below cover their named historical snapshots, not the current experiment.

The historical [V40 routing-opportunity analysis](reports/frontier_v40.md) remains available; its counts and draft below describe that older snapshot.

A historical [exploratory short-paper draft](paper/manuscript.md), [claim audit](paper/claim_evidence.md) and [readiness assessment](paper/readiness.md) now accompany the data. This is a narrow negative-results candidate,not an established novel/generalizable router. Close prior work and onlytwo exposed systems limit the claims.

The [portable V38 archive](output/llm_escalation_v38_reproduction_v39_1.zip) remains verified on Python3.10/3.12;it does not include V40analysis.

Start with **[STATUS.md](STATUS.md)**. Previous results include [V28 voting](reports/consensus_v28.md) and [V27 metric sensitivity](reports/metric_sensitivity_v27.md); all earlier outcomes are preserved.

The older [V25 standalone reconstruction bundle](output/llm_escalation_v25_reproduction.zip) remains a reproducible **V25 snapshot**,not a package of V27–V34. Its isolated standard-library replay passed on Python3.10.13 and3.12.14. Extract it and run `python3 -I -S scripts/verify_reproduction_v26.py`. [Scope/instructions](BUNDLE_V26_README.md). The older PDF/V21 ZIP are also historical. Original request: [START_HERE.md](START_HERE.md).

## Evidence map

| Stage | Executed scope and disposition | Report / raw evidence |
|---|---|---|
| V1–V2 | Initial runs, malformed responses, timeout and subsequently discovered SQLite schema error; preserve, do not pool with corrected results | [Erratum](reports/schema_erratum.md); `results/classical/`, `results/paired/`, `results/v2/` |
| V3 | Corrected three-system, five-seed smoke; 20 evaluations with checkpoint 10; real local inference | [Report](reports/pilot_report_v3.md); `results/v3/` |
| V4–V5 | Projection control, source/alias registry and admission checks; proposed 20-group study never executed | [Registry](reports/registry_v5.md); `results/v4_projection_diagnostic/` |
| V6 | Six families, development-sealed router, three held-out families; no observed router advantage | [Report](reports/pilot_report_v6.md); `results/v6/` |
| V7 | Prefix-copy exclusion: 15 real model cases and matched controls; no material benefit | [Report](reports/pilot_report_v7.md); `results/v7/` |
| V8 | Direct candidate selection: 15 real model cases and 30 controls; model always selected IDs 0–9 | [Report](reports/pilot_report_v8.md); `results/v8/` |
| V9 | Exact retrospective random-selection reference, exhaustive subset verification | [Result](reports/concrete_result.md); `results/v9_analysis/` |
| V10 | Hindsight headroom and normalized-metric audit; no new model calls or acquisitions | [Decision](reports/headroom_decision.md); `results/v10_headroom/` |
| V11 | Retrospective runtime/output-size feasibility, explicitly hindsight | [Report](reports/quality_feasibility.md); `results/v11_quality/` |
| V12 | 20 actual cheap constrained continuations, 300 charged joint-vector accesses, mixed result | [Report](reports/constrained_controls_v12.md); `results/v12_controls/` |
| V13–V14 | Registry and external-artifact coverage/provenance audits; no new task admitted | [Registry admission](reports/admission_v13.md), [external audit](reports/external_admission_v14.md) |
| V15 | 288 live physical trials, correctness/payload evidence, descriptive timing stability | [Report](reports/live_measurements_v15.md); `results/v15_measurements/` |
| V16 | 30 paired classical arms, acquired-only replay, little remaining recorded headroom | [Report](reports/classical_controls_v16.md); `results/v16_classical/` |
| V17 | Expanded282-setting grid:846 physical trials,30 classical arms; little remaining recorded headroom | [Report](reports/expanded_grid_v17.md); `results/v17_measurements/`, `results/v17_classical/` |
| V18 | All30 saved development cases: initial-reference/checkpoint opportunity decomposition | [Report](reports/checkpoint_opportunity_v18.md); `results/v18_checkpoint_audit/` |
| V19 | Nine real-model ID/display interventions: all selections follow first displayed ten | [Result](reports/order_probe_v19.md); `results/v19_order_probe/` |
| V20 | Post-hoc rule comparison: two alternatives match all24 saved responses | [Audit](reports/rule_identifiability_v20.md); `results/v20_rule_audit/` |
| V21 | Three real interleaved-ID calls: one prefix-rule match, two sequence/lowest-ID matches | [Result](reports/nonmonotone_probe_v21.md); `results/v21_nonmonotone/` |
| V22 | 60 real 1.5B calls, 90 control arms, 1,500 new recorded acquisitions; small control-adjusted gain, presentation sensitivity | [Result](reports/larger_model_v22.md); `results/v22_larger/` |
| V23 | All 15 prefixes: observed gain envelopes and family-concentration checks; no consistent advantage over first-display selection | [Result](reports/robustness_v23.md); `results/v23_robustness/` |
| V24 | Exact hindsight/random escalation curves at every call budget; limited opportunity beyond first-display control | [Result](reports/opportunity_v24.md); `results/v24_opportunity/` |
| V25 | 15 new adaptive-shortlist classical arms,150 charged labels; improved old baseline but no average win over LLM | [Result](reports/shortlist_v25.md); `results/v25_shortlist/` |
| V26 | Independent stdlib reconstruction from isolated extraction on two Python versions;295-file deterministic bundle | [Report](reports/reproduction_v26.md); `artifacts/reproduction_v26/` |
| V27 | Metric sensitivity on135 paired comparisons; LLM-versus-static mean changes sign | [Report](reports/metric_sensitivity_v27.md); `results/v27_metric_sensitivity/` |
| V28 | Fifteen cached-response voting arms,150 charged labels; mixed gain at three-call scenario cost | [Report](reports/consensus_v28.md); `results/v28_consensus/` |
| V29 | Thirty fixed batch/sequential3NN arms,300 charged labels; sequential improves on tested LLM averages | [Report](reports/neighbors_v29.md); `results/v29_neighbors/` |
| V30 | Fifty prospectively frozen classical arms on Opus/Z3, 600 charged labels; mixed 3NN transfer, no model calls | [Report](reports/transfer_v30.md); `results/v30_transfer/` |
| V31 | Twenty random-control arms, 200 labels; exhaustive shortlist reference finds zero headroom beyond adaptive centroid in 9/10 cases | [Report](reports/random_v31.md); `results/v31_random/` |
| V32 | 140 fresh physical trials on seven fixed selections; Zstandard gain changes sign, all bytes verified | [Report](reports/reliability_v32.md); `results/v32_reliability/` |
| V33 | 180 real-response cost comparisons, no new inference; one finite fixed-presentation recovery case versus3NN, none across all presentations | [Report](reports/amortization_v33.md); `results/v33_amortization/` |
| V34 | Seventy constrained continuations,800 joint-vector accesses; weak-control gain disappears against stronger controls;0 new model calls | [Report](reports/constrained_v34.md); `results/v34_constrained/` |
| V35.1 | Isolated V34 reconstruction on Python3.10/3.12;9corruptions rejected; versioned float-reduction fix;418-file deterministic archive | [Report](reports/reproduction_v35.md); `artifacts/reproduction_v35_1/` |
| V36 | Twenty exact-arithmetic continuations,200charged vectors;5paths/3sets change,0terminal runtime changes | [Report](reports/arithmetic_v36.md); `results/v36_arithmetic/` |
| V37 | Offline Linux/Python3.11 reconstruction matches macOS3.10/3.12;two corruption controls;no new inference or downloads | [Report](reports/linux_reproduction_v37.md); `artifacts/study_v37/` |
| V38 | Thirty real size-aware calls,300 new vectors;small positive primary comparison but no wins over runtime3NN;258tests | [Result](reports/size_prompt_v38.md); `results/v38_size_prompt/` |

| V39 | Portable V38 replay on Python3.10/3.12;10corruptions rejected;553-file deterministic archive | [Report](reports/reproduction_v39.md); `artifacts/reproduction_v39_2/` |

| V40 |30,720exact allocations;zero recorded routing opportunity over runtime3NN;264tests;exploratory paper draft|[Result](reports/frontier_v40.md);`results/v40_frontier/`|

Scientific protocols, inputs and executed source snapshots are versioned and frozen. Tests under `tests/synthetic/` are excluded from research aggregates. V1–V14 optimizer evaluations acquire recorded-table outcomes. V15 adds a controlled local compression workload; V16 optimizes its recorded medians. V17 repeats collection with a larger grid and paired classical controls. No live production workload was benchmarked. Repeated seeds are not independent systems.

## Verify locally without inference

Python 3.10.13 and the packages in `requirements.lock.txt` were used. With the supplied environment and pinned inputs:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_size_prompt_v38.py --verify-only
.venv/bin/python -I -S scripts/verify_size_prompt_v38.py
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
.venv/bin/python scripts/analyze_robustness_v23.py --verify-only
.venv/bin/python scripts/analyze_opportunity_v24.py --verify-only
.venv/bin/python scripts/analyze_shortlist_v25.py --verify-only
.venv/bin/python scripts/analyze_neighbors_v29.py --verify-only
.venv/bin/python scripts/verify_neighbors_v29.py
.venv/bin/python scripts/analyze_transfer_v30.py --verify-only
.venv/bin/python scripts/verify_transfer_v30.py
.venv/bin/python scripts/audit_history_v30.py
.venv/bin/python scripts/analyze_random_v31.py --verify-only
.venv/bin/python scripts/verify_random_v31.py
.venv/bin/python scripts/analyze_reliability_v32.py --verify-only
.venv/bin/python scripts/verify_reliability_v32.py --verify-only
.venv/bin/python scripts/analyze_amortization_v33.py --verify-only
.venv/bin/python scripts/verify_amortization_v33.py
```

The suite includes evidence-corruption, prompt-preservation and V22 permission/model-identity checks. The V22 read-only audit requires the retained local tokenizer and source tables; it checks frozen inputs, all 60 token/provenance mappings, 150 arm replays and metrics without inference or ledger mutation. Earlier verifiers have historical accounting assumptions; `verify_review_current.py` targets the 140-call snapshot and is no longer the current entrypoint. No clean-machine reconstruction is claimed.

The saved [exact-reference figure](results/v9_analysis/exact_reference.png) is regenerated with `scripts/render_selection_null_v9.py`. Unlike the read-only audit, analysis/render commands charge runtime to the persistent ledger.

## Provenance and limits

- [Primary source audit](reports/source_audit.md), [third-party attribution](THIRD_PARTY.md), [model manifest](artifacts/model_manifest.json), [decisions](reports/decisions.md).
- Exact SNAP2 code was not located in the bounded search. The paper-based classical method and small Qwen model are adaptations, not a numerical replication.
- Follow-up requests: **230/230 exhausted**, plus 100 initial attempts. Cumulative recorded experiment time: **2,531.5285/3,600 seconds**. External spend: **USD 0**. Historical costs remain counted.
- Actual paired research collection and estimated one-branch deployment costs are separate. Preserve failures and complete intended denominators.
- Fresh collection needs a new protocol, output namespace and explicit bounded allowance. Do not reset ledgers, overwrite results or repeatedly optimize against inspected held-out outcomes.

Weights, downloaded tables and source archives are Git-ignored; restoration and licensing caveats are in REPRODUCE.md. No paid/cloud inference, publication, remote push or external contact occurred. See the [current result and next-experiment conditions](reports/size_prompt_v38.md) before extending this pilot.
