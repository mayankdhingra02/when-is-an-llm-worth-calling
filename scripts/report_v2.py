"""Generate the exploratory v2 discussion report strictly from saved evidence."""
from pathlib import Path
import json,csv
root=Path(__file__).resolve().parents[1];out=root/'results/v2/analysis'
s=json.loads((out/'summary.json').read_text());c=s['costs'];gate=json.loads((root/'results/v2/feasibility/gate.json').read_text());ledger=json.loads((root/'artifacts/resource_ledger_v2.json').read_text())
pairs=list(csv.DictReader((out/'paired_gains.csv').open()));policies=s['policies'];table=[]
for d in ['Apache','SQL','X264']:
 r={v['method']:v for v in s['methods'] if v['dataset']==d}
 l=r['local_llm_constrained_v2'];gain=[float(p['gain']) for p in pairs if p['dataset']==d]
 table.append(f"| {d} | {r['random']['mean_loss']:.5f} | {r['ezr_centroid_adapted']['mean_loss']:.5f} | {l['mean_loss']:.5f} | {sum(gain)/len(gain):+.5f} |")
pt=[]
for p in policies:
 pt.append(f"| {p['policy']} | {p['mean_loss_system_weighted']:.5f} | {p['escalations']}/5 | {p['selected_branch_requests']} | {p['missed_useful_count']}/{p['useful_count']} | {p['harmful_escalations']} |")
