# Projection-control diagnostic and larger-study status v4

**The model-free control ran; the larger study is frozen but cannot yet be admitted.** All 15 projection continuations completed from the same corrected v3 ten-label prefixes, acquiring exactly ten new labels per branch. This is exploratory evidence on three previously seen systems. It is not a new held-out evaluation.

## What was frozen and implemented

[protocol_v4.md](protocol_v4.md) specifies 20 independent untouched systems, twelve development/eight test groups, five seeds, B=20/t=10, fixed controllers and group-level comparisons. Its freeze manifest binds 46 code/input files before diagnostic collection. An outcome-blind, hash-checked registry audits 47 MOOT tables and rejects unresolved aliases, incompatible schemas and all previously exposed system variants. Only four named untouched systems fit the current treatment, so no larger-study split or optimizer collection occurred. See [registry_audit_v4.md](registry_audit_v4.md) and artifacts/registry_v4/preflight.json.

The new `uniform_domains_projection_v1` control samples each legal feature coordinate uniformly and uses the identical feature-space projection rule and tie order as v3. It is explicitly model-free, with isolated deterministic RNG, separate measured namespace and no access to hidden objectives. Its first proposals are fixed by dataset hash and seed; acquired labels do not influence later proposals. Tests swap objective values while preserving features and confirm identical proposal/selection traces.

## Actual diagnostic results

Five seeds per system; lower loss is better. LLM and earlier classical/random values are reused measured v3 evidence, with their historical costs retained. The last column is projection loss minus LLM loss, so positive values favor the LLM.

| System | Random | Centroid | Real LLM | Uniform projection | LLM gain over projection |
|---|---:|---:|---:|---:|---:|
| Apache | 0.01333 | 0.00000 | 0.03000 | 0.01667 | -0.01333 |
| SQL | 0.17420 | 0.18451 | 0.16484 | 0.19672 | +0.03189 |
| X264 | 0.03054 | 0.06175 | 0.05881 | 0.02201 | -0.03679 |

The uniform projection control has lower mean loss on Apache and x264; the LLM has lower mean loss on SQLite. The LLM is materially better than this control in 2/15 pairs and materially worse in 4/15, at the predeclared 0.02 margin. The mean x264 advantage for projection is dominated by seed 37; inspect all points rather than treating that average as stable. Neither equality nor overall superiority is established with three systems. This control tests the combined value of informed model proposals versus uniform proposals under the same projection, not every possible non-LLM optimizer.

![Paired diagnostic](../results/v4_projection_diagnostic/analysis/llm_vs_projection.png)

The finding strengthens the need for a projection control in any larger study. The prior benefit-router result is unchanged and was not refitted after inspecting this diagnostic. No additional prompt/model search was performed.

## Costs, verification and limitations

- **150 new objective-label accesses, zero new LLM calls, zero new tokens, USD 0 external experiment spending.** Logical budget remains 20 per control arm, including its reused prefix. This is real recorded-table acquisition, not a live system benchmark.
- Measured projection-branch time: 0.5651 seconds across 15 runs. Reused prefix acquisition and prior paired collection are not free; the marginal control timing excludes those and separates verification/report overhead.
- 110/150 uniform proposals required nonzero-distance projection, with 3 duplicates of acquired configurations and 4 collisions. Corresponding v3 LLM counts were 141, 61 and 110. Both methods acquire a fresh row after projection, and the LLM's duplicate requests still cost inference.
- All-history collection now totals **1658 charged label accesses**. Follow-up requests remain **66/100** (166 historical attempts including v1). Cumulative experiment/analysis runtime is **1157.30/1,800 seconds**; no resource ceiling was increased.
- **30 tests passed** before collection. Independent verification checks frozen inputs, RNG draws, Hamming-distance selection/ties, prefix equality, recorded objectives, metrics and budgets. Raw events/checkpoints, tables and PNG/PDF are in results/v4_projection_diagnostic. No synthetic fixture is included in these quality values.

The larger design needs 203 calls versus only 34 remaining, and its four schema-compatible untouched candidate groups fall short of the required 20. No meaningful larger held-out evaluation has run; objective provenance, wider schemas, group breadth and the full larger collector remain untested/incomplete. The proposed resource increase is merely recorded for review, not authorized or consumed.

## Reproduce

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/build_registry_v4.py
.venv/bin/python scripts/preflight_v4.py  # expected exit 2: admission blocked
.venv/bin/python scripts/verify_projection_v4.py
.venv/bin/python scripts/analyze_projection_v4.py
.venv/bin/python scripts/report_v4.py
```

Pinned table retrieval uses scripts/fetch_registry_sources.py under the original download guard; tables remain Git ignored. Analysis makes no inference calls or new label acquisitions but adds runtime to the ledger. The collection command is `PYTHONPATH=src .venv/bin/python -m escalation.projection_diagnostic`; it refuses to overwrite existing evidence. Do not delete outputs or reset ledgers to repeat it.

**Next action:** extend the outcome-blind registry with verified original-system lineage and compatible data, or freeze a versioned broader feature treatment, before allocating a larger inference run. The present blockers are now concrete rather than an assumption that 20 table names mean 20 independent systems.
