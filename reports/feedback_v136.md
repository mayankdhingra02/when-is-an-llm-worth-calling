# V136: matched-call sequential feedback diagnostic

This is a prospective diagnostic on two previously exposed recorded software families, LLVM (10 features) and SAC (59), chosen by feature-count extremes among the six original families. Five fixed seeds each. Both arms start from the same B10 prefix, make five real calls proposing two settings each, and finish at B20. Feedback receives its own new measured outcomes; masked receives newly tried settings with outcomes withheld. No router was fitted. Ten paired seeds are only two independent software groups.

Primary comparison: does feedback improve the final incumbent at the same model-call and objective budget? Positive values favor feedback.

| Family | Feedback vs masked | Wins/ties/losses | Feedback vs sequential3NN | Masked vs sequential3NN |
|---|---:|---:|---:|---:|
| llvm | 0.0000% | 0/5/0 | -0.9688% | -0.9688% |
| sac | 0.0000% | 0/5/0 | -0.4036% | -0.4036% |

| Family / seed | Prefix incumbent | Feedback | Masked | Historical sequential | Historical one-shot batch |
|---|---:|---:|---:|---:|---:|
| llvm / 11 | 201.546667 | 201.546667 | 201.546667 | 200.38 | 201.546667 |
| llvm / 23 | 206.9 | 200.38 | 200.38 | 200.38 | 206.226667 |
| llvm / 37 | 199.953333 | 199.953333 | 199.953333 | 199.953333 | 199.953333 |
| llvm / 53 | 219.153333 | 208.92 | 208.92 | 200.38 | 219.153333 |
| llvm / 71 | 201.896667 | 201.896667 | 201.896667 | 201.896667 | 201.896667 |
| sac / 11 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 23 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 37 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 53 | 1.51 | 1.51 | 1.51 | 1.5 | 1.51 |
| sac / 71 | 1.5 | 1.5 | 1.5 | 1.48 | 1.5 |

LLVM minimizes the recorded compiler optimization time; SAC minimizes recorded n-body execution time, in their original source units. Cross-family raw values must not be pooled. Historical classical and one-shot controls reuse verified identical prefixes. Historical one-shot prompts/grammar/output caps differ (LLVM V127; valid SAC repair V135), so comparison with them does not isolate feedback alone. Old failed SAC responses are not replaced.

Additional descriptive contrasts:

| Family / arm | Gain vs prefix | Prefix improvements /5 | Gain vs historical one-shot |
|---|---:|---:|---:|
| llvm / feedback | 1.5642% | 2 | 1.5009% |
| llvm / masked | 1.5642% | 2 | 1.5009% |
| sac / feedback | 0.0000% | 0 | 0.0000% |
| sac / masked | 0.0000% | 0 | 0.0000% |

Reliability: 100/100 valid round responses; 0 fallback rounds, zero retries. Of 200 valid proposals, 172 required nonzero feature-distance projection, 10 repeated the other proposal within their round, and 112 exactly matched an already acquired setting before projection. All selected rows remained unique within their B20 arm. Identical round-zero prompts and sampling seeds yielded identical text in 10/10 cases.

A post-outcome exploratory trace audit (followup_trace.json) finds 36/40 follow-up pairs with different raw outputs and 27/40 with different selected rows. Tied final incumbents therefore do not mean the model ignored the changed prompt or followed identical search paths. Changed text alone does not establish beneficial use of feedback.

Actual collection: 100 real local requests, 7378 observed generated and 140387 observed prefill tokens; missing intended usage receipts 0/0. Allocated output tokens 25600; 200 newly charged recorded acquisitions. Model lifecycle 854.842s, overall collection 854.844s, recorded evaluation 0.090712s; peak sampled server RSS 6,336,479,232bytes. No new native workload, download, retry, paid/cloud call or spending.

Deployment accounting: one escalation requires five requests and ten additional evaluations after B10 (B20 total), with1280 allocated output tokens. Per-arm measured request times are in comparison.json and exclude cold start and historical prefix collection. Actual research collection includes both arms and all100 requests; historical controls retain their original costs. No monetary, energy or actual software runtime saving is inferred from recorded-table access time.

Limits: two exposed groups cannot validate a learned router or establish journal readiness. The intervention supplies numeric feedback in symbolic configuration space; it is not an exact SNAP2/LLAMBO reproduction. Five rounds of two proposals are not fully sequential one-proposal feedback. Hamming projection can dominate model suggestions. These are fixed recorded observations, not fresh native correctness or noise tests. Shared hardware and a single quantized8B model limit transfer claims. No tuning or further batch is triggered by whether this result is favorable.

Provenance: reports/protocol_v136.md and protocol_v136.freeze.json; artifacts/study_v136/jobs.json and candidates; results/v136_feedback decisions, preflight, generation_starts.jsonl, responses.jsonl, selections, acquisitions.jsonl, rounds, arms, runtime/ledger/summary. Every selection precedes its charged labels. Independent standard-library replay reconstructs prompts, masking, sampling, projection, raw source rows and contrasts. Synthetic tests are separate. Prior V135 config had a stale split label; protocol/report were already explicit exposed development; see prior_metadata_erratum.json.

Safe reproduction: `.venv/bin/python scripts/verify_feedback_v136.py` then `.venv/bin/python scripts/analyze_feedback_v136.py`. These commands make no model requests and acquire no new outcomes.
