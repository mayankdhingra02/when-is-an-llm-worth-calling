# STATUS — V84 H2 classical comparison completed

## Resume here

Read `reports/h2_v84.md` and the frozen `reports/protocol_v84.md`. All **165 native trials completed and validated** in 683.521 seconds. Five fixed seeds each have an immutable 10-evaluation prefix. RF and random continuations each used 20 logical evaluations, including three fresh confirmations; the standalone indexed baseline used only three evaluations.

Neither search method improved over the baseline by the predeclared 10% margin in any seed. Mean query times were 0.69% worse for RF and 0.30% worse for random. All comparisons passed the coarse repeat-precision screen; this does not establish statistical equivalence. This is one exposed H2 development family and a generated workload. No H2 LLM treatment, held-out result, positive router or Q2-readiness claim exists. No experiment remains running.

## Evidence and actual verification

Raw charges, commands, settings, indexes, exact answers, process receipts, saved prefixes and locked incumbents: `results/v84_h2_classical/`. Analysis and inspected figure: `results/v84_h2_analysis/`. Findings and costs: `artifacts/study_v84/`. The frozen analyzer reconstructed every acquired-only RF/random decision, shared prefix, round order and budget, and independently checked 1,013,760 scored query answers.

The full explicit suite passed 608 tests before collection (`artifacts/study_v84/tests_all.log`). Synthetic fixtures are excluded from measured results. The initial sandbox process-inspection denial occurred before collection; the identical command then ran with permission. There were no failed native trials or retries.

Executed `run_h2_v84.py`, `analyze_h2_v84.py`, `write_h2_v84_report.py` and `bundle_h2_v84.py`. Portable archive: `output/h2_v84_outcome_reconstruction.zip`, 3,426,268 bytes, SHA256 `040ffd81bb67741aa5d595fa073b21ad9c44b58b15401a098bc1475a63bb0fa3`. Extract and run `python3 -I -S scripts/replay_h2_v84_portable.py`. Actual isolated Python 3.10.13 replay passed; metric, budget and denominator corruptions were rejected even after updating their file hashes. Receipt: `artifacts/reproduction_v84/verification.json`. This reconstructs saved outcomes; it does not rerun Java, RF selection, the model or a clean machine.

Current evidence/history check: `.venv/bin/python scripts/seal_h2_v84.py --verify-only`. Root document history is preserved in `artifacts/study_v84/previous_snapshot/`. Do not rewrite frozen evidence. `reports/novelty_boundary_v84.md` records primary-source checks of related hybrid optimization and model-capacity work; `reports/readiness_v84.md` audits the broader research goal. No external study code was executed.

## Costs and remaining limits

New physical trials: 165. Cumulative H2: 184, comprising 183 validated trials and one historical V81 validation failure; eight historical unattempted slots remain recorded. V84 logical charges: 215 (200 RF/random and 15 prior), because 50 shared-prefix physical trials are reused once logically. Native process time: 678.352 seconds; policy-selection time: 1.795 seconds. Runner time includes validation/checkpoint overhead but excludes initial setup and later analysis. The 1,800-second and 165-trial caps were respected.

No new model calls, artifact downloads or external spending. Cumulative model calls: 2,156. Downloaded artifact bytes: 4,817,487,882; 551,221,238 remain under 5 GiB. Prior Kanzi 1,265 and RocksDB 350 physical trials, and 26,358 recorded-table acquisitions, are unchanged. Electricity/hardware costs are unknown. Modeled index amortization excludes loading, warm-up and tuning; it does not establish production savings.

V80 remains 105 real SmolLM3 calls and 450 valid trials: zero wins, ten ties and five losses against its cheap preset, with 9.852 seconds extra decision time per case. See `reports/kanzi_v80.md`. That inference allowance is consumed; no new model batch is frozen or authorized here. Bounded preparation/classical work remains available; no paid/cloud/push/contact permissions.

## Single most important next action

Prepare a bounded same-model H2 paired continuation study from these five saved prefixes, with fresh classical controls while the model is resident, explicit query context, and the cheap prior retained. Freeze and review the exact request/resource scope before consuming any new inference allowance. A classical result alone cannot establish that an LLM adds no value.

Still missing: real H2 LLM continuation, sufficient independent held-out paired benefit evidence, practical deployment utility, stronger-model robustness, clean-machine native replication and defensible novelty. More seeds on this simple workload do not close those gaps. Keep the full research objective active.
