# V22 executed: larger local model with presentation controls

The fixed experiment completed all **60 real local-model calls and 90 deterministic control arms**, with no retries, malformed responses, timeouts, fallbacks or omitted cases. There is a small positive descriptive quality difference against the saved classical continuation, concentrated in MySQL. The advantage over the first-displayed-ten control is much smaller. This does **not** establish useful benefit-aware routing or a cost-justified LLM policy.

The [protocol](protocol_v22_larger.md) and its 135-reference freeze preceded V22 responses. Its pending-authorization wording is a preserved historical snapshot; [separate authorization](../configs/authorization_v22.json) records the user's subsequent approval. This is an adaptive development follow-up to earlier exposed results, not a fresh held-out test.

## Executed design

MySQL, lrzip and Brotli; seeds 11, 23, 37, 53, 71; the same 15 saved ten-evaluation prefixes. Every completed arm retains that prefix and acquires ten additional recorded outcomes, for an inclusive budget of 20. Forty-five distinct prompts cover nonmonotone assigned IDs, reversed display with the same mapping, and independently reassigned IDs. Fifteen byte-identical repeats follow. The 90 controls select the first displayed ten or canonical lowest ten IDs; repeats reuse their explicitly attributed original control outputs. All 1,500 new recorded-label acquisitions remain charged, including repeated selections across arms.

Actual model: Qwen/Qwen2.5-1.5B-Instruct, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, CPU float32, four threads, greedy decoding, unchanged ten-distinct-ID grammar, 20 output tokens per request. All nine downloaded owner files passed pinned size and Git-blob/LFS hash checks. See [model manifest](../artifacts/model_manifest_v22.json). No fabricated or cached substitute supplied these responses.

## Quality results

Lower normalized terminal loss is better. Primary means average the three unique presentations and five seeds within each family, then weight the three families equally. Exact repeats are excluded from quality means but included in costs. Full-table extrema are used only in retrospective scoring. These normalized-loss differences are **not percentages of runtime saved**.

| Family | Classical | Uniform expectation | First displayed | Lowest IDs | LLM |
|---|---:|---:|---:|---:|---:|
| Brotli | 0.00068959 | 0.00046498 | 0.00047093 | 0.00043460 | 0.00046855 |
| lrzip | 0.00139187 | 0.00102427 | 0.00111147 | 0.00107500 | 0.00124491 |
| MySQL | 0.04465970 | 0.03526081 | 0.03294972 | 0.04726159 | 0.03224341 |

Equal-family mean gain, defined as baseline loss minus LLM loss: **+0.00426143 versus classical**, +0.00093106 versus uniform expectation, **+0.00019175 versus first displayed**, +0.00493810 versus lowest IDs. MySQL accounts for most of the aggregate gain. On lrzip the LLM is worse than both rule controls and the uniform expectation; on Brotli it is worse than uniform expectation and lowest IDs. Uniform is the previously computed exact retrospective ten-of-twenty expectation, not a newly collected random arm.

Every family and unique presentation is retained below (five-seed mean). All individual outcomes are in [outcomes.csv](../results/v22_larger/outcomes.csv).

| Family | Presentation | LLM | Classical | Uniform | First displayed | Lowest IDs |
|---|---|---:|---:|---:|---:|---:|
| Brotli | Assigned | 0.00049911 | 0.00068959 | 0.00046498 | 0.00049911 | 0.00041864 |
| Brotli | Reverse display | 0.00041457 | 0.00068959 | 0.00046498 | 0.00041457 | 0.00041864 |
| Brotli | Reassigned | 0.00049198 | 0.00068959 | 0.00046498 | 0.00049911 | 0.00046652 |
| lrzip | Assigned | 0.00092816 | 0.00139187 | 0.00102427 | 0.00076327 | 0.00119163 |
| lrzip | Reverse display | 0.00178361 | 0.00139187 | 0.00102427 | 0.00180787 | 0.00119163 |
| lrzip | Reassigned | 0.00102295 | 0.00139187 | 0.00102427 | 0.00076327 | 0.00084174 |
| MySQL | Assigned | 0.02808258 | 0.04465970 | 0.03526081 | 0.02943298 | 0.04925601 |
| MySQL | Reverse display | 0.03998320 | 0.04465970 | 0.03526081 | 0.03998320 | 0.04925601 |
| MySQL | Reassigned | 0.02866446 | 0.04465970 | 0.03526081 | 0.02943298 | 0.04327274 |

