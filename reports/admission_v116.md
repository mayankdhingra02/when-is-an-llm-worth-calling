# V116: reserved-family recovery — original Storm source located, no new group admitted

This executed audit checked six candidate tables using features only and scanned 27,460 saved result/manifest files (327,895,803 bytes) for family aliases. It acquired no objective values and made no model requests. It does not establish that the candidate systems lack optimization opportunity.

## Source recovery changes the next step

The original [BO4CO paper](https://arxiv.org/pdf/1606.06543) by Pooyan Jamshidi and Giuliano Casale identifies the [DICE owner repository](https://github.com/dice-project/DICE-Configuration-BO4CO). We pinned commit `c94d9ad23e1cc4e9009a70cee23cbb42f122b5be`, retrieved its complete 876-entry inventory, and verified 11 source/document blobs against Git object hashes. No upstream code was executed or installed.

The owner's [dataset record](https://zenodo.org/records/56238), DOI10.5281/zenodo.56238, identifies ten tables for three Storm applications, with configuration columns and final throughput/latency columns. Its description says ten-minute measurements; the paper's initial methodology says eight minutes including burn-in. This discrepancy is retained. The archive is a specific next lead, not a newly downloaded/admitted dataset. WordCount variants remain one Storm family; different clusters do not create independent software systems.

The pinned [measurement updater](https://github.com/dice-project/DICE-Configuration-BO4CO/blob/c94d9ad23e1cc4e9009a70cee23cbb42f122b5be/src/integrated/update_expdata.m) reads topology `transferred` counts into a column labeled messages. The [summarizer](https://github.com/dice-project/DICE-Configuration-BO4CO/blob/c94d9ad23e1cc4e9009a70cee23cbb42f122b5be/src/integrated/summarize_expdata.m) averages that column as throughput without an explicit elapsed-time division. It trims an initial polling-row interval, averages latency, and, when that mean is zero, substitutes summed bolt process latency. Thus its outputs need not always represent a uniform measured end-to-end latency or requests/second contract. This is source-level evidence, not proof that any particular archived table contains substituted metrics or incorrect values.

The [Storm response wrapper](https://github.com/dice-project/DICE-Configuration-BO4CO/blob/c94d9ad23e1cc4e9009a70cee23cbb42f122b5be/src/integrated/storm/f_storm.m) returns -1 for unsuccessful deployment or missing summaries. We have not linked those sentinel cases, per-message validation, or a complete attempt denominator to the MOOT tables. The code revision is pinned but not proven to be the revision that generated the2016 archive. A newer source harness cannot certify an older table retrospectively.

The source license calls itself FreeBSD but its actual text contains three conditions, including non-endorsement; preserve the complete file instead of silently calling it a two-clause license. Dataset redistribution terms are not inferred from the code license. [License](https://github.com/dice-project/DICE-Configuration-BO4CO/blob/c94d9ad23e1cc4e9009a70cee23cbb42f122b5be/LICENSE.txt).

## Feature-only eligibility results

These are illustrative necessary coverage checks. They do not certify legal settings, common utility, task correctness or source-to-target linkage. Raw target cells were not converted, ranked or exported.

| Table / family | Distinct vectors | Fixed fields for partition | Largest partition |
|---|---:|---|---:|
| SS-V / MongoDB | 6,840 | journal, nojournal, SSL, wire checks, journal commit interval | 270 |
| named Storm | 1,557 | message size, acker count, topology level | 256 |
| SS-J / RollingSort (Storm) | 3,840 | message size, chunk size, emit frequency | 64 |
| SS-K / WordCount (Storm) | 2,880 | None for this preliminary coverage count | 2,880 |
| SS-I / WordCount (Storm) | 1,080 | None for this preliminary coverage count | 1,080 |
| Redis | 3,155 | None for this preliminary coverage count | 3,155 |

All six pass the40-setting necessary coverage threshold of this audit. This does not supersede the400-setting target used by some later native protocols. MongoDB's exact original workload/release/target mapping and validation remain unresolved. Redis's nine-knob recorded target is still not linked to a measurement generator; the previously pinned CM-CASL tree contains learning code/data rather than the needed measurement recipe. No family passes all the existing V52 admission gates.

## Exposure correction

The scan found1,474 matching files. Every match is in admission/manifest context or the existing V60/V61 Redis work. In particular,1,444 matching files are in `results/v61_redis_physical/` and two in `results/v61_redis_screen/`. Redis is therefore an exposed family; its V52 reservation must not be used as an untouched-test certificate. No non-admission MongoDB/Storm measurement file was found within this scan's declared scope. Absence of such a match is not proof of complete historical non-exposure: unnamed, external, deleted, binary and non-inventoried artifacts remain gaps.

## Execution and bounded costs

- Sources: `artifacts/sources/v116/`; audit: `results/v116_admission/summary.json`.
- Rules and executable/input hashes were frozen before their respective retrieval/audit stages. Scope manifest: `artifacts/study_v116/exposure_scope.json`.
- Fourteen persisted retrieval attempts, thirteen completed, one sandbox DNS failure retained and explicitly retried through the execution-permission mechanism. Total saved source bodies290,909 bytes, below10MiB. Web-tool Zenodo opening returned429; search exposed the owner record, but no archive download occurred.
- Ten new synthetic tests verify poisoned-target isolation, deduplication, nonfinite-feature rejection and selected-source retrieval boundaries. Synthetic fixtures are not research observations. Full suite then passed887 tests; V117 adds two more tests separately.
- Zero new optimizer acquisitions, native workloads, model calls or paid spending. Cumulative saved-download accounting becomes9,876,194,026/10GiB, leaving861,224,214 bytes. Source/agent investigation time is not treated as deployment cost.

Reproduce the frozen audit with `.venv/bin/python scripts/audit_reserved_v116.py --verify-only`. Do not rerun collection into the existing source directory or overwrite prior manifests.

## Concrete next step

For a recorded-only independent-family extension, recover the owner WordCount archive's exact metric/workload and failure/validation linkage before scoring it, using the DOI above. Prefer latency with a documented metric type over assuming the derivative throughput suffix defines the task. If that evidence cannot be recovered, keep this candidate unadmitted; a fresh correctness-checked collection would be a different, prospective experiment. This audit is a useful admission result, not additional evidence of LLM performance or journal readiness.

Follow-up: [V118](archive_v118.md) subsequently retrieved the original archive and its explicit BSD-3-Clause metadata under a separate frozen allowance. It resolves archive location/license/schema, while measurement/validation gates remain closed.