gains=[float(p['gain']) for p in pairs];positive=sum(g>.02 for g in gains);negative=sum(g<-.02 for g in gains)
text=f'''# Exploratory follow-up v2: real paired results

**The structured-output repair enabled real local-model continuations.** The three format checks passed, and {c['completed_paired_runs']}/15 paired software runs completed. This removes v1's format blocker; it does not establish that a learned escalation controller generalizes.

The user authorized continuation after v1 stopped at its cap. A new allowance of 100 local attempts was announced and frozen in [protocol_v2.md](protocol_v2.md). The original 30-minute cumulative runtime ceiling and USD 0 external-spending restriction remained. All original v1 evidence, including its failures, is preserved in [pilot_report.md](pilot_report.md).

## What changed

The same official Qwen 0.5B model used a compact prompt and constrained JSON decoding. Punctuation and legal domains are enforced; variable values are selected from the model's logits. Generated token IDs and the complete constraint schedule are logged so this distinction is auditable. Nothing uses unseen objectives to select tokens or project candidates. A known dead worker now stops collection before reserving another request; a timeout stops the stage.

Three real-model format checks used independent synthetic fixtures with 9, 16 and 39 binary variables. These calls count toward costs but their synthetic quality never enters software results. They passed before the first v2 continuation. No prompt or model was changed after seeing v2 outcomes. This is a changed-treatment exploratory adaptation, not a SNAP2 numerical replication.

## Optimization results

All classical continuations and ten-label prefixes were reused unchanged from v1. Each new LLM continuation acquired exactly ten additional labels, giving the same logical B=20 per arm. The only held-out smoke system is x264; its classical scores had already been inspected during v1, so v2 is explicitly exploratory.

| System | Random mean loss | Centroid mean loss | Constrained LLM mean loss | Mean paired gain |
|---|---:|---:|---:|---:|
{chr(10).join(table)}

Loss is best acquired normalized d2h (lower is better); gain is classical loss minus LLM loss. Across 15 pairs, {positive} gains exceeded the predeclared +0.02 material margin, and {negative} were below -0.02. These are descriptive counts, not independent-system statistical evidence.

![Paired gains](../results/v2/analysis/paired_gains.png)

## Fixed controller comparison

Ridge benefit prediction and both ablations used only Apache+SQLite development groups, with group cross-fitted predictions for threshold selection. Uncertainty thresholds also used development groups only. Preprocessing and fitted weights did not access x264 outcomes. Policies were applied once with fixed thresholds. Repeated seeds are not new software groups.

| Policy | x264 mean loss | Escalations | Selected-branch requests | Missed useful / useful | Harmful escalations |
|---|---:|---:|---:|---:|---:|
{chr(10).join(pt)}

The hindsight row chooses after seeing both outcomes and is **non-deployable**. Its selected-branch requests are an accounting reference, not the cost of obtaining oracle knowledge. Random realized-rate matching uses only the count of selected cases, never outcome quality; it is a retrospective diagnostic with one fixed random draw. All fixed-grid points are retained in threshold_curves.csv. No further test-set threshold selection was performed.

Only two development systems and one held-out system are available. Router evidence remains insufficient regardless of the ordering in this five-seed table. No confidence intervals, significance tests, non-inferiority claims or generalization claims are made.

![Fixed threshold curves](../results/v2/analysis/quality_cost_curve.png)

## Reliability and costs

- {c['actual_requests']} additional real local requests: {c['feasibility_requests']} format checks and {c['paired_model_requests']} software-continuation requests; {c['request_errors']} provider errors, {c['malformed_responses']} malformed paired responses, {c['retries']} retries.
- {c['fallback_acquisitions']} fallback acquisitions; {c['projected_proposals']} proposals required nonzero feature projection distance; {c['duplicate_proposals']} were exact duplicates of an acquired configuration; {c['collision_proposals']} were nearer an acquired row than their selected unevaluated row. Projection still charges a fresh label, and duplicate suggestions still have model cost.
- Observed v2 tokens: {c['input_tokens']:,} input and {c['output_tokens']:,} output, including grammar-forced syntax and the three feasibility calls. This is real inference, not hand-produced JSON proposals.
- **{c['v2_new_label_accesses']} new label accesses** in v2. Historical v1 collection remains 700; cumulative collection is {c['all_version_actual_label_accesses']}. Classical/prefix reuse incurs no new acquisition, but historical cost is not erased. The method-comparison artifact's 750 accesses includes the reused 600-label classical reference and the 150 new continuations; it is not the new incremental collection bill.
- v2 request wall time: {c['request_wall_seconds']:.2f} seconds. Cumulative recorded experiment time: {ledger['experiment_seconds']:.2f}/1,800 seconds, of which {ledger['experiment_seconds']-ledger['carried_v1_seconds']:.2f} seconds were charged to v2 including its analysis. Model startup/loading is separately recorded in model_runtime.json.
- Additional experiment spending: **USD 0**. No new dependencies, weights or cloud resources. Electricity and hardware costs remain unknown. v1 timeout tokens remain unknown; v2 observed usage does not retroactively fill that gap.

Policy deployment costs select only the chosen branch plus prefix/feature computation; per-router prediction overhead is separately recorded in router files and is very small, but this is trace replay rather than a separately timed deployed service. Historical training/paired collection and model loading are not advertised as free. The cumulative ledgers and per-request raw logs remain authoritative.

## Evidence and limits

[results/v2](../results/v2/) contains the frozen manifest/source snapshot, real raw requests, generated token IDs, constraints, feasibility fixtures, checkpoints and run records. The verifier checks exact prefix equality, 20-label budgets, table outcomes, prompt reconstruction from acquired observations only, projection replay, token-to-text decoding, legal token schedules and metrics. Original v1 verification remains separate.

The constrained format gate is largely guaranteed by construction; it checks execution and serialization, not model reasoning. The small model, binary single-objective tables, offline objectives and three software groups sharply limit scientific claims. Optimizer normalization/projection and the model differ from the source paper. Dataset pretraining contamination and original workload/hardware versions remain unresolved. See [limitations.md](limitations.md).

## Next action

Review the paired gains and policy table with the source-alignment caveats, then freeze a larger evaluation with more independent software systems. Before spending on scale, assess whether useful LLM gains and harmful cases provide enough routing variation. Do not tune repeatedly on this x264 smoke result. A meaningful generalization study needs untouched system groups, a validated system/variant registry and a new resource plan.
'''
(root/'reports/pilot_report_v2.md').write_text(text)
print('V2 report generated from measured results')
