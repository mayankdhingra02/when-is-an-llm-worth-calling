# Schema erratum — discovered during continuation, 2026-09-24

The original loader used a generic upstream-style suffix convention: ignore any column ending in X. The SQLite CSV contains a real configuration option named `sQLITE_OMIT_AUTOMATIC_INDEX`. Applying that convention silently removed this option.

| SQLite quantity | Original full CSV | Actual v1/v2 parser | Corrected v3 |
|---|---:|---:|---:|
| Feature columns | 39 | 38 | 39 |
| Source data rows | 4,653 | 4,653 | 4,653 |
| Unique configurations after first-row deduplication | 4,652 | 4,132 | 4,652 |
| Excluded rows | 1 true full-vector duplicate | 521 projected-vector duplicates | 1 true full-vector duplicate |

The 520 additional collapses merged configurations that differed on the omitted option. The earlier pilot report and STATUS incorrectly described the raw/full-vector counts as the effective experimental counts. The original raw schema artifacts did contain the reduced counts, but the initial verification did not compare them against the manifest. Budget, prefix, token and deterministic-replay checks passed within the wrong feature representation; they could not validate the intended dataset schema.

This is a project implementation and reporting error. It is not evidence about SQLite optimization quality, nor a claim that MOOT data are invalid. Apache and x264 feature parsing was unaffected, but routers trained on the affected SQLite outcomes are not interpretable as full-schema results.

Upon discovery, v2 collection was interrupted, the worker terminated, and completed/partial/blocked run records preserved. Request 33 was interrupted; its token usage is unknown. v2 consumed 33 attempts and 58 new label acquisitions. No affected results were silently replaced. Original v1/v2 logs and executed code snapshots remain available for audit.

The correction uses explicit feature names and ignored-column lists in data/manifest_v3.json, asserts effective dimensions/unique counts/duplicate counts before collection, and adds a regression test for a real option name ending in INDEX. All classical arms are rerun under the corrected schema with the same original seeds/budgets. v3 is a newly frozen exploratory treatment, not a repaired historical v1 result.

For v3's smaller serialization overhead, the real model generates constrained bit strings, five candidates per call, with all choices retained as raw text and token IDs. This treatment change is documented in protocol_v3.md and is not pooled with the earlier JSON treatment. The existing follow-up request/runtime budget is reused without any increase.
