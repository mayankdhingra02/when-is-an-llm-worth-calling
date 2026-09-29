"""Generate registry and diagnostic reports from saved audit/measurement records."""
import json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((ROOT/p).read_text())
r=read('data/registry_v4.json');a=read('artifacts/registry_v4/summary.json');lineage=read('artifacts/registry_v4/lineage.json')
s=read('results/v4_projection_diagnostic/analysis/summary.json');c=s['costs'];ledger=read('artifacts/resource_ledger_v2.json')
rows=[]
for d in r['datasets']:
    rows.append(f"| {d['dataset_id']} | {d['system_group'] or 'unresolved'} | {len(d['schema']['feature_names'])} | {d['schema']['unique_configurations']:,} | {len(d['schema']['objective_names'])} | {'; '.join(d['exclusion_reasons']) or 'schema eligible'} |")
text=f'''# Outcome-blind registry audit v4

Inspected **{a['tables']} pinned MOOT tables** under optimize/config and optimize/systems. All payloads matched their pinned Git blob IDs; SHA-256 values and source URLs are in data/registry_v4.json. Objective payloads were not parsed, ranked or summarized. New systems remain untouched by optimization. Schema audit is transductive feature access, not label collection.

The inventory names 14 candidate system groups, including the three previously exposed groups. Under the frozen binary/single-objective/size criteria, only **four untouched schema-compatible groups** remain: BDB-C, HSQLDB, LLVM and DeepArch. They contain respectively 2,560, 864, 1,024 and 4,096 unique configurations. Original-row objective orientation/provenance checks remain admission requirements. The 20-group split gate correctly produced no assignments.

## Source and identity evidence

The [pinned MOOT systems README](https://github.com/timm/moot/blob/{r['moot_commit']}/optimize/systems/README.md) names its PromiseTune lineage. The [owner's PromiseTune catalogue]({lineage['readme_url']}) identifies the named tools, including BDB-C, HSQLDB, LLVM and DeepArch. Its commit is {lineage['commit']}. Only metadata/catalogue inspection occurred; no PromiseTune optimizer or installation instructions were executed. Its reported software versions/workloads are upstream claims, not independently validated provenance for every MOOT row. Suspicious-looking version strings were not silently corrected or adopted as facts. The [original paper](https://arxiv.org/html/2507.05995v1) is by Pengzhou Chen and Tao Chen; no performance result from it is treated as our measurement.

The [MOOT configuration README](https://github.com/timm/moot/blob/{r['moot_commit']}/optimize/config/README.md) does not map SS letters to independent software identities. We quarantine SS variants, HSMGP and rs/sol/wc rather than inflate counts. Named software is grouped by product, not vendor: Apache HTTP Server and Apache Storm are different systems; both x264 tables belong to x264 and are excluded from new-system evaluation. Exact workload/hardware lineage remains unresolved in the registry. MOOT has an MIT repository license; that alone does not verify every original collection's provenance.

## Overlap warnings from feature-only fingerprints

Identical feature-value matrices occur among SS-D/F/G and three wc-composition tables; SS-J/S and both rs objective variants; SS-K and wc; SS-L/P; and SS-N and systems/x264. Fingerprints ignore objective payloads and feature names, so equality is a conservative warning, not proof of software identity. These warnings justify provenance review before a group split. No target correlation or outcome similarity was used to discover them.

## All candidate dispositions

No column was silently dropped because its name ends in X. Numeric feature values were normalized for deduplication; objective headers supply only names/directions. Duplicate configurations keep the first source row during eventual collection, independent of outcomes. Table counts differ from some source prose; the manifest records effective feature-vector counts rather than copying catalogue numbers.

| Table | Candidate group | Features | Unique rows | Objectives | Disposition |
|---|---|---:|---:|---:|---|
{chr(10).join(rows)}

## Admission result

The full design requires 20 untouched admitted groups, 203 new model calls and 6,000 new label acquisitions. The existing inference allowance has 34 calls left, well below 203. The proposed 60-minute additional-stage budget is unapproved and is not installed as a replacement cap. Data identity/schema breadth and resource authorization are separate blockers. The full larger collector is also not yet implemented; the current executable performs only admission checks and the exposed-system projection diagnostic.

Next, resolve original-system lineage and broaden the candidate sources or, with a new versioned treatment, support finite numeric/categorical schemas. Do this before freezing final test assignments. Acquiring more seeds from the four eligible systems cannot repair the independent-group shortfall. No fresh-model experiments were run on those systems.
'''
(ROOT/'reports/registry_audit_v4.md').write_text(text)
methods=[]
for d in s['systems']:
    methods.append(f"| {d['dataset']} | {d['random_mean_loss']:.5f} | {d['classical_loss']:.5f} | {d['llm_loss']:.5f} | {d['projection_loss']:.5f} | {d['llm_gain_over_projection']:+.5f} |")
