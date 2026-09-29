# When Is an LLM Worth Calling?

A reproducible, bounded pilot on cost- and reliability-aware escalation in offline software-configuration optimization.

**Result: no demonstrated useful LLM selection or benefit-router advantage.** All 15 direct-selection model responses chose the first ten displayed candidates. A simple order rule reproduces those choices. A later classical-only size-constrained experiment produced mixed results: +4.82% on lrzip, −2.79% on Brotli, +1.01% across two families. These point estimates do not establish statistical reliability or LLM value.

Start with the **[decision brief](reports/decision_brief.md)**, then [STATUS.md](STATUS.md) and [REPRODUCE.md](REPRODUCE.md). The bounded pilot is complete. Further inference is not recommended on the current design; the next step is task/utility review and development-only headroom validation. The original request is preserved in [START_HERE.md](START_HERE.md).

Latest continuation: [prospective admission audit](reports/admission_v13.md) executed over all 81 registered tables. No untouched family has an explicit output-size field. The current suite has **102 passing tests**; no new inference or objective acquisition was performed.

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

Scientific protocols, inputs and executed source snapshots are versioned and frozen. Tests under `tests/synthetic/` are excluded from research aggregates. Evaluations acquire recorded-table outcomes; this repository did not run live production software benchmarks. Repeated seeds are not independent systems.

## Verify locally without inference

Python 3.10.13 and the packages in `requirements.lock.txt` were used. With the supplied environment and pinned inputs:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_review_packet.py
.venv/bin/python scripts/verify_pilot_completion.py
```

The V12 suite had 95 passing tests; the current suite has 102 after the metadata admission guards. The review verifier checks scientific freezes, headline arithmetic, current accounting and local document links; it does not replace independent numerical replay. The older whole-pilot verifier covers the original scope through V9. V10–V12 replay evidence and commands are documented separately in [REPRODUCE.md](REPRODUCE.md). No clean-machine reconstruction is claimed.

The saved [exact-reference figure](results/v9_analysis/exact_reference.png) is regenerated with `scripts/render_selection_null_v9.py`. Unlike the read-only audit, analysis/render commands charge runtime to the persistent ledger.

## Provenance and limits

- [Primary source audit](reports/source_audit.md), [third-party attribution](THIRD_PARTY.md), [model manifest](artifacts/model_manifest.json), [decisions](reports/decisions.md).
- Exact SNAP2 code was not located in the bounded search. The paper-based classical method and small Qwen model are adaptations, not a numerical replication.
- Follow-up requests: **128/128 exhausted**, plus 100 initial attempts. Cumulative recorded experiment time: **1,671.48/1,800 seconds**. External spend: **USD 0**. Historical costs remain counted.
- Actual paired research collection and estimated one-branch deployment costs are separate. Preserve failures and complete intended denominators.
- Fresh collection needs a new protocol, output namespace and explicit bounded allowance. Do not reset ledgers, overwrite results or repeatedly optimize against inspected held-out outcomes.

Weights, downloaded tables and source archives are Git-ignored; restoration and licensing caveats are in REPRODUCE.md. No paid/cloud inference, publication, remote push or external contact occurred. See the [next-experiment conditions](reports/next_experiment.md) before extending this pilot.
