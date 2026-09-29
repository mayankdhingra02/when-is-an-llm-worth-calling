# Expanded-grid development result (V17)

**The expanded space still leaves little recorded feasible-runtime headroom after cheap search.** All846 physical trials and30 paired classical arms completed. No model was called. This is a completed exploratory negative result for this benchmark recipe, not a negative verdict on LLM optimization generally.

| Family | Settings | Cheap gain over random, mean | Remaining hindsight headroom, mean | Cases above10% headroom |
|---|---:|---:|---:|---:|
| zstd | 96 | +0.499% | 0.537% | 0/5 |
| lz4 | 96 | +0.592% | 0.197% | 0/5 |
| zlib | 90 | +0.000% | 0.000% | 0/5 |

Each family has five fixed seeds. Maximum individual headroom is1.132%. The equal-family mean cheap gain is0.364%; this small observed difference does **not** establish superiority or practical benefit. The full-table optimum is a non-deployable descriptive bound over measured medians, not an LLM result or a confidence bound on true runtime. No case exceeds the previously fixed10% diagnostic. This diagnostic is not an application-approved success margin.

## What was fixed and executed

[Protocol and stop rule](protocol_v17_expansion.md) and22 source/input files were hash-frozen before measurement. One strict expansion of V15: Zstandard levels1–12, four windows, two checksum modes; LZ4 levels1–12, four blocks, two dependency modes; zlib levels1–9, five memory levels, two strategies.282 configurations ×three fresh shuffled repetitions =846 trials. Original measurements were preserved and not mixed into this session. No retries, warmups or filtered cases. The80-second collection ceiling was respected (actual collection ledger increment43.8062seconds).

The same901120-byte CPythonv3.10.13 archive, pinned commit49965601d6afedafe47cc85556d99b7a24981051, and installed Zstandard1.5.7/LZ4 1.10.0/zlib1.2.12 were used. All compressed outputs decoded exactly and are retained with hashes. See [original workload provenance](../artifacts/study_v15/workload_manifest.json) and [environment hashes](../artifacts/study_v15/environment.json). No packages were installed.

Optimizer inputs contain configuration features and acquired vectors only. The unchanged charged V16 oracle/nominal-Hamming joint3NN method acquires the reference plus three seeded settings, then six cheap steps to checkpoint10. The size cap is the acquired reference size. Each branch has ten further acquisitions, including infeasible settings. Logical budget20/arm; actual shared-prefix collection30 accesses/case,450 total. An independent implementation replayed every choice and verified all15 shared prefixes,30 arms and450 charges. All families/variants/seeds remain development data.

## Timing and interpretation

| Family | Median within-setting CV | Settings above10% CV | Distinct compressed outputs |
|---|---:|---:|---:|
| zstd | 1.87% | 2 | 96/96 |
| lz4 | 2.39% | 4 | 60/96 |
| zlib | 2.81% | 2 | 75/90 |

No setting produced unstable output bytes across its three repetitions. Repeated feature settings can still produce identical compressed outputs; none was deleted. Three repetitions offer limited uncertainty information. The small outcome differences relative to descriptive timing variation warrant caution; neither superiority nor equivalence is established. Selecting a full-table minimum can exploit timing noise.

![All paired cases](../results/v17_classical/comparison.png)

The grid now spends20/96 or20/90 settings per arm instead of20/32, yet the recorded headroom remains small. This weakens the explanation that20/32 coverage alone caused the earlier result. It does not isolate candidate count causally: levels, session, and CLI timing boundary changed together. V17 moves parameter construction outside compression timing; CLI launch/pipes remain included, whereas zlib uses its Python API. A small single archive and these timing stacks limit relevance to production compression. Do not compare raw family runtimes or claim a broader benchmark has been validated.

## Evidence and reproducibility

- Raw physical attempts, complete denominator and medians: [results/v17_measurements](../results/v17_measurements/); actual bytes in artifacts/sources/live_v17/outputs/ (Git ignored).
- Raw saved prefixes, both continuations and all cases: [results/v17_classical](../results/v17_classical/).
- [Choice replay](../artifacts/study_v17/verification.json), [physical verification](../artifacts/study_v17/physical_verification.json), [final checks](../artifacts/study_v17/final_checks.json), [120 passing tests](../artifacts/study_v17/precollection_tests.log), [accounting](../artifacts/study_v17/final_accounting.json).
- [Frozen source map](protocol_v17_expansion.freeze.json); [feature manifest](../data/live_manifest_v17.json); [reproduction instructions](../REPRODUCE.md).

The separate post-collection audit rechecked846 payloads,282 medians,450 charges and all15 historical/current freezes (1038 file references). It did not rerun codecs or create new outcomes. Completed collector reuse was checked and made no new trials. A harmless snapshot filename is retained exactly as emitted: artifacts/study_v17/physical_analysis_ledger_ledger.json. A precollection file-copy generation assertion was corrected before freeze; no measurement had started. No experimental failures were suppressed.

## Costs and disposition

This stage:846 physical-vector attempts +450 recorded-vector accesses, **0 model requests**, **45.4948seconds** charged including analysis/render/audit,0 download bytes,USD0 external spend. Cumulative:1134 physical trials and5408 recorded accesses, kept as different cost types. Follow-up inference128/128 exhausted (228 historical attempts including initial stage). Runtime1743.8069/1800seconds;56.1931seconds remain; ledger inactive.

Dataset construction is actual research cost; an estimated deployed selection would observe20 configuration vectors, not collect the entire846-trial grid or both branches. These offline lookups do not establish live deployment runtime, energy or monetary savings. No modeled LLM deployment costs are added because no LLM ran in V17.

The predeclared single-grid follow-up stops here regardless of sign. The most useful next action is to review the negative pilot with Tim and agree on an application-grounded runtime/size task before authorizing another measurement or model campaign. [Review note](review_note.md) separates defensible findings from untested claims. Stronger-model routing, untouched-family generalization, broad workload coverage and application utility remain untested; leftover runtime alone does not justify another outcome-driven grid expansion.