text=f'''# Projection-control diagnostic and larger-study status v4

**The model-free control ran; the larger study is frozen but cannot yet be admitted.** All 15 projection continuations completed from the same corrected v3 ten-label prefixes, acquiring exactly ten new labels per branch. This is exploratory evidence on three previously seen systems. It is not a new held-out evaluation.

## What was frozen and implemented

[protocol_v4.md](protocol_v4.md) specifies 20 independent untouched systems, twelve development/eight test groups, five seeds, B=20/t=10, fixed controllers and group-level comparisons. Its freeze manifest binds 46 code/input files before diagnostic collection. An outcome-blind, hash-checked registry audits 47 MOOT tables and rejects unresolved aliases, incompatible schemas and all previously exposed system variants. Only four named untouched systems fit the current treatment, so no larger-study split or optimizer collection occurred. See [registry_audit_v4.md](registry_audit_v4.md) and artifacts/registry_v4/preflight.json.

The new `uniform_domains_projection_v1` control samples each legal feature coordinate uniformly and uses the identical feature-space projection rule and tie order as v3. It is explicitly model-free, with isolated deterministic RNG, separate measured namespace and no access to hidden objectives. Its first proposals are fixed by dataset hash and seed; acquired labels do not influence later proposals. Tests swap objective values while preserving features and confirm identical proposal/selection traces.

## Actual diagnostic results

Five seeds per system; lower loss is better. LLM and earlier classical/random values are reused measured v3 evidence, with their historical costs retained. The last column is projection loss minus LLM loss, so positive values favor the LLM.

| System | Random | Centroid | Real LLM | Uniform projection | LLM gain over projection |
|---|---:|---:|---:|---:|---:|
{chr(10).join(methods)}

The uniform projection control has lower mean loss on Apache and x264; the LLM has lower mean loss on SQLite. The LLM is materially better than this control in {s['llm_materially_better_than_projection']}/15 pairs and materially worse in {s['projection_materially_better_than_llm']}/15, at the predeclared 0.02 margin. The mean x264 advantage for projection is dominated by seed 37; inspect all points rather than treating that average as stable. Neither equality nor overall superiority is established with three systems. This control tests the combined value of informed model proposals versus uniform proposals under the same projection, not every possible non-LLM optimizer.

![Paired diagnostic](../results/v4_projection_diagnostic/analysis/llm_vs_projection.png)

The finding strengthens the need for a projection control in any larger study. The prior benefit-router result is unchanged and was not refitted after inspecting this diagnostic. No additional prompt/model search was performed.

## Costs, verification and limitations

- **{c['new_label_accesses']} new objective-label accesses, zero new LLM calls, zero new tokens, USD 0 external experiment spending.** Logical budget remains 20 per control arm, including its reused prefix. This is real recorded-table acquisition, not a live system benchmark.
- Measured projection-branch time: {c['measured_branch_seconds']:.4f} seconds across 15 runs. Reused prefix acquisition and prior paired collection are not free; the marginal control timing excludes those and separates verification/report overhead.
- {c['projected']}/150 uniform proposals required nonzero-distance projection, with {c['duplicates']} duplicates of acquired configurations and {c['collisions']} collisions. Corresponding v3 LLM counts were 141, 61 and 110. Both methods acquire a fresh row after projection, and the LLM's duplicate requests still cost inference.
- All-history collection now totals **{c['all_version_label_accesses']} charged label accesses**. Follow-up requests remain **66/100** (166 historical attempts including v1). Cumulative experiment/analysis runtime is **{ledger['experiment_seconds']:.2f}/1,800 seconds**; no resource ceiling was increased.
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
'''
(ROOT/'reports/pilot_report_v4.md').write_text(text)
print('Generated registry audit and projection diagnostic report')
