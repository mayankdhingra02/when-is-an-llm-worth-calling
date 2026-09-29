# STATUS — V42 exact shortlist diagnostic executed

Updated 2026-09-25. Resume from this section, `reports/selection_reference_v42.md`, `reports/protocol_v42_selection_reference.md` and its freeze. The V41 measured study below is unchanged; V42 is explicitly post-hoc, not a new held-out confirmation.

New concrete result: every saved shortlist was fully covered by already acquired branches. Exact uniform ten-of-twenty selection distributions were computed for all30prefixes and independently checked by enumerating5,542,680subsets. No new model call or objective acquisition.

-1.5B attains the shortlist ceiling28/30times; batch3NN already does27/30. Maximum possible mean gain over batch3NN is only+0.1174%, versus the measured+0.1024%.
-Against full-domain sequential3NN, a perfect shortlisted selector used on every case is bounded at−1.8207%, versus measured1.5B−1.8356%. Seven cases still permit selective gains, fifteen tie and eight cannot match full-domain search. Do not claim all possible routers are dominated.
-Exact expected relative gain vs uniform selection:1.5B+1.0689%,0.5B−1.8872%; all six family means respectively positive/negative. Conditional random-match probabilities are not population p-values.

This separates within-shortlist selection quality from a candidate-pool limitation. It supports a more specific negative/mixed contribution, but Q2 readiness, novelty and useful routing remain unproven. Larger selectors alone cannot remove a fixed-pool ceiling. Do not retune the exposed cases until favorable.

Evidence: `results/v42_selection_reference/summary.json`, all60model comparisons/60ceiling comparisons inCSV, PNG/SVGfigure; `artifacts/study_v42/analysis.log`, `exhaustive_verification.json`, `tests.log`;315tests pass. Original308inputs frozen before these new calculations; exact formulas checked by independent enumeration. Figure visually verified. No new LLM output or live physical trial. The V41review ZIP is unchanged and excludes V42.

Commands actually run:
```
.venv/bin/python scripts/analyze_selection_reference_v42.py
.venv/bin/python -I -S scripts/verify_selection_reference_v42.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/render_selection_reference_v42.py
```

Resources:290/290follow-up calls;2860.933003/3600seconds, remaining739.066997s. V42 charged2.187796s, zero calls/acquisitions/downloads/USD. No active job. Previous turn was substantive progress(real60-call V41); this turn made progress with a new exact diagnostic. Broad goal remains unachieved; no completion claim.

**Next scientific action:** compare this specific candidate-pool diagnosis with prior work and develop an escalation intervention that can expand useful search regions under equal application quality and independent development/test groups. More ranking calls on these same shortlists cannot solve the observed limitation. Any new inference still requires a concrete bounded extension; no cap increase is inferred from automatic continuation. No author contact/publication authorized.

---

# STATUS — V41 real-model study completed and verified

Updated2026-09-25. Resume from this file, `reports/models_v41.md`, the unchanged original protocol/analysis seals and the measured summaries. Do not reread the full literature report. The user's exact60-call extension was approved and fully executed. The old approval blocker is resolved; the broader Q2-quality objective remains unachieved and is not marked complete.

## New concrete research result

Completed60real local-model cases: six newly admitted software families × five fixed seeds × two Qwen2.5-Instruct sizes(0.5B/1.5B). Each shares its original10-evaluation prefix and acquires10continuation outcomes. No completed cases, seeds, failed attempts or poor results were dropped. Seven classical controls were fixed in advance.

-1.5B vs primary batch3NN: **+0.1024%** equal-family mean,2wins/27ties/1harm; family bootstrap95%[0%,0.3073%], exact sign-flip p=1. Only HIPAcc has a nonzero family mean.
-1.5B vs full-domain sequential3NN: **−1.8356%**,6wins/15ties/9harms; exact family p=.15625.
-0.5B vs batch3NN: **−3.0260%**; vs full-domain sequential3NN: **−4.9260%**.
-The unchanged benefit router selects1/30cases. On1.5B it ties batch3NN and slightly harms the strong control; on0.5B it harms quality. Uncertainty selects0calls. No successful useful routing claim.
-1.5B hindsight oracle opportunity is only0.1075% vs batch3NN(2calls) or0.2816% vs full-domain3NN(6calls), before cost. Diagnostic/nondeployable.

