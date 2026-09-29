# V73: cross-system audit identifies a fresh Kanzi candidate

The executed metadata audit admitted no recorded performance table and opened no
candidate objective member. It identified Kanzi for a fresh correctness-checked
benchmark. This is a source/admission result, not a new optimization measurement.

## Primary artifact and bounded access

Mühlbauer, Sattler, Kaltenecker, Dorn, Apel and Siegmund's *Analyzing the Impact
of Workloads on Modeling the Performance of Configurable Software Systems*
(ICSE2023) provides configuration samples and measurement scripts. Initial
record1.1 resolves to owner version1.2, DOI10.5281/zenodo.7658046. The paper
describes nine systems, runtime except H2 throughput, and five repetitions except
H2. Workloads are not independent software families.
[Owner record](https://zenodo.org/records/7658046).

Version1.1 lacks the advertised non-coverage ZIP; version1.2 provides it at
401,331,220 bytes. Its directory alone is46,552,624 bytes, exceeding the unchanged
10MiB audit cap. The full-directory request was rejected before its body was
downloaded. Exact HTTP ranges inspected13,935 of327,963 directory entries, then
retrieved only selected configuration/source members. This inventory is PARTIAL.
Member CRCs and SHA256 hashes were verified; the full archive MD5 was not checked.
No extracted code ran. Persisted response bodies total2,913,745 bytes, leaving
565,525,018 bytes under the cumulative5GiB limit. No new inference or benchmarks.

## Kanzi reconciliation

The released sample has4,112 distinct feature vectors. The original sample has
4,180 distinct vectors but only3,344 unique index values: an ID-only join is
invalid. Explicit feature-only transformation of its one-hot thread/block-size
encoding reproduces every released vector and identifies exactly68 original
vectors absent from the release. No objective value was used in this join.
[Owner README](https://zenodo.org/records/7658046/files/README.md).

Do not label those68 vectors confirmed crashes: individual omission reasons were
not retrieved. The README describes unsuccessful configurations being excluded
in general. Complete per-attempt failure denominators remain unresolved.

The XML feature model names thread choices1,32,64; both samples use1,4,8. This
is an inconsistency, not permission to silently map32 to4 or64 to8. Of the
released vectors,1,660 enable checksums, above the nominal400-setting criterion.
Legal/effective application of these vectors is still unverified.

Two sampled shell scripts invoke compression through `exec_bash.py` and GNU time,
then compute compressed/original byte ratio. The inspected bodies contain no
decompression equality check or explicit shell exit-status gate. The wrapper was
NOT inspected, so this does not establish that every upstream validation path is
absent. The scripts were read as data, never executed. Recorded timings remain
unadmitted for this study's correctness/reliability claims.

## Other feature-only screens

| Candidate | Unique vectors | Largest illustrative fixed-contract partition | Disposition |
|---|---:|---:|---|
| Kanzi | 4112 | 2452 by checksum;1660 with checksum enabled | Prioritize fresh validation |
| H2 | 1954 | 369 fixing MVSTORE, IGNORE_CATALOGS, DROP_RESTRICT | Below400 for this conservative partition |
| Batik | 1919 | 1 fixing output/rendering/security options | No tuning domain under that contract |
| Z3 | 1010 | 4 fixing output/validation/instrumentation options | Below400; paper nominal count1011 differs |

These are exploratory conservative partitions, not certified utility equivalence
or evidence that those systems inherently lack useful tuning options. Fixing all
observed options naturally removes tunability. Broader contracts need semantic
justification before use. No family is certified as untouched held-out data;
Kanzi still needs an explicit historical exposure audit.

## Reuse, evidence and limits

Zenodo metadata says CC BY4.0. The included license heading says CC BY-SA4.0,
while linking to CC BY4.0 and describing attribution alone. Preserve this
discrepancy rather than asserting resolved redistribution terms. Application
licenses are separate; a fresh Kanzi runtime must be pinned from its program owner.
These limitations do not invalidate the original performance-modeling paper.
Our failure-aware equal-utility optimization study imposes additional requirements.

Raw sources: `artifacts/sources/v73/`. Executed audit:
`results/v73_admission/summary.json`. Logs: `artifacts/study_v73/`.
All529 tests passed in3.84 seconds; five new synthetic tests cover feature-only
reconciliation and rejection of target columns/invalid encodings. These are not
research measurements. Full archive inspection and candidate timings remain
unexecuted. `scripts/audit_admission_v73.py` recomputes the audit in a fresh copy.

## Single next action

Pin Kanzi's owner source/runtime and build a fresh byte-exact compress/decompress
validator with resource bounds, checksum enabled and canonical transform order.
Freeze one reproducible workload and a bounded reference/contrast/reference
feasibility stage before timing. Preserve failures rather than dropping vectors.
This would be a development adaptation, not reproduction of the archived setup
or an independent-family routing result. No new LLM allowance is requested here.
