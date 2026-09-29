"""Generate review report from actual v6 records, never invented values."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,lines

def main():
    s=read('results/v6/summary.json');v=read('artifacts/study_v6/verification.json');seal=read('results/v6/router_seal.json');rows=read('results/v6/outcomes.json');held=[r for r in rows if r['split']=='test']
    ledger=read('artifacts/resource_ledger_v2.json');baseline=read('results/v6/manifest.json')['baseline_ledger'];c=s['collection_cost'];runtime=read('results/v6/model_runtime.json');diversity=read('results/v6/proposal_diversity.json')
    p={r['policy']:r for r in s['held_out_policies']};tests=Path('artifacts/study_v6/tests_final.log').read_text().strip().splitlines()[-1]
    help_count=sum(r['gain']>.02 for r in held);harm_count=sum(r['gain']<-.02 for r in held)
    report=f'''# V6 pilot: six new families, sealed held-out routing

Actual execution completed on 2026-09-24. This is an expanded exploratory smoke test, not the proposed 20-group study and not evidence of generalization. Thirty paired cases across six software families completed, with five fixed seeds per family, checkpoint 10 and logical budget 20 per arm. Prior raw results and the v4/v5 frozen snapshots remain unchanged.

## Measured finding

On the 15 held-out cases from three families, the local LLM materially improved on the classical continuation in **{help_count}/15** cases and materially harmed it in **{harm_count}/15**, using the frozen .02 normalized-loss margin. The benefit controller escalated **{p['benefit']['escalations']}/15** cases. Its system-averaged loss was **{p['benefit']['group_mean_loss']:.6f}**, versus **{p['never']['group_mean_loss']:.6f}** for never-escalate and **{p['always']['group_mean_loss']:.6f}** for always-escalate. These are descriptive outcomes from only three independent test families.

The hindsight oracle loss was **{p['hindsight_oracle_diagnostic']['group_mean_loss']:.6f}**. It selects branches after observing their outcomes and is not deployable. Repeated seeds are not additional independent software systems.

## Admission and treatment

Development: MySQL 5.6.10, lrzip 530, Brotli 0.3.0. Held-out: VP8 v0.9.1, HSQLDB 2.1.0, PostgreSQL 10.0. Seven families had explicit target semantics in the pinned owner case READMEs; six were selected and split by the frozen family-hash rule. OpenVPN was admitted with throughput maximization but excluded by that allocation. MySQL/MariaDB and VP8/VP9 remain single families. Previous Apache/SQLite/x264 families are excluded. Other v5 candidates remain unadmitted; 22 candidates never meant 22 validated tasks.

All six measured tables have binary features, despite the new interface supporting finite domains. The mixed-domain format gate used synthetic objectives, stored separately. One local-model request proposes ten configurations without within-batch feedback. That differs from v3's two batches of five, so differences across versions cannot isolate the effect of software family, device or representation. Every nonconstant proposal coordinate comes from real model logits under a domain/syntax constraint. Projection chooses an unevaluated real candidate using features only.

The model is Qwen/Qwen2.5-0.5B-Instruct, revision 7ae557604adf67be50417f59c2c2f167def9a775. This run used **{runtime['device']} / {runtime['dtype']}**, with greedy generation and no sampling-seed support. The earlier run used MPS; bitwise cross-device equivalence is not asserted.

## Per-family outcomes

Lower normalized loss is better. Each number averages five seeds within one family.

| Family | Split | Random from start | Classical | LLM | Uniform projection | Material help / harm |
|---|---|---:|---:|---:|---:|---:|
'''
    for r in s['systems']:
        report+=f"| {r['system_group']} | {r['split']} | {r['random_loss']:.6f} | {r['classical_loss']:.6f} | {r['llm_loss']:.6f} | {r['projection_loss']:.6f} | {r['material_help']} / {r['material_harm']} |\n"
    report+='''
## Held-out policies

All controller preprocessing and thresholds use development groups only. The Ridge gain predictor uses leave-one-development-family-out predictions for threshold selection and is sealed before the first held-out objective acquisition. Threshold curves are preserved; no operating point is selected from test outcomes.

| Policy | Group-mean loss | Escalations / 15 | Missed material benefits | Harmful escalations |
|---|---:|---:|---:|---:|
'''
    for r in s['held_out_policies']:
        report+=f"| {r['policy']} | {r['group_mean_loss']:.6f} | {r['escalations']} | {r['missed_material_benefits']} | {r['harmful_escalations']} |\n"
    report+=f'''
`random_development_rate` is a deployable Bernoulli baseline using the development-selected benefit rate. `random_matched_realized_rate_diagnostic` samples the test set at the realized benefit count, without using outcomes, and is only a retrospective rate-matching diagnostic. The oracle is also diagnostic. No significance test or formal risk guarantee is claimed.

![Measured quality and escalation](../results/v6/quality_cost_review.png)

![All paired gains](../results/v6/paired_gains.png)

## Costs and reliability

Actual new collection: **{c['actual_objective_acquisitions']} objective acquisitions**, **{c['actual_request_attempts']} real local-model attempts** ({c['synthetic_format_attempts']} synthetic format checks + {c['measured_pair_attempts']} measured pairs). Per paired case: 10 shared prefix + 10 classical + 20 random from start + 10 projection + 10 LLM = 60 actual accesses. Each continuation arm still has a logical total budget of 20. No live software benchmark was rerun; these are charged accesses to the original authors' measurement tables.

Observed model usage: {c['observed_input_tokens']} input tokens, {c['observed_output_tokens']} output tokens, {c['request_wall_seconds']:.3f} request wall seconds. Startup/load cost was {c['model_startup_seconds']:.3f} seconds, separate from request time. Controller fitting cost was {c['development_fit_seconds']:.6f} seconds. Cumulative v6 ledger time including executed analysis was {ledger['experiment_seconds']-baseline['experiment_seconds']:.3f} seconds when this report was generated. Source auditing, coding and unit-test overhead is not called experiment time.

Across {c['proposal_denominator']} LLM proposals: {c['projection_events']} projected, {c['duplicate_events']} exact previously seen duplicates, {c['collision_events']} proposals nearer an acquired candidate than any unacquired candidate, {c['fallback_events']} fallback acquisitions. These counts overlap. A separately labeled post-hoc diagnostic confirms **{diversity['exact_original_prefix_copies']}/{diversity['total_proposals']} proposals exactly copied configurations from the original ten-observation prefix**. There were {diversity['total_unique_within_batch']} unique-within-batch strings across the 30 batches, so the issue is mainly copying observed examples, not just repeating one row ten times. Valid syntax did not imply useful exploration. This diagnosis did not change any controller, threshold, prompt or measured run. Request failures, malformed responses and retries remain in the raw logs; completed status counts are {v['status_counts']}.

Estimated held-out policy deployment needs 15 × 20 = 300 label accesses and only the selected branch; benefit used {p['benefit']['estimated_deployment_requests']} requests with {p['benefit']['selected_observed_input_tokens']} observed input tokens and {p['benefit']['selected_observed_output_tokens']} output tokens. Selected future usage is retrospective evaluation accounting, never a router input. Deployment time in policies.csv excludes startup, fitting and unmeasured router-prediction overhead; it reuses recorded branch times, not a production latency promise. All historical research collection still cost time and inference. **External spending: USD 0.** No cloud-price extrapolation.

The shared follow-up ledger is now {ledger['requests']}/100 attempts, with {100-ledger['requests']} attempts left. Runtime is {ledger['experiment_seconds']:.3f}/1800 seconds, with {1800-ledger['experiment_seconds']:.3f} seconds left. Historical acquired-label total is {1658+c['actual_objective_acquisitions']}; historical attempts including v1 are {100+ledger['requests']}.

## Validation and evidence

- Tests actually executed: **{tests}**.
- Independent verification: {v['verified_pairs']} paired states, all source labels/row IDs, exact prefix restoration, 20-label budgets, all generated token IDs against the recorded grammar, model revision, request cap and router seal timing.
- Raw acquisition journal: `results/v6/acquisitions.jsonl`.
- Prefixes/classical/paired states: `results/v6/prefixes/`, `classical/`, `paired/`.
- Real model evidence: `results/v6/request_starts.jsonl`, `requests.jsonl`, `model_runtime.json`.
- Separate synthetic gate: `results/v6/feasibility/`.
- Frozen protocol/code: `reports/protocol_v6.md`, `protocol_v6.freeze.json`, `results/v6/source_snapshot/`.
- Sealed router: `results/v6/router_seal.json`; machine summaries and reproducible figures in `results/v6/`.
- Test and verification logs: `artifacts/study_v6/`. An initial replay-check bug mutated the verifier's own in-memory prefix; the verifier was corrected to clone it, and full replay then passed. The failure note is preserved; no frozen collection code or raw data changed.

## Limits and next experiment

Three development groups are too few for a stable gain predictor; three test groups cannot establish cross-system generalization. The model is tiny, the proposal grammar is constrained, the empirical features are all binary, and nearest-row projection can dominate model behavior. A single target ignores quality/size/energy tradeoffs. The original measurements have source noise; the case READMEs differ from the global workload summary for MySQL and compression payload size. The admission manifest preserves these discrepancies. Public-benchmark pretraining contamination is unknown. No claim of novelty, publication readiness or professor acceptance follows.

The single most important next experiment is a development-only, paired ablation of the observed prefix-copying behavior: compare the fixed prompt with a predeclared mechanism preventing observed configurations, using the same prefixes and projection controls. It needs a new versioned protocol and enough explicitly approved local calls; only two requests remain. Do not tune on the three exposed test families. Broader generalization work still requires source-valid independent families and a larger allowance; resolve target/transformation and workload lineage before expanding. The current six families are now exposed and should not be reused as untouched test groups in an adaptively tuned follow-up.

## Reproduce

Use the pinned local environment and downloaded source/model manifests. `scripts/admit_v6.py` recreates the semantic manifest without objective reads. `scripts/freeze_v6.py` refuses to overwrite the existing freeze. The collection command refuses to overwrite a completed run; do not delete raw evidence to rerun. An independent fresh-copy reproduction must retain its own collection ledger and explicitly account for additional resources.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_v6.py
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v6
.venv/bin/python scripts/diagnose_v6.py
.venv/bin/python scripts/report_v6.py
```

Analysis regeneration consumes remaining experiment-runtime allowance but makes no model calls or new optimizer label acquisitions. Retrospective evaluator access is distinct from optimizer acquisition. No work is scheduled after this session.
'''
    Path('reports/pilot_report_v6.md').write_text(report)
    print('Wrote reports/pilot_report_v6.md from actual records')
if __name__=='__main__':main()
