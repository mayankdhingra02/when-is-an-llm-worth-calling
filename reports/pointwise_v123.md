# V123: pointwise numeric surrogate development screen

A materially different interface asks Qwen3-8B Q4_K_M for one scalar prediction per configuration, without candidate IDs or a list to choose from. Twenty predictions select ten configurations from the same saved shortlist. Three previously exposed families, seed11 each, were chosen alphabetically before inference. This is development screening, not held-out validation or a full LLAMBO replication. No controller was refitted.

| Control | Mean relative gain | Wins/ties/losses |
|---|---:|---:|---:|
| batch_3nn | 0.038% | 1/0/2 |
| full_sequential_3nn | -16.352% | 0/1/2 |
| random_full | -0.685% | 0/1/2 |
| presentation_first10 | -0.251% | 0/2/1 |
| single_portfolio | -0.096% | 1/0/2 |

Normal valid branches: 3/3. Joint≥5% wins versus batch3NN, sequential3NN and first-ten: 0/3. Loss responsiveness: 3/3 families meet≥3 of10 changed predictions by≥0.02 (requires2). Observation-order stability: 9/9 paired probes differ by≤0.05 (requires7). Frozen combined screening criterion: NOT MET.

| Family | Distinct predictions | Selected IDs (provenance only) | Batch gain | Sequential gain | First-ten gain | Portfolio gain |
|---|---:|---|---:|---:|---:|---:|
| berkeleydb | 1 | 0123456789 | -0.113% | 0.000% | 0.000% | -0.113% |
| dune_hsmgp | 2 | 01245789AC | -1.177% | -47.344% | -0.754% | -1.177% |
| hipacc | 1 | 0123456789 | 1.405% | -1.712% | 0.000% | 1.003% |

Actual collection: 99 charged real local requests, 495 observed generated tokens, 0 missing generated-token receipts, 1584 allocated tokens, 30 new recorded acquisitions; 553.493s lifecycle and 7,383,220,224bytes peak sampled serverRSS. No retries, downloads or external spending. Each logical arm isB20 from the identical acquired prefix10; old prefixes and15 comparator branches were reused, with their historical collection costs retained. Diagnostic interventions add39requests; deployment would need20normal requests per escalation plus setup, not99.

All99 intended requests and all three intended branches remain in the denominator. Missing/invalid scores require batch3NN fallback; no partial-score cherry-picking. Raw outputs, rendered templates, tokenization, generation settings, timestamps, model revision/blob hash, precollection and pre-acquisition seals remain saved. Fixed ID-order tie breaking is an explicit free rule, not evidence of model reasoning. Scores are clipped to[0,1] and quantized to0.01; this may discard useful ranking information. The order probes cover only3candidates per family. Loss removal is a responsiveness diagnostic, not a demand that every individual prediction must change. Both conditions share greedy sampling, with no cross-hardware determinism claim.

Interpretation is conditional on these recorded datasets, fixed shortlist, prefix, model and adapter. Three exposed families and one seed each cannot support a generalizable router or a Q2-readiness claim. Original source correctness/noise and redistribution limitations remain unchanged. Do not tune this prompt on the measured outcomes and relabel it confirmatory. Prior broad model/decoder experiments, including V92/V93 and V103, remain relevant negative evidence.

Evidence: reports/protocol_v123.md and its freeze; artifacts/study_v123/jobs.json; results/v123_pointwise/responses.jsonl and generation_starts.jsonl; results/v123_analysis/diagnostics.json, selection_seal.json, acquisitions.jsonl, arms and comparison.json. Safe replay: scripts/verify_pointwise_v123.py, then scripts/analyze_pointwise_v123.py --report.
