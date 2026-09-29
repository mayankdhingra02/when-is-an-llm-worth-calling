# Prospective task admission: no untouched runtime/size families in the current registry

The executed metadata audit checked **all 81 registered tables**, without opening objective CSVs or examining new outcomes. Four tables explicitly contain output size: Brotli, lrzip, VP8 and VP9. These represent **three families, all previously exposed**. No untouched runtime/size family is available in this registry for a new held-out evaluation. This is a statement about these pinned inputs, not a claim that no suitable data exists elsewhere.

| Table | Family / exposure | Source-supported properties | Admission consequence |
|---|---|---|---|
| Brotli | brotli; V6 development, V11/V12 analysis/controls | Compression runtime and compressed output size | Can support exploratory development; cannot become fresh held-out evidence |
| lrzip | lrzip; V6 development, V11/V12 analysis/controls | Compression runtime and output size | Same limitation; units and workload discrepancy remain documented |
| VP8 | libvpx; V6 test already inspected | Encoding runtime and output size | Used family; lossless input does not prove lossless or equal-quality encoded output |
| VP9 | libvpx; related to VP8 | Encoding runtime and output size | A different codec/revision does not make a new family; distortion/correctness must be addressed |

Pinned owner README hashes and manual semantic classifications are in `data/admission_evidence_v13.json`; all classifications remain separate from measured outcomes. The full 81-row checklist is `results/v13_1_admission/checklist.csv`. Tables without an explicit size field are unverified for this particular task, not universally unusable for research.

## Concrete task contract and executable safeguards

`configs/task_contract_v13.json` proposes minimizing compression runtime under a size cap with exact decompression equality. It deliberately leaves the application size cap and practical runtime margin unresolved. The old prefix-derived cap is a reproducible research default, not an independently justified service requirement. This draft is not an authorization or a new result.

Before any future collector runs, its admission must establish:

1. Pinned software/data/workload identity, usable feature schema and at least 20 distinct configurations per case.
2. Documented runtime and output-size semantics, a justified cap and practical gain threshold fixed before continuation outcomes.
3. Roundtrip correctness evidence and repeated measurements sufficient to assess noise; aggregate published variability does not substitute for case-level paired observations.
4. Family-based separation, retaining every version/codec/seed of an exposed family in development or exploratory analysis. Headroom selection may use development data only.
5. A frozen comparison with cheap quality-aware methods, explicit charged objective vectors/probes, model-order controls, intended denominators and a bounded resource allowance.

The new `validate_prospective_split` function rejects unadmitted families, empty studies, split-crossing variants/seeds and previously exposed test families. It is tested preparation for future collection, not retroactively inserted into frozen collectors. The metadata script does not claim that passing schema checks validates application utility or authorizes model calls.

## Actual execution and an exposed error

The first V13 pass missed x264 in the historical exposure list because its old manifest uses `heldout_smoke` rather than `test`. Review caught this; V13.1 recognizes the old spelling and rejects unknown historical labels. The corrected audit retains **nine exposed families**. Both the first pass and correction are frozen and preserved. The initial omission did not change the zero-new-size-family conclusion and admitted no collection. Use V13.1 outputs for current decisions.

```sh
.venv/bin/python scripts/audit_admission_v13_1.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

**102 tests passed**, including seven new synthetic admission/regression checks. Current audit verifies 17 frozen metadata/code files, all 81 rows, the four size-bearing tables and nine exposed families. Evidence: `artifacts/study_v13_1/audit.log`, `verification.json` and `tests.log`. No new model request, acquired objective, optimizer experiment or dataset/model download occurred; the resource ledger is byte-identical.

## Bounded external-source reconnaissance

A public owner-documentation search on 24 September 2026 found two possible collection tools, not an admitted offline dataset:

- [lzbench](https://github.com/inikep/lzbench) describes in-memory compressor benchmarking, decompression equality checks, codec-level selections and timed/repeated loops. This could support a new correctness-aware measurement study, but configurations, corpus, family independence, licenses, exact commit and runtime allowance still need auditing. It was not installed or run.
- [Zstandard](https://github.com/facebook/zstd) is an owner source for a configurable lossless compressor. One additional codec would supply at most one new family; levels/workloads cannot be counted as independent software systems. It was not downloaded, pinned or admitted.

These are documentation leads only. Current HEAD pages are not a version manifest; no published benchmark values from the search were imported as experimental evidence. Search queries were `software configuration compression time size dataset 7zip zstd github measurements` and `site.github.com SPLConqueror 7zip measurements size`; owner pages above were opened. This is not an exhaustive search.

## Decision and next action

The existing tables cannot support a fresh held-out runtime/size routing study. **The next substantive action is to obtain and admit a pinned corpus with runtime, output-size, correctness and repetition evidence from genuinely new software families**, using the contract/checklist before looking at gains. A new local measurement campaign is an alternative, but must be concretely scoped against the remaining 128.52 seconds of experiment time and exhausted 128/128 inference allowance. More variants or seeds of the current systems do not resolve the independent-group shortage.

The original negative LLM/router finding and mixed classical result remain unchanged. No external contact, publication or positive-result claim follows from this admission audit.
