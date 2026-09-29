# Status — 2026-09-25: V31 random controls and exact reference completed

## Resume here

**Next concrete result:** adaptive shortlist centroid reaches the best target available in the saved prefix plus twenty-row shortlist in **9 of 10 Opus/Z3 cases**. The sole exception, Z3/11, permits at most a **0.131810%** target reduction (4.552 → 4.546). Thus a shortlist-restricted LLM has no opportunity to beat this comparator in nine cases. This is an evaluator-only hindsight ceiling, not an achieved LLM/router result or a general claim about LLMs.

Read [V31 report](reports/random_v31.md), [frozen protocol](reports/protocol_v31_random.md), and relevant code. V31 is exploratory after V30 outcome inspection. Both families remain exposed. Do not reread the full literature or treat seeds as independent systems.

## What actually ran

- Twenty new random continuation arms: ten cases × full-space/shortlist uniform sampling without replacement. Same ten-label saved V30 prefix, ten new labels per arm, twenty total evaluations.
- All 20/20 completed; 200 new recorded-label acquisitions, zero model calls/retries/failures/omitted cases. Selection uses IDs and deterministic independent SHA256-derived RNG seeds; no target-based seed search.
- 156 input references frozen before new acquisition. Old scientific code, data and results preserved.
- 217 tests passed in 1.37 seconds; tests/synthetic results stay separate from research aggregates.
- Exact conditional random terminal-target distributions calculated for both candidate pools. All 1,847,560 shortlist subsets independently enumerated; all twenty distributions independently checked with survival counts.
- Independent source/RNG/state replay checked all twenty arms/200 events. Decimal verification checked 400 source labels including reused prefixes, 600 paired metrics, 120 family metrics, 60 aggregate metrics and 30 win/tie/loss counts.
- All 2,242 frozen historical/current input references pass integrity checks. Figure visually inspected. No jobs are running or scheduled.

## Result and interpretation

Adaptive shortlist centroid beats both full-space and shortlist random expectations in both family averages under both normalized and relative target metrics. Shortlist random is 6.83253% worse relative to that comparator in exact expectation; full-space random is 10.85800% worse. These percentages average paired target ratios, not deployment speedups.

Observed random outcomes are separate: full random has 0 wins/4 ties/6 losses against adaptive shortlist centroid; shortlist random has 1/5/4. Restricting to the shortlist improves expected loss on both families, but the actual shortlist draw is worse than the full-space draw on Z3. Exact probabilities are conditional finite-pool mathematics, not p-values or confidence about new systems.

The nine zero-headroom cases and remaining 0.131810% maximum gain imply an equal-family hindsight ceiling of 0.013181% over this comparator, before inference cost. This conclusion is conditional on the frozen shortlist and prefix. It does not cover full-domain proposals or prove LLM inferiority. No new LLM behavior, learned routing, application-quality guarantee, noise estimate or independent-system generalization was tested.

## Commands and evidence

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_random_v31.py
.venv/bin/python scripts/analyze_random_v31.py
.venv/bin/python scripts/analyze_random_v31.py --verify-only
.venv/bin/python scripts/verify_random_v31.py
.venv/bin/python scripts/audit_history_v30.py
```

The last three commands are read-only verification. Collection/analysis refuse completed outputs.

- `results/v31_random/`: raw acquisitions, twenty arms/checkpoints, progress, summary, cases/pairs CSV, PNG/SVG figure; exact distributions explicitly labeled as evaluator references.
- `artifacts/study_v31/`: executed logs, tests, collection/analysis costs, Decimal/exhaustive verification (including each hindsight ceiling), replay, historical integrity and final checks.
- `src/escalation/random_v31.py`: ID-only sampler and charged continuation.
- `reports/protocol_v31_random.freeze.json`: frozen inputs.
- `artifacts/history/v31_before_execution/`: prior STATUS/README and ledgers.
- V26 ZIP unchanged; remains a V25 reconstruction snapshot, not a V31 bundle.

No experiment or verification failures occurred. The historical audit uses the V30 wrapper that explicitly checks the archived pre-download ledger plus the append-only paper download; this preserves the original V22 identity checks.

## Costs and next action

Added collection/analysis runtime: 2.473465166 seconds. Cumulative runtime: 2,268.086494921 / 3,600 seconds; 1,331.913505079 remaining; active_since null. New recorded accesses: 200; historical total: 8,308. Physical trials: 1,134 unchanged. Prefix cost already charged in V30. Across both random methods, 400 logical evaluations; one-method deployment across ten cases would use 200 and zero inference calls.

Follow-up model allowance remains 200/200 exhausted (300 including initial stage). No new allowance inferred. No downloads; byte ledgers unchanged. External spend USD 0. No cloud, remote push, publication or contact.

**Single next action:** define a quality-constrained task and establish usable headroom on development data, then freeze the strong classical comparisons and reserve untouched software families for evaluation. Do not screen future test groups by outcomes or spend new inference on these same nearly saturated shortlists. Actual fresh inference requires a new bounded allowance or compatible provenance-checked cache. Preserve the original negative/insufficient router finding and the mixed V30 transfer result.
