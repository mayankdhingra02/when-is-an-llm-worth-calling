# V13: metadata-only prospective task admission

Audit the fixed 81-table V5 registry for a proposed file-compression task: minimize runtime while meeting an output-size constraint and preserving exact decompressed contents. This is a design/admission audit, not a new optimizer experiment. No objective CSV is opened; no new outcomes, model calls, controller fits, threshold search or held-out scoring occur. Existing scientific conclusions remain unchanged.

Use the V3 and V6 manifests to conservatively retain all previously used families as exposed. Group codecs/variants/seeds using the frozen registry's family mapping. Inspect only schema metadata and pinned owner READMEs. The exact `size` column is a source lead, not proof of equal quality or correctness. For VP8/VP9, lossless input does not establish lossless encoded output. Missing correctness/repetition data remain unknown; published average variability is not a case-level paired error estimate.

Emit all 81 records and explicit failed checks, including rows with unknown families or excluded task kinds; never silently drop the denominator. Report size-bearing table/family counts independently of stricter readiness. No family becomes admitted merely because the script passes. Unknown application utility blocks prospective readiness. Runtime/size semantics are documented for four owner tables; other rows remain unverified for this task rather than declared universally unusable.

Add a reusable prospective split guard that rejects cross-family leakage, previous exposure disguised by new variants/seeds, unknown admission and empty studies. This guard is preparation for a new collector; it does not alter already frozen collectors and does not authorize inference.

Freeze audit code, synthetic tests, source metadata, reviewed READMEs, task contract and this protocol before executing the registry audit. Save derived JSON/CSV and verification logs under separate V13 paths. This forensic metadata inspection and tests do not consume objective or inference budgets or benchmark-runtime allowance. The live resource ledger must remain byte-identical. Do not inspect new candidate performance values to decide admissions.
