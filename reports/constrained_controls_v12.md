# Actual constrained controls: a small, mixed classical result

A new classical-only experiment completed all20 intended continuations on ten development prefixes, using runtime and output size jointly. The cheap three-nearest-neighbor optimizer improved average relative feasible runtime versus random continuation by **4.82% on lrzip**, worsened it by **2.79% on Brotli**, and improved it by **1.01% across the two equally weighted families**. These are exploratory point estimates; neither statistical significance nor LLM benefit is established.

This is actual recorded-table optimization with charged acquisitions, not a hindsight upper reference. The aim was to test whether the quality-constrained opportunity in V11 remains after a cheap optimizer is given the same information. It was not tuned until a positive aggregate appeared: one specified method, one random control, all fixed cases, no hyperparameter search, both gains and losses retained.

## Fixed setup and execution

Use Brotli0.3.0 and lrzip530, five seeds [11,23,37,53,71]. Reacquire the same original ten prefix row IDs as runtime/size vectors, charging each vector once. The original runtime-only history remains recorded separately. The fastest prefix row's output size defines a fixed zero-slack cap. Each continuation acquires ten more vectors from the full feature table, preserving inclusive20/configuration budget. Both branches start from exactly the same joint prefix and use independent state.

The adaptive cheap method predicts mean runtime and size from each candidate's three nearest acquired rows in nominal feature distance. It chooses the lowest predicted-runtime candidate predicted to satisfy the cap, with frozen deterministic tie rules; if none is predicted feasible, it chooses smallest predicted size. It acquires the true pair before updating. Random continuation follows the next available row of the original seeded order. No hidden-size feasibility prefilter, unobserved objective scaling, model requests or reliability probes are used.

Both branches return their fastest actually acquired feasible configuration; a feasible prefix incumbent is always retained. Actual new accounting:100 shared prefix vectors +100 cheap continuation vectors +100 random continuation vectors = **300 charged configuration-vector accesses**. These revisit authors' recorded tables and are not300 newly executed live software measurements. Ten vectors per continuation are additional to its logical ten-prefix budget.

## Complete results

| Family | Cases | Mean relative gain of cheap optimizer over random | Wins / losses / ties | Remaining ideal feasible gain above10% |
|---|---:|---:|---|---:|
| Brotli | 5 | -2.79% | 2 / 1 / 2 | 2/5 |
| lrzip | 5 | +4.82% | 4 / 0 / 1 | 0/5 |
| Equal-family aggregate | 10 | +1.01% | 6 / 1 / 3 | 2/10 |

Both methods acquired17 size-infeasible rows among their100 new continuation acquisitions. These remain charged, and both retained feasible incumbents. No run failed, disappeared or used a fallback. The full per-seed outcomes are in `results/v12_controls/outcomes.csv`.

After the cheap optimizer, the full-table hindsight runtime headroom averages **0.37% on lrzip** and **9.09% on Brotli**. The remaining above10% opportunities are concentrated in Brotli, not broadly available across independent systems. Hindsight gains are not achieved optimizer gains and use hidden labels only retrospectively. Measurement uncertainty is not available at the paired-run level; effects such as the1.01% aggregate cannot be called reliable improvements from these data alone.

## What can be claimed

The positive observation is limited: this particular cheap, size-aware method beat its matched random control on the lrzip cases and on the two-family average. It did not win consistently across systems and is not claimed state of the art. The controls show why a fair LLM comparison needs a quality-aware cheap baseline: much of the lrzip headroom seen against old runtime-only search disappears when a cheap method uses the joint outcomes.

This does not satisfy a claim that an LLM is worth calling or that a benefit router works. The historical LLM still chose the first ten displayed IDs in all15 direct-selection cases. Its apparently favorable scores are exactly reproducible by a model-free rule. V11's oracle opportunities and V12's cheap-method gains must not be relabeled as positive LLM results.

I do **not** recommend continuing to swap models on these cases until a favorable score appears. Before broader routing research, the task/metric setup needs more independent, source-validated systems with headroom beyond strong cheap constrained controls and a prospectively justified practical margin. New models or evaluation groups would be a new bounded experiment; their success cannot be promised.

## Verification and evidence

**95 tests passed.** Independent deterministic replay recomputed every online candidate choice using only the recorded acquired joint labels, validated all300 source-vector accesses, checked shared prefixes, size caps, 20-label budgets, preserved failure denominators and feasible incumbents. All prior scientific freezes remain intact.

- Frozen specification: `reports/protocol_v12_controls.md` and `.freeze.json`.
- Raw charged vectors: `results/v12_controls/acquisitions.jsonl`.
- Shared prefixes, actual branches and checkpoints: `results/v12_controls/prefixes/`, `joint_3nn/`, `random/`, `checkpoints/`.
- Full denominator: `results/v12_controls/progress.json` (20/20 completed).
- Numerical results: `results/v12_controls/summary.json` and `outcomes.csv`.
- Execution and verification: `artifacts/study_v12/collection.log`, `analysis_verification.log`, `verification.json`, `tests.log`.
- Acquisition code: `src/escalation/quality_controls_v12.py`; collector `scripts/run_quality_controls_v12.py`.
- Offline replay/evaluator: `scripts/analyze_verify_quality_controls_v12.py`.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_verify_quality_controls_v12.py
```

The replay/evaluator makes no inference requests or optimizer acquisitions but records computation against the experiment-runtime ledger. Collectors reuse completed cases and fail closed on interrupted transactions. No old output or ledger was reset. No packages/models were downloaded, no money spent, and no publication or contact occurred. The model request cap remains128/128; additional real inference needs a separate explicit allowance.
