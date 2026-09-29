# V78: real local-model continuation on Kanzi

The approved batch completed all **35 real SmolLM3 requests and 150 new physical trials**, with no invalid responses, retries, fallbacks or failed trials. On this one generated workload, the LLM beat RF-LCB on two of five seeds but produced **1.33% larger files on average**, adding **9.83 seconds of decision time per seed**. It beat 3NN on four seeds and reduced mean size by 2.89%. These mixed results do not establish a useful escalation controller or Q2 readiness.

## Frozen comparison and actual execution

User approval is recorded in `artifacts/study_v78_execution/user_approval.json`. The original [protocol](protocol_v78.md) and freeze remain unchanged (SHA256 `59766c399b902a0e9f9eb5f785e2eb5350e383810e368de53467fce3a3bdd440`). Execution began at 2026-09-26 05:58:12 UTC and ended at 06:06:16 UTC. A sandbox process-inspection denial occurred before collection; the identical command then ran with execution permission and exited successfully. No experiment retry occurred.

Five fixed seeds (11, 23, 37, 53, 71) reused the saved V77 ten-evaluation prefixes. RF-LCB, 3NN and LLM each received seven new search evaluations and three charged incumbent confirmations: 20 logical evaluations per arm. This is 300 logical charges including shared prefixes, with 150 new physical trials (105 search, 45 confirmation) and 50 historical prefix trials reused. Model residency was maintained for every fresh arm; round order was randomized prospectively. Optimizers used acquired labels only. No new controller was fitted.

The workload is the same fixed generated 16 MiB input, with 448 canonical candidates. Distinct effective behavior for every candidate is not established. Kanzi 1.9 uses the isolated V76 buffer-reference repair and is explicitly an **adaptation**, not an unmodified release. Every trial passed stream checksum, independent header/settings verification and exact decompression. All three confirmation sizes agreed in every case. Successful bulky payloads were removed under the prospective retention rule; hashes, logs and receipts remain. Offline replay verifies those receipts, not the deleted payload bytes anew.

## Confirmed results

Lower compressed byte count is better; cells are medians of three charged confirmations.

| Seed | RF-LCB bytes | 3NN bytes | LLM bytes | LLM versus RF |
|---|---:|---:|---:|---|
| 11 | 4,751,282 | 5,529,352 | 5,147,315 | 8.34% larger |
| 23 | 5,739,996 | 5,739,996 | 5,147,315 | 10.33% smaller |
| 37 | 4,976,391 | 4,686,563 | 5,150,518 | 3.50% larger |
| 53 | 4,686,563 | 5,302,168 | 5,147,315 | 9.83% larger |
| 71 | 5,248,371 | 5,248,371 | 5,147,315 | 1.93% smaller |
| Mean | 5,080,520.6 | 5,301,290.0 | 5,147,955.6 | 1.33% larger |

The primary descriptive mean comparison uses the ratio of mean byte counts. Mean per-seed percentage savings is a different statistic: −1.883% versus RF and +2.436% versus 3NN. All comparisons exceeded the predeclared absolute 1% descriptive margin; this margin is not a significance test or a business utility valuation. Seeds are repeated searches within one family, not independent systems. No population confidence or significance claim is made.

The hindsight better-of-RF-and-LLM mean is 4,941,773.2 bytes. This nondeployable diagnostic uses terminal outcomes; it is neither a trained policy nor evidence that pre-decision features can identify the winners.

![Paired quality and decision costs](../results/v78_kanzi_analysis/paired_results.png)

## Post-hoc alternative explanation

All four model-derived incumbents are candidate 439: `LZP+TEXT+BWT+LZP`, `CM`, 2 MiB blocks, one job. The transform/entropy pair matches the owner's level-7 preset in the pinned `BlockCompressor.java`; block size is a separate choice. All 16 observed physical trials at this candidate produced 5,147,315 bytes and the same output hash. Seed 37 retained its prefix incumbent instead.

This acquired-only diagnostic is post-hoc. It suggests that a cheap preset-and-block strategy could explain the observed gains. It does not prove that strategy's unmeasured performance or identify the model's internal mechanism. No missing outcomes were fabricated. A prospective cheap-preset baseline on independently chosen new workloads is the most important next experiment.

## Actual collection and modeled deployment costs

Collection took **483.97 seconds**, below the 1,800-second cap, with 300 new JVM application processes. There were 35 generation calls and 109 total HTTP requests including health/template/tokenization operations. Observed usage was 20,760 input tokens and 326 output tokens; no request had unknown usage. Server startup took 0.770 seconds; sampled peak server RSS was 2,389,196,800 bytes. No downloads or external monetary spending occurred; electricity and hardware costs are unknown.

Total selection time across five seeds was RF 1.049 seconds, 3NN 0.0127 seconds, LLM 50.211 seconds. The 9.83-second average increment versus RF is decision overhead, not total deployment time. Native continuation trial supervision totaled 431.525 seconds, including collection checks.

`deployment_estimates.json` separately accounts for a hypothetical single selected branch using recorded prefix process times, continuation wall time and selection time, with model startup separate. It excludes prefix verification/I/O and router overhead, and uses controls collected with the model resident. It is retrospective accounting, not a measured deployed controller or a dollar-cost estimate. Actual research collection paid for all three continuations; never treat the hypothetical selected branch as the amount actually collected.

Model: SmolLM3-3B-Q4_K_M, revision `4965cb60b150737b68a0408c36aeefb65078f894`, GGUF SHA256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`, local llama.cpp b11146. Runtime/model/configuration pins, prompts, raw completions and usage receipts are preserved. The completed batch exhausts its 35-call allowance; there is no continuing background experiment.

## Evidence, reproduction and limits

- Raw measurements, selection decisions and real model responses: `results/v78_kanzi_paired/`.
- Verified tables, JSON, deployment accounting and figures: `results/v78_kanzi_analysis/`.
- Post-hoc preset diagnostic: `results/v78_preset_diagnostic/summary.json`.
- Approval, costs, test receipt and supplementary verification: `artifacts/study_v78_execution/`.
- Both the frozen analyzer and supplementary accounting verifier passed on the real outputs. The full repository suite passed: **580 tests in 3.92 seconds**. Synthetic fixtures are excluded from measured aggregates.

Read-only evidence/history verification:

```sh
.venv/bin/python scripts/seal_v78_execution.py --verify-only
```

Analysis commands used were `scripts/analyze_kanzi_v78.py`, `scripts/verify_kanzi_v78_addendum.py`, `scripts/report_kanzi_v78.py` and `scripts/diagnose_kanzi_v78.py`, all with `.venv/bin/python`. Regenerate outputs in a separate repository copy after sealing; do not overwrite sealed artifacts. The executed collector was `scripts/run_kanzi_v78.py --approved-envelope-sha256 59766c399b902a0e9f9eb5f785e2eb5350e383810e368de53467fce3a3bdd440`; replaying collection requires a separately bounded allowance and fresh output namespace.

This is one generated input, one development family, one model and a patched runtime on one host. Reliability observed here does not imply zero failure probability elsewhere. No real-workload transfer, independent family-level test, useful fitted router, clean-machine V78 reproduction, or cost-benefit preference elicitation was completed. The previous same-model RocksDB result was negative against both controls on all five seeds; its milliseconds must not be pooled with these bytes. Earlier router experiments and historical reproduction bundles retain their own scopes. The research has a concrete mixed finding, not yet a defensible claim of broadly beneficial LLM escalation.
