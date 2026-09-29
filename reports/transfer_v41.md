# V41: six new families, classical transfer executed

This is new measured recorded-table evidence, not a new LLM result. Six families previously unacquired in the local study passed source/schema/exposure checks: BerkeleyDB C, Dune, LLVM, HIPAcc, SaC and OpenVPN. Five fixed seeds, 30 shared prefixes and seven classical continuations each completed. All 210 arms used exactly 20 logical evaluations including the same ten-label prefix. All 2,400 newly acquired scalar outcomes are journaled. Source targets were replayed only for already acquired rows.

The strongest useful new observation is that full-domain sequential 3NN improves the equal-family mean relative to the batch-shortlist 3NN reference by **1.415%**, with **8 wins, 16 ties and 6 harms** across 30 paired cases. Its six-family bootstrap interval is **[0.062%, 3.290%]**, while the exact family sign-flip p-value is **0.15625**. The different summaries and only six groups do not justify a strong significance/generalization claim. This establishes a concrete stronger control that any proposed LLM benefit must survive. It does not establish an LLM benefit.

| Classical continuation | Mean gain vs batch 3NN | Wins / ties / harms |
|---|---:|---:|
| full_classical | -0.694% | 5 / 20 / 5 |
| static_rank | -0.562% | 1 / 22 / 7 |
| batch_3nn | +0.000% | 0 / 30 / 0 |
| sequential_3nn | +0.061% | 2 / 28 / 0 |
| full_sequential_3nn | +1.415% | 8 / 16 / 6 |
| random_shortlist | -1.662% | 3 / 21 / 6 |
| random_full | -2.005% | 6 / 11 / 13 |

All comparisons use relative improvement in the acquired best target, with equal family weights. OpenVPN maximizes throughput; other targets minimize time. Family breakdowns, uncertainty summaries, all 210 cases and a reproducible figure are in `results/v41_transfer/`. No family/seed was removed for a bad score. No overall best optimizer claim is made from seven descriptive contrasts.

## Actual collection and validation

Collection/token preflight charged 9.782281s; replay/analysis/rendering charged 19.103170s. New inference: zero. New physical trials: zero. USD0 external spend. Three primary documents downloaded under the existing persistent cap (899,606 bytes); no model or dataset download.

285 tests pass (264 existing plus 21 new). New tests cover minimization/maximization, paired-state isolation, deterministic arms, target parsing/charging, exact budgets, byte-equivalent prompt content, subset selection and fail-closed authorization. All 30 prefixes, 210 arms and 2,400 acquisition events replay exactly against recorded acquired targets. Figure visually inspected. The real-model entrypoint was executed as an authorization-gate check and refused before model startup; this expected failure is saved, not called successful inference.

The default pytest configuration only discovers `tests/synthetic`; run the explicit command below to include the new frozen V41 tests. Their fixtures are synthetic test data and never enter the measured directory.

```sh
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/analyze_transfer_v41.py
```

The collector is intentionally one-shot and refuses an existing measured directory. A fresh-workspace reproduction uses the pinned source manifest and protocol freeze, then `scripts/run_transfer_v41.py`. Analysis reuses measured labels; it does not charge new objective acquisition. Reanalysis still counts computational runtime.

## Concrete next model experiment

All 60 actual saved prompts pass both installed tokenizers: 897–3302 input tokens, below the frozen 4,096 cap. Requests are blocked at 230/230. The prepared runner requests exactly 60 additional local calls, 30 per installed model size (0.5B/1.5B), cumulative cap 290, no retries, 600 maximum new recorded outcomes, a 700-second stage inside the unchanged 3,600-second global allowance, no downloads and USD0. Remaining global runtime after this work: 1039.586041s. Actual runtime is unknown until execution; 700s is a cap, not a forecast guarantee.

The model comparison, all classical controls, prompts, candidate mapping and old-router transfer policy were frozen before acquiring new outcomes. Classical outcomes are now exposed. No treatment/threshold changes based on these results are permitted within this prospective protocol. Both models share the Qwen family, so even a completed positive result would not establish generalization across model families.

## What this still does not establish

Not yet sufficient to call the research Q2-ready. Important gaps remain: no V41 LLM evidence or useful unseen-system routing result; only six newly admitted groups; source benchmark age and possible pretraining exposure; nominal representations; fixed feature-only subsampling; unresolved DeepPerf data redistribution license; unknown equality of application quality/security/services and measurement noise. A recorded-target optimization advantage is not necessarily application utility. Dune problem size is fixed, but numerical accuracy was not measured. VPN settings are not security recommendations. All original source tables remain local and ignored.

Prioritized next work: (1) execute the frozen real-model continuation under an exact bounded extension; (2) assess whether any gain survives full-domain 3NN and costs across families, retaining negative findings; (3) if signal exists, collect independent model-family and application-utility/correctness evidence under a new protocol; (4) obtain scientific feedback on the narrow contribution against the close prior work before journal targeting. Do not repeatedly tune these six now-exposed families until a favorable outcome appears.
