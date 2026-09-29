# STATUS — V99/V100 timed out; V97 remains the latest complete comparison

The user's “try now” was acted on. Tools executed successfully. Local Qwen3 inference remained too slow for the frozen request deadline. Both new attempts are preserved separately; neither is a model-quality result.

## What actually ran

- **V99:** context reduced from 6144 to 4096; same 36-condition order and model/method as V98. One charged request timed out at 120 seconds, zero responses; 35 conditions unattempted. Lifecycle 130.239 seconds; peak sampled model RSS 5,769,822,208 bytes. Cleanup escalated from SIGTERM to SIGKILL after three seconds, exit -9. No retry. All 36 intended policy arms were retained through explicit classical fallback with 360 charged recorded-table accesses. Saved-evidence replay verified every acquisition. Its -2.5752% mean versus sequential 3NN is entirely fallback behavior, not LLM performance.
- **V100:** separately frozen two-condition feasibility test with the documented `--load-mode none`, keeping 4096 context and other server settings. Caps were reduced to three requests, 768 allocated tokens, 600 seconds, zero objective acquisitions; 120-second requests and 8 GiB RSS guard unchanged. One charged request again timed out before returning an answer; the thinking condition was unattempted. Lifecycle 139.723 seconds; peak sampled model RSS 5,802,639,360 bytes; cleanup exit -9. Feasibility criterion failed. No retry or new objective acquisition.

Each attempt allocated 128 output tokens, but actual total output/prefill usage is unknown because no response returned. Incomplete server progress is not a completed token-usage record. Zero returned-response sums must not be reported as zero actual generation. No fabricated answers, new downloads, paid/cloud use, application closures, or system-setting changes. A read-only process check confirmed the owned model server exited.

V99's empty response journal was initialized after shutdown with an explicit receipt; V100 initialized its empty journal before collection. Both contain zero invented response entries. The saved-evidence V100 audit passed, and report rendering is checked for byte-identical replay. All 771 tests passed: the configured synthetic suite had 744 passes in 93.41 seconds; the 27 additional root/integration tests passed in 0.48 seconds. Logs: artifacts/study_v100/tests.log and tests_additional.log. Three new request/token-guard tests passed before inference. V99's figure was inspected; its right panel describes fallback-only policy behavior.

## Evidence and reproduction

V99: `results/v99_reasoning/`, `results/v99_analysis/`, `artifacts/study_v99/`, `reports/research_readiness_v99.md`. Protocol freeze SHA 695bfa304f4a8fbd617acbba7f2262c8ba950976bf987c8b6ad3082cfe2fc710. Its evidence manifest SHA b6a5294b450cabe0e962a1c9b25060a5efc533ad350f272783c645253a32ce94 sealed 124 files and 37 historical checkpoints before the new root-document snapshot.

V100: raw requests, errors, ledger, prompts and runtime log in `results/v100_reasoning/`; independent audit in `artifacts/study_v100/feasibility.json`; readable report `reports/feasibility_v100.md`. Protocol freeze SHA 73ad9cd1a67874128907a266b6618acbd04018afa0b7c45b494bad08aaa57615 pins 63 files including weights/runtime and inherited method. Prior root documents are in `artifacts/study_v100/previous_snapshot/`.

Safe saved-evidence replay, with no model calls or new labels:
```
.venv/bin/python scripts/audit_feasibility_v100.py
.venv/bin/python scripts/report_feasibility_v100.py
.venv/bin/python scripts/seal_reasoning_v100.py --verify-only
```
Do not rerun once-only collectors or V99's charged analyzer into existing outputs. Use the latest snapshot-aware sealer after root-document changes; historical standalone seals need their preserved document versions.

## Cumulative cost and scientific limits

Real model requests: **3,897**. Recorded-table acquisitions: **27,738**. Native numerical configuration acquisitions: 790 across V94/V96/V97; physical repetitions counted separately. Older native counts unchanged (DuckDB 78 physical, H2 299, Kanzi 1265, RocksDB 350). Downloads 9,870,221,104 bytes / 10 GiB, leaving 867,197,136; model payload 9,126,358,023 bytes / 9 GiB unchanged. External spending zero; electricity/hardware cost unknown. Actual research collection cost is not deployment cost.

V97 remains the latest completed optimization comparison: 250 valid native acquisitions, 50 valid local model calls, mean LLM gain -1.52% versus batch 3NN, -2.77% versus sequential 3NN and +12.62% versus random; zero >=5% wins against either strong control in five exposed SuperLU seeds. Neither useful benefit prediction, reserved-final-answer reasoning quality, independent-machine replication, nor Q2 readiness is established.

**Single next action:** save work and restart the Mac, then leave only research tools open so a separately frozen feasibility check can test a fresh session. This is a proposed intervention, not a proven fix; the agent has not rebooted the machine. Do not run another unchanged full batch in the current session. No second host is connected. See `reports/next_experiment.md` for the bounded follow-up and remaining scientific needs.