![Actual family means](../results/v22_larger/verified_comparison.png)

Panels use different vertical scales; numerical comparisons across families should use the table. The [CSV](../results/v22_larger/verified_family_means.csv) and SVG preserve the plotted values.

## Reliability and presentation sensitivity

All **15/15 exact repeats matched** their original raw outputs. Reversing display changed the selected configuration set in **12/15** cases; reassigning IDs also changed it in **12/15**. The model exactly matched the first-displayed-ten set on 25/45 unique prompts and the lowest-ID set on 0/45. Thus deterministic repeated answers coexist with sensitivity to arbitrary presentation. Matching a simple rule on some inputs does not identify an internal algorithm. See [all paired overlaps](../results/v22_larger/presentation_overlaps.csv).

The logs retain an installed-Transformers sliding-window/SDPA warning. The model config has `use_sliding_window:false` and a window of 32,768; the warning check keys on the nonzero window field. The longest observed input plus output was 1,792 tokens, below that window. No setting was changed during collection. Sample-only temperature/top-p/top-k warnings also occurred under greedy decoding. These were not failed requests; equivalence with another attention implementation was not tested.

## Actual costs and deployment distinction

Actual collection: **60 requests, 95,720 input tokens, 1,200 output tokens**, zero missing usage; **431.6949 seconds** summed request wall time (mean 7.1949 seconds, range 5.2130–18.4143). Startup was 8.5656 seconds, including 4.4935 seconds model loading. Control acquisition, model verification/startup, collection, analysis and independent audit/plotting added **458.2772 experiment seconds** after the recorded pre-run ledger. Model download separately took **74.1449 seconds** and transferred 3,098,971,928 bytes. External service spending was **USD 0**; electricity and monetary value of local hardware time were not measured.

New objective accesses: 900 control + 600 LLM = **1,500**. Prefix and classical outcomes were explicitly reused historical evidence. A hypothetical one-presentation deployment over 15 cases would use 300 logical objective evaluations and 15 always-escalate requests, not the 60-call research collection. This is a workload scenario, not a measured deployment, runtime guarantee, dollar-saving estimate or cost-benefit threshold.

Follow-up requests now **200/200**, 300 including the initial stage. Cumulative experiment runtime **2,248.9888/3,600 seconds**; no model attempts remain. Recorded outcome accesses total 6,908; physical compression trials remain 1,134 and are a separate cost type. Cumulative download accounting: 4,514,296,954 total bytes and 4,098,574,535 model bytes, within the original 5 GiB/4 GiB caps. No workers remain active.

## Validation, limits and next action

**156 synthetic tests passed in 1.09 seconds.** Independent post-collection verification reconstructed all 60 prompt/cache/token/grammar mappings, replayed all 150 arms against source labels and shared prefixes, checked 1,500 journal acquisitions and 150 scalar losses, and verified family aggregation and repeats. Read-only replay also passed. All 20 scientific freezes / 1,306 references remain intact. The figure was visually inspected. Evidence and command logs are in [artifacts/study_v22](../artifacts/study_v22/).

The audit/figure script is explicitly post-collection and does not alter frozen selection or analysis code. The earlier PDF and ZIP remain V21 review snapshots and do not include V22. Fresh-machine reproduction, peak memory, other model/device/prompt combinations, untouched-system quality, uncertainty estimates across sufficient independent systems, and a useful learned router remain untested. Three exposed families are insufficient for broad inference; repeated seeds/presentations do not create new systems. Historical 0.5B runs used different conditions, so this does not isolate a causal model-size effect. No formal non-inferiority or practical benefit claim follows from the small positive mean.

**Single next action:** review this complete comparison with Tim and decide whether the small advantage over cheap selection controls justifies a prospectively specified, application-grounded held-out study. Prioritize a practical improvement/cost threshold and independent task admission before another router experiment. Nothing has been sent, published or pushed, and no additional campaign is queued.

Read-only verification in the retained project environment:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
```

The frozen collection and analysis commands ran successfully and are recorded in the protocol. They refuse completed outputs; do not delete guards or reset ledgers to force a rerun.
