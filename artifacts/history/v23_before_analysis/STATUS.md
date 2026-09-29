# Status — 2026-09-24 America/New_York: V22 executed and verified

## Resume here

The exact approved extension **actually completed60/60 real local-model calls and90/90 deterministic control arms**, with1500 new charged recorded-label acquisitions and no failures,retries,timeouts,fallbacks or omitted cases. Read [the current report](reports/larger_model_v22.md) and [next priorities](reports/next_experiment_v22.md). No useful benefit router or cost-justified LLM policy is established.

Equal-family mean normalized-loss gain: **+0.00426143 versus saved classical**, **+0.00019175 versus first-displayed-ten**, +0.00093106 versus exact uniform expectation. Most gain comes from MySQL. On lrzip the LLM is worse than both rule controls and uniform expectation. These are descriptive development results, not percentages of runtime saved or a held-out router finding.

All15 exact repeats matched. Reversing display changed selected configuration sets in12/15 cases; ID reassignment also changed12/15. First-displayed-ten matches25/45 unique selections; lowest IDs matches0/45. Repeatability does not imply presentation invariance or practical utility.

## Actual execution and checks

Pinned Qwen/Qwen2.5-1.5B-Instruct revision989aa7980e4cf806f80c7fef2b1adb7bc71aa306;CPUfloat32,four threads,greedy,20 generated tokens under the frozen distinct-ID grammar. All nine owner files downloaded and passed pinned size/hash checks; actual model loading succeeded. No fabricated responses or paid/cloud inference.

MySQL/lrzip/Brotli × seeds11,23,37,53,71;the same15 saved ten-evaluation prefixes. Three unique presentations and one exact repeat per case.90 controls +60 model arms each retain the prefix and acquire10 outcomes to finish at20. The separate evaluator uses full-table labels only retrospectively. No held-out families or controller fitting added. Frozen protocol pending wording is historical; separate authorization/start records prove approval preceded execution.

Executed successfully:

```sh
.venv/bin/python -u scripts/fetch_model_v22.py
.venv/bin/python scripts/run_larger_v22.py --preflight
.venv/bin/python -u scripts/run_larger_v22.py
.venv/bin/python scripts/analyze_larger_v22.py
.venv/bin/python scripts/verify_report_larger_v22.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
```

**156 tests passed in1.09seconds.** Independent verification checked60 tokenizer/grammar/cache/provenance replays,150 arm/prefix/source-label replays,1500 journal acquisitions,150 scalar losses and all family aggregates/repeats. Read-only replay passed. All20 scientific freezes/1306 references intact. Figure visually inspected. Synthetic tests remain separate. Audit/figure code is explicitly post-collection and leaves frozen selection/analysis code untouched.

## Evidence

- [Current report](reports/larger_model_v22.md), [outcomes](results/v22_larger/outcomes.csv), [summary](results/v22_larger/summary.json), [figure](results/v22_larger/verified_comparison.png).
- Raw prompts/responses/tokens/usage: results/v22_larger/requests.jsonl and request_starts.jsonl.
-150 arms/checkpoints and1500 label journal entries: results/v22_larger/arms/,checkpoints/,acquisitions.jsonl. Complete intended denominator: progress.json.
- Prospective design: reports/protocol_v22_larger.md and .freeze.json;data/larger_probe_v22.json;data/manifest_v8.json.
- Permission and start: configs/authorization_v22.json;results/v22_larger/started.json. Model provenance: artifacts/model_manifest_v22.json and artifacts/study_v22/model_download_plan.json.
- Command logs: artifacts/study_v22/download.log,inference.log,analysis.log,verification_presentation.log,read_only_verification.log.
- Test/check/cost receipts: artifacts/study_v22/post_execution_tests.json,execution_verification.json,scientific_freeze_verification.json,executed_accounting.json,executed_evidence.json.
- Previous mutable docs, pending authorization and pre-execution ledgers: artifacts/history/v22_before_execution/. Its STATUS.md preserves the full older chronology.

PDF and ZIP in output/ remain **V21 historical review snapshots**, excluding V22. Do not present them as current. Prior scientific results and failures remain unchanged. Resume from this file and current report, not the long initial research report.

## Costs and limits

Actual60 requests:95,720 input/1,200 output tokens,missing usage0;431.6949seconds summed request wall. Startup8.5656seconds includes4.4935seconds model loading. Execution,analysis,audit/plotting added458.2772 experiment seconds. Download separately74.1449seconds and3,098,971,928bytes. External spendUSD0;electricity/hardware monetary cost unmeasured. A hypothetical15-case one-presentation deployment uses300 logical evaluations and15 always-escalate calls, distinct from actual collection.

**200/200 follow-up requests exhausted**;300 including initial100. Runtime **2248.9888/3600seconds**,1351.0112remaining;active_since null. History6908 recorded-objective accesses and1134 separate physical trials. Cumulative downloads4,514,296,954total /4,098,574,535model bytes,within5GiB/4GiB caps. No active workers/scheduled tasks. No further calls authorized; preserve ledgers and completed guards.

Initial owner download hit sandbox DNS then succeeded after network escalation. No inference/analysis failures. Transformers sliding-window/SDPA and ignored sampling-parameter warnings remain in logs. Model use_sliding_window:false and32768window exceed maximum1792 observed total tokens; settings unchanged. Other backend equivalence untested. A documentation patch was rejected for targeting STATUS twice; it changed no file, and a normal replacement succeeded.

## Earlier evidence and remaining uncertainty

V3 completed corrected three-system/five-seed smoke after preserved V1/V2 schema errors. V6 implemented all requested routing policies with group splits: three held-out families showed no benefit-router advantage and development-tuned policies escalated zero times. V8/V9 and V19–V21 exposed selection/presentation effects. V15–V18 physical compression work found little remaining headroom. Exact SNAP2 code was not located in the bounded primary-source audit; implementations remain adaptations,not numerical replication. Conditional escalation alone is not an established novelty claim.

V22 does not turn those findings into routing success. Historical0.5B/current1.5B conditions differ,so no model-size causal claim. Three exposed families do not support significance/generalization. Untested:fresh-host reproduction,peak memory,application-grounded cost/quality thresholds,untouched-system validation,and useful live routing.

## Single most important next action

**Review V22 with Tim and decide whether its small advantage over cheap selection controls warrants a prospective held-out study.** Agree on practical utility/cost thresholds and eligible independent tasks before more model/router collection. Nothing emailed,published,pushed or submitted;no additional campaign queued. The positive mean is not authorization to search until it grows.

Safe read-only continuation: tests and scripts/verify_report_larger_v22.py --verify-only. Older verify_review_current.py assumes the140-call snapshot;retain its old receipt instead of resetting today's ledger. Collection/analysis refuse completed outputs.
