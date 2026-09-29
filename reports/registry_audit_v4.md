# Outcome-blind registry audit v4

Inspected **47 pinned MOOT tables** under optimize/config and optimize/systems. All payloads matched their pinned Git blob IDs; SHA-256 values and source URLs are in data/registry_v4.json. Objective payloads were not parsed, ranked or summarized. New systems remain untouched by optimization. Schema audit is transductive feature access, not label collection.

The inventory names 14 candidate system groups, including the three previously exposed groups. Under the frozen binary/single-objective/size criteria, only **four untouched schema-compatible groups** remain: BDB-C, HSQLDB, LLVM and DeepArch. They contain respectively 2,560, 864, 1,024 and 4,096 unique configurations. Original-row objective orientation/provenance checks remain admission requirements. The 20-group split gate correctly produced no assignments.

## Source and identity evidence

The [pinned MOOT systems README](https://github.com/timm/moot/blob/90803be51b00f881305db45aa0cf6a3b5340804f/optimize/systems/README.md) names its PromiseTune lineage. The [owner's PromiseTune catalogue](https://github.com/ideas-labo/PromiseTune/blob/f614bc482e8cdd7b266ffefbf9989748f8a06e7e/README.md) identifies the named tools, including BDB-C, HSQLDB, LLVM and DeepArch. Its commit is f614bc482e8cdd7b266ffefbf9989748f8a06e7e. Only metadata/catalogue inspection occurred; no PromiseTune optimizer or installation instructions were executed. Its reported software versions/workloads are upstream claims, not independently validated provenance for every MOOT row. Suspicious-looking version strings were not silently corrected or adopted as facts. The [original paper](https://arxiv.org/html/2507.05995v1) is by Pengzhou Chen and Tao Chen; no performance result from it is treated as our measurement.

The [MOOT configuration README](https://github.com/timm/moot/blob/90803be51b00f881305db45aa0cf6a3b5340804f/optimize/config/README.md) does not map SS letters to independent software identities. We quarantine SS variants, HSMGP and rs/sol/wc rather than inflate counts. Named software is grouped by product, not vendor: Apache HTTP Server and Apache Storm are different systems; both x264 tables belong to x264 and are excluded from new-system evaluation. Exact workload/hardware lineage remains unresolved in the registry. MOOT has an MIT repository license; that alone does not verify every original collection's provenance.

## Overlap warnings from feature-only fingerprints

Identical feature-value matrices occur among SS-D/F/G and three wc-composition tables; SS-J/S and both rs objective variants; SS-K and wc; SS-L/P; and SS-N and systems/x264. Fingerprints ignore objective payloads and feature names, so equality is a conservative warning, not proof of software identity. These warnings justify provenance review before a group split. No target correlation or outcome similarity was used to discover them.

## All candidate dispositions

No column was silently dropped because its name ends in X. Numeric feature values were normalized for deduplication; objective headers supply only names/directions. Duplicate configurations keep the first source row during eventual collection, independent of outcomes. Table counts differ from some source prose; the manifest records effective feature-vector counts rather than copying catalogue numbers.

| Table | Candidate group | Features | Unique rows | Objectives | Disposition |
|---|---|---:|---:|---:|---|
| Apache_AllMeasurements | apache | 9 | 192 | 1 | previously_exposed_system |
| HSMGP_num | unresolved | 14 | 3,456 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| SQL_AllMeasurements | sqlite | 39 | 4,652 | 1 | previously_exposed_system |
| SS-A | unresolved | 3 | 1,343 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-B | unresolved | 3 | 206 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-C | unresolved | 3 | 1,512 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-D | unresolved | 3 | 196 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-E | unresolved | 3 | 756 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-F | unresolved | 3 | 196 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-G | unresolved | 3 | 196 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-H | unresolved | 4 | 259 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-I | unresolved | 5 | 1,080 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-J | unresolved | 6 | 3,840 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-K | unresolved | 6 | 2,880 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-L | unresolved | 11 | 768 | 2 | unresolved_system_identity; requires_single_objective |
| SS-M | unresolved | 17 | 864 | 3 | unresolved_system_identity; requires_single_objective |
| SS-N | unresolved | 17 | 52,250 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective; row_count_outside_20_5000 |
| SS-O | unresolved | 11 | 972 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-P | unresolved | 11 | 768 | 2 | unresolved_system_identity; requires_single_objective |
| SS-Q | unresolved | 13 | 2,736 | 3 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-R | unresolved | 14 | 3,008 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-S | unresolved | 6 | 3,840 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective |
| SS-T | unresolved | 12 | 5,184 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective; row_count_outside_20_5000 |
| SS-U | unresolved | 21 | 4,608 | 2 | unresolved_system_identity; requires_single_objective |
| SS-V | unresolved | 16 | 6,840 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective; row_count_outside_20_5000 |
| SS-W | unresolved | 16 | 65,536 | 2 | unresolved_system_identity; requires_single_objective; row_count_outside_20_5000 |
| SS-X | unresolved | 11 | 86,058 | 2 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment; requires_single_objective; row_count_outside_20_5000 |
| X264_AllMeasurements | x264 | 16 | 1,152 | 1 | previously_exposed_system |
| rs-6d-c3_obj1 | unresolved | 6 | 3,840 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| rs-6d-c3_obj2 | unresolved | 6 | 3,840 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| sol-6d-c2-obj1 | unresolved | 6 | 2,866 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| wc+rs-3d-c4-obj1 | unresolved | 3 | 196 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| wc+sol-3d-c4-obj1 | unresolved | 3 | 196 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| wc+wc-3d-c4-obj1 | unresolved | 3 | 196 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| wc-6d-c1-obj1 | unresolved | 6 | 2,880 | 1 | unresolved_system_identity; nonbinary_schema_unsupported_by_frozen_treatment |
| 7z | 7zip | 14 | 68,640 | 1 | nonbinary_schema_unsupported_by_frozen_treatment; row_count_outside_20_5000 |
| BDBC | berkeleydb_c | 16 | 2,560 | 1 | schema eligible |
| HSQLDB | hsqldb | 18 | 864 | 1 | schema eligible |
| LLVM | llvm | 10 | 1,024 | 1 | schema eligible |
| PostgreSQL | postgresql | 9 | 864 | 1 | nonbinary_schema_unsupported_by_frozen_treatment |
| dconvert | dconvert | 18 | 1,910 | 1 | nonbinary_schema_unsupported_by_frozen_treatment |
| deeparch | deeparch | 12 | 4,096 | 1 | schema eligible |
| exastencils | exastencils | 12 | 86,058 | 1 | nonbinary_schema_unsupported_by_frozen_treatment; row_count_outside_20_5000 |
| javagc | javagc | 35 | 164,449 | 1 | nonbinary_schema_unsupported_by_frozen_treatment; row_count_outside_20_5000 |
| redis | redis | 9 | 3,155 | 1 | nonbinary_schema_unsupported_by_frozen_treatment |
| storm | storm | 12 | 1,557 | 1 | nonbinary_schema_unsupported_by_frozen_treatment |
| x264 | x264 | 17 | 52,250 | 1 | previously_exposed_system; nonbinary_schema_unsupported_by_frozen_treatment; row_count_outside_20_5000 |

## Admission result

The full design requires 20 untouched admitted groups, 203 new model calls and 6,000 new label acquisitions. The existing inference allowance has 34 calls left, well below 203. The proposed 60-minute additional-stage budget is unapproved and is not installed as a replacement cap. Data identity/schema breadth and resource authorization are separate blockers. The full larger collector is also not yet implemented; the current executable performs only admission checks and the exposed-system projection diagnostic.

Next, resolve original-system lineage and broaden the candidate sources or, with a new versioned treatment, support finite numeric/categorical schemas. Do this before freezing final test assignments. Acquiring more seeds from the four eligible systems cannot repair the independent-group shortfall. No fresh-model experiments were run on those systems.
