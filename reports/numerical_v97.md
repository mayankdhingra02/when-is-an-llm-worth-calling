# V97: restricted-domain paired result

**Exploratory follow-up on one previously studied system.** No new independent test group, no retuned controller and no claim of journal readiness. All original V94–V96 evidence is preserved.

| Comparator | LLM mean relative gain | >=5% benefit cases | >=5% harm cases |
|---|---:|---:|---:|
| batch_3nn | -1.52% | 0/5 | 1/5 |
| full_sequential_3nn | -2.77% | 0/5 | 2/5 |
| random_full | +12.62% | 2/5 | 1/5 |

LLM cases beating BOTH strong controls by at least5%: **0/5**. Positive gain means a faster measured incumbent. All seeds, including failures, are retained. No population interval is appropriate for one software system.

| Seed | Batch 3NN seconds | Sequential 3NN seconds | Random seconds | LLM seconds |
|---|---:|---:|---:|---:|
| 11 | 0.00364646 | 0.00366354 | 0.00363483 | 0.00401425 |
| 23 | 0.00412817 | 0.00376179 | 0.00706212 | 0.00400129 |
| 37 | 0.00359133 | 0.00359133 | 0.00359133 | 0.00356183 |
| 53 | 0.00342450 | 0.00342450 | 0.00342450 | 0.00342450 |
| 71 | 0.00368496 | 0.00378321 | 0.00529029 | 0.00373596 |

## Executed scope

250 freshly charged native acquisitions; 250 valid, 0 failed workers. Physical journal: 750 starts / 750 returns. Independently recomputed 750 numerical certificates from saved solution vectors. Each branch uses its identical saved10-label prefix and10 additional labels. Every selection is replayed from pre-decision/acquired data.

Real Qwen3: 50 requests / 50 returned responses, 50 generated tokens; 34620 summed context tokens and 3507 reported actual prefill tokens. Zero retries. Model/prompt/runtime provenance and raw responses are saved.

Native collection 79.429s; model lifecycle 17.143s. Peak sampled model RSS 6,152,175,616bytes. External spendingUSD0; electricity and hardware cost unknown. No download or installation.

## Frozen policies and costs

| Policy | Calls / cases | Mean gain vs sequential | Missed >=5% cases |
|---|---:|---:|---:|
| never | 0/5 | +0.00% | 0 |
| always | 5/5 | -2.77% | 0 |
| random_matched_zero | 0/5 | +0.00% | 0 |
| uncertainty_frozen | 0/5 | +0.00% | 0 |
| benefit_frozen | 0/5 | +0.00% | 0 |
| hindsight_oracle | 2/5 | +0.41% | 0 |

Benefit/uncertainty thresholds were fixed to never-call by the older development fit; matched-rate random therefore has zero calls too. Their equality is not a learned-router success. The hindsight oracle uses both outcomes and is not deployable.

Actual collection:250 labels (50 shared-prefix+200 continuation), up to750 physical solves, plus every model request/startup. Estimated deployment of one arm per case:100 total labels (5×20), up to300 physical solves; always-call would add50 model requests, never-call adds0. These are accounting scenarios, not a new deployment measurement. The per-case inference-only break-even reuse counts in summary.json exclude model startup, search differences and noise.

## Limits and next action

Median within-acquisition relative timing range: 3.35%. Repeated configurations: 69; median relative range 2.04%. These are descriptive ranges, not uncertainty bounds. Selecting the best noisy median can bias apparent runtime improvements. One input/machine and a changed candidate domain limit comparison with V94; do not attribute differences solely to one parameter or count these five seeds as independent systems. A clean run does not prove reliability.

Next decisive research step remains independent replication and additional systems. The next locally available methodological test is a separately frozen reasoning procedure that reserves tokens for its final answer; run only on development data until its procedure is validated. Do not tune against these outcomes or reopen completed V95 collection.

Raw: `results/v97_native/`, `results/v97_qwen/`. Protocol and hashes: `reports/protocol_v97.md`, `reports/protocol_v97.freeze.json`. Regenerate with `scripts/analyze_numerical_v97.py`, `scripts/cost_noise_numerical_v97.py` and `scripts/report_numerical_v97.py` in the pinned environment. All three are saved-data-only analyses.
