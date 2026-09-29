# Status — 2026-09-24, concrete result and original-scope audit complete

## Read first

**reports/concrete_result.md** is the final concise result. **reports/completion_audit.md** maps the original seven requested stages to inspected code, raw evidence and executed checks. **REPRODUCE.md** gives reproduction commands and honest scope limits. Do not reread the initial research report. V8 collection history remains in reports/pilot_report_v8.md; prior STATUS/README/review notes are preserved in artifacts/history/v8_before_exact_analysis/.

The active goal asked to continue until a concrete result, with permission to stop if no good result was possible. This turn added a mathematical comparison and an end-to-end audit rather than further speculative inference. The original task explicitly accepts negative findings. **The bounded pilot now has a concrete reproducible finding; a successful benefit-aware router is not established.** No positive-effect/novelty/publication claim is made.

## Concrete finding

All15 real V8 model responses selected IDs0–9, exactly the first ten displayed candidates, with row sequences identical to the measured continuations. Because candidate identities were randomly assigned, the observed rule is equivalent to taking half a shuffled shortlist. It can reproduce these recorded choices and outcomes without a model. This does not prove what the model would do on new prompt orders; no such inference was run.

The new V9 retrospective analysis computed exact uniform ten-of-twenty minimum-loss distributions, including the prefix incumbent, and independently enumerated **184756 subsets for every one of15 cases**. All counts and expectations matched. These are analysis combinations, not2.77million new experiments or oracle acquisitions. Mean losses (first average five seeds within each development system, then three systems):

| Continuation/reference | Mean normalized loss |
|---|---:|
| Existing adaptive classical | .015580 |
| Exact uniform shortlist expectation | .012250 |
| Measured static shortlist ranking | .011337 |
| Observed LLM (first displayed half) | .010232 |

Uniform shortlist selection already yields expected gain **.003330** versus adaptive classical; observed LLM gain was **.005349**. The residual observed advantage **.002018** over random expectation does not establish learned ranking, given the identical positional response pattern. Each individual random-subset distribution assigns at least **50%** probability to matching or beating that case's observed LLM loss (ties included). These are conditional finite-pool reference probabilities, not p-values or generalization guarantees. No aggregate significance claim is made.

V6 remains the latest held-out routing test:2/15 material benefits,3/15 harms, zero escalations from both benefit and uncertainty controllers, no demonstrated router advantage. Only three independent held-out groups. V7 removed prefix copying without material improvement. V8 showed superficially favorable scores but a trivial positional selection rule. All are documented separately; adaptive development versions are never pooled as fresh held-out evidence.

## What actually ran this goal turn

- Added src/escalation/selection_null_v9.py and13 new synthetic mathematical tests; **77 tests passed in0.83sec** overall.
- Froze a post-hoc analysis specification and input/code hashes before its computation: reports/protocol_v9_analysis.md and .freeze.json. The report explicitly says outcomes were already seen.
- Ran scripts/analyze_selection_null_v9.py. Exact integer subset counts matched brute-force enumeration in all15 cases, including ties/incumbent clipping; floating-point loss expectations agreed.
- Rendered and visually inspected results/v9_analysis/exact_reference.png/.svg with scripts/render_selection_null_v9.py. No model call or optimizer acquisition.
- Ran scripts/verify_pilot_completion.py: corrected V3 smoke/classical/paired replay; V6/V7/V8 source-label/state/token/provenance/budget replay; official local weights hashed; all30 V6 predecision feature vectors recomputed; development-only controller refit reproduced sealed scaling/coefficients/thresholds; all seven held-out policies reproduced. Current live ledger unchanged by this forensic audit.
- Created reports/concrete_result.md, reports/completion_audit.md and REPRODUCE.md; updated README, review note and this status.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_selection_null_v9.py
.venv/bin/python scripts/render_selection_null_v9.py
.venv/bin/python scripts/verify_pilot_completion.py
```

The analysis command refuses overwrite of completed numerical evidence. The renderer regenerates only presentation. Old V6/V7 verifiers contain stage-specific ledger assertions; the unified audit evaluates those against preserved historical snapshots98/113 and separately checks the current128 ledger, without resetting or mutating it. Historical outputs are redirected to artifacts/completion_audit/. Source and scientific freezes remain intact.

## Evidence to inspect

- Main result: reports/concrete_result.md.
- Original requirement audit: reports/completion_audit.md; machine proof artifacts/completion_audit/completion.json and per-version replay reports/logs.
- V9 exact reference: results/v9_analysis/summary.json, cases.csv, exact_distributions.json; post-hoc namespace distinct from measured results.
- Enumeration run: artifacts/study_v9/analysis.log. Tests: artifacts/study_v9/tests.log. Audit execution: artifacts/study_v9/completion_audit.log.
- Scientific protocol/code: reports/protocol_v9_analysis.md/.freeze.json; src/escalation/selection_null_v9.py; scripts/analyze_selection_null_v9.py; tests/synthetic/test_v9_null.py.
- Figure: results/v9_analysis/exact_reference.png/.svg; presentation-only renderer scripts/render_selection_null_v9.py.
- V8 raw real-model evidence unchanged: results/v8/requests.jsonl, request_starts.jsonl, acquisitions.jsonl, llm/, uniform_selection/, static_rank/, selection_diagnostics.json.
- Final accounting/index: artifacts/study_v9/final_ledger_snapshot.json and evidence_complete.json.

## Resources and permissions

This turn added **0 model calls and0 optimizer acquisitions**. It consumed **1.2456 seconds** recorded analysis/figure time; tests and forensic verification are not labeled collection time. Requests remain **128/128** follow-up, **228 historical** including V1. Historical target acquisitions remain **4208**. Runtime **1670.0678/1800sec**, **129.9322sec left**, ledger inactive. Downloads/model bytes unchanged; **USD0** external spend. No background worker, cloud, contact, remote push or publication.

The prior explicit fifteen-call approval was fully executed in V8. A further spoken “Approved” arrived during this no-call analysis; it is not recorded as approval for an unspecified request-cap increase. No additional inference allowance is assumed.

## Completion and single next action

The requested bounded, credible pilot and evidence package are complete, including a negative/limited answer to the routing hypothesis and a concrete mechanism finding. The requirement-by-requirement audit passes. This is not a stopping decision caused merely by token limits, runtime or a desire for positive results.

**Single next research action: discuss the concrete result with Tim and decide whether a predeclared candidate-order permutation diagnostic should precede any larger router study.** The repository provides the report; nothing has been sent. New inference would need a specific allowance. Do not silently reset counts or treat exposed test systems as untouched.

Untested: model responses on independently permuted orders, stronger local models, empirical nonbinary tasks, multiple budgets/objectives, broader independent families, clean-machine repeated inference, and learned-router generalization. A future positive routing result cannot be promised. No work is scheduled outside this session.