This is a stronger negative/mixed empirical result than the previous two-family study, not evidence that the original hypothesis is established. Six groups, two sizes of one model family, benchmark age/subsampling/nominal encoding, unknown application quality and unresolved novelty still prevent a Q2-readiness claim. Do not keep tuning these now-exposed cases until a mean becomes positive.

## Execution and reliability

The0.5B model completed30cases. The first1.5B worker failed during startup with OpenMP Error179(Cannot open SHM), before issuing any request. Terminal original run and logs are preserved in `artifacts/study_v41/recovery_attempt1/`. User-approved sandbox escalation allowed the one-shot recovery wrapper to run only the30unattempted1.5B cases with unchanged settings. All63completed0.5B files were hash-preserved. Failed-startup time counted against the same700-second stage cap. No request retry; one startup retry/failure. Transformers implementation warnings remain in raw logs.

Actual model collection:60requests,600newrecorded outcome accesses,98,342input tokens,1,200output tokens,254.780243s request wall time,277.213992s total stage time including startup/failure/recovery. Combined V41 collection:3,000recorded accesses including the210classical continuations. Every logical deployment arm remains20evaluations. No new physical trials, downloads, cloud usage or external spending.

## Verified evidence

- `results/v41_models/`: all requests/request-starts/model identities,60branches, checkpoints,600-event acquisition journal and complete denominator.
- `results/v41_model_analysis/`: all420paired comparator rows,14contrasts,108policy views, complete cost summary, two PNG/SVGfigures.
- `results/v41_policy_precommit/`: decisions and analysis seal from before all new model responses;29/30prefixes outside at least one development range; no refit.
- `artifacts/study_v41/`: collection/recovery logs, source/token/arithmetic checks, tests, archive receipts.
-300tests pass. All600acquired targets match source rows(542distinct rows), independently on Python3.10/3.12. All60prompt/token/grammar/cache-key traces replay. Fraction arithmetic independently agrees on420contrasts,14summaries and108policy means on both interpreters.
-Original103-input protocol freeze and later analysis/policy seal remain intact. Model logits were not regenerated, and a separate physical machine was not used.

## Portable local review artifact

`output/llm_escalation_v41_review.zip` — 1,613,626bytes,465files; SHA256 `84a935ae4373a7299dbf49f14f58434b3528fd893fad026245f426b3e75657c8`.
Extract locally and run `python3 -I -S scripts/verify_review_bundle_v41.py`. Verified in isolated3.10/3.12 processes; deliberate corruption of an extracted copy was rejected. It reproduces acquired-record arithmetic, not fresh model inference. Full datasets, weights and papers are omitted; source manifests/hashes and local-check receipts remain. Nothing was uploaded, pushed or sent to anyone. DeepPerf data-specific redistribution permission remains unresolved.

## Commands actually executed

```sh
.venv/bin/python scripts/run_models_v41.py
.venv/bin/python scripts/resume_models_v41.py
.venv/bin/python -I -S scripts/verify_source_events_v41.py --kind model
.venv/bin/python scripts/analyze_models_v41.py
.venv/bin/python scripts/verify_model_tokens_v41.py
.venv/bin/python -I -S scripts/verify_model_results_v41.py
.venv/bin/python scripts/render_models_v41.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/build_review_bundle_v41.py
```

Initial collector failed after the0.5B stage as described; recovery completed the denominator. Source/arithmetic/bundle verification also ran under the installed Python3.12 interpreter. Collectors/archive builder are one-shot; do not overwrite original outputs. Reanalysis counts computational runtime but no new objective acquisition.

## Limits and next decision

Follow-up requests **290/290**(390includinginitial), cumulative experiment runtime **2858.745207/3600s**, remaining **741.254793s**. Cumulative recorded outcome accesses12,608; physical trials remain1,274. No active model or experiment process. No remaining model-call allowance; do not silently extend it.

**Single most important next action:** assess with Tim Menzies whether this now-broader negative/control-transfer result offers a distinct enough contribution against the close prior work in `reports/literature_update_v40.md`, before authorizing another experimental design. A reviewable report and local replay kit are ready; do not contact him automatically. If further collection is scientifically justified, prioritize independent development families, an independent model family and equal application-utility/correctness constraints before another held-out router. A stronger result is not guaranteed by more calls.
