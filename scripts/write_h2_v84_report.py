"""Write the actual V84 result and resumable next research decision."""
import hashlib,json,shutil,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def main():
    d=read('results/v84_h2_analysis/summary.json');assert d['complete'];cases=d['cases']
    snap=R/'artifacts/study_v84/previous_snapshot';snap.mkdir(exist_ok=False);mapping={}
    for n in ['STATUS.md','README.md','reports/next_experiment.md']:
        dest=snap/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,dest);mapping[n]={'snapshot_path':str(dest.relative_to(R)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    (snap/'mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    findings={}
    for arm in ['rf_lcb','random']:
        a=[c['arms'][arm] for c in cases]
        findings[arm]={'mean_gain_vs_prior':statistics.mean(x['gain_vs_prior'] for x in a),'material_gain_flags':sum(x['material_gain_flag'] for x in a),'material_and_precision_flags':sum(x['material_gain_flag'] and x['comparison_precision_pass'] for x in a),'precision_inconclusive':sum(not x['comparison_precision_pass'] for x in a),'same_config_as_prior':sum(x['selected_config_id']==c['arms']['prior']['selected_config_id'] for x,c in zip(a,cases))}
    rf=findings['rf_lcb'];rand=findings['random']
    table='| Seed | RF median s | Random median s | Prior median s | RF gain vs prior | Random gain vs prior |\n|---|---:|---:|---:|---:|---:|\n'
    for c in cases:
        a=c['arms'];table+=f"| {c['seed']} | {a['rf_lcb']['median_seconds']:.6f} | {a['random']['median_seconds']:.6f} | {a['prior']['median_seconds']:.6f} | {a['rf_lcb']['gain_vs_prior']:.2%} | {a['random']['gain_vs_prior']:.2%} |\n"
    headline=f"RF had {rf['material_gain_flags']}/5 and random {rand['material_gain_flags']}/5 descriptive improvements of at least10% over the fixed prior. Gains also passing the repeat-precision screen: RF {rf['material_and_precision_flags']}/5, random {rand['material_and_precision_flags']}/5."
    next_action='Prepare a bounded same-model H2 paired continuation study from these five saved prefixes, with fresh classical controls while the model is resident, explicit query context, and the cheap prior retained. Freeze and review the exact request/resource scope before consuming any new inference allowance. A classical result alone cannot establish that an LLM adds no value.'
    report=f'''# V84: actual budgeted classical H2 result

**165/165 native trials completed and validated across five fixed seeds.** Each RF/random arm used20logical evaluations including10shared prefix,7new search trials and3fresh confirmations. The fixed predicate-index baseline used3/20allowed evaluations, with no optimization. There were no failed trials, retries or unattempted slots, and no model requests.

{headline} Mean per-seed relative gains were RF {rf['mean_gain_vs_prior']:.2%} and random {rand['mean_gain_vs_prior']:.2%}; positive is faster. RF selected exactly the prior configuration in {rf['same_config_as_prior']}/5 cases; random in {rand['same_config_as_prior']}/5. These are descriptive results from ONE exposed H2 development family, not five independent systems or a significance test. No H2 LLM result is present.

## Prospective design

Read [frozen protocol](protocol_v84.md). Same V83 generated100000-row SQL workload and version-pinned H2/Java/harness;32warm-up suites and128scored suites (6144queries) per charged process. Predicate-index prior chosen before V81 timings: indexes(grp,score),(acct,grp),tick; no forced recompilation; analyze10000. All prefixes begin with that prior, then four random candidates and five RF-LCB choices. This equips the cheap optimizer with available domain knowledge rather than requiring an LLM to rediscover a known index pattern.

RF and random then branch from the exact same10observations, without sharing continuation labels. RF uses64trees on log query time, with mean-minus-standard-deviation acquisition and feature-only encodings. This is an original RF adaptation, not an exact EZR/SNAP2 reproduction. Search chooses a candidate using only acquired labels; confirmation locks the best of17 and cannot reselect it after seeing repeats. Random/RF collection order alternates; three-arm confirmations use a fixed rotated Latin order. The standalone prior is not a shared-prefix branch and its lower actual budget is deliberate, not hidden.

## Measured outcomes

{table}
The gain margin10% and repeat range/median limit20% were frozen before collection. Comparisons failing precision: RF {rf['precision_inconclusive']}/5, random {rand['precision_inconclusive']}/5; retain them and treat small differences as inconclusive. The range screen is not a confidence interval, non-inferiority test or domain-wide noise guarantee. Every raw repeat, candidate/configuration, precision flag and modeled index-amortization scenario is in `results/v84_h2_analysis/summary.json` and `per_seed.csv`.

![Confirmation medians](../results/v84_h2_analysis/confirmation.png)

## Cost and reliability accounting

Actual physical charges165 =50prefix +70search continuations +30RF/random confirmation +15fixed-prior confirmation. Logical budgets:200RF/random plus15prior =215, counting shared prefix labels in both branches. Every reliability probe is charged; no repeated configuration is treated as a free label. Prior feasibility19charges remain separate, so cumulative H2 physical count184 (183validated,one historical validation failure).

Runner wall time {d['runner_wall_seconds']:.6f}s; summed native-process time {d['actual_native_wall_seconds']:.6f}s; policy-selection time {d['actual_decision_seconds']:.6f}s. Runner time also includes validation and checkpoint writes; it excludes initial hash/preflight/Python-oracle setup and later analysis. Realized per-arm collection times include reused prefix costs for branch comparison and must not be summed as actual collection cost. These are collection times, not production deployment measurements.

Index/analyze + K*query-suite cost for K=1,10,100 is an explicit modeled sensitivity using acquired confirmation medians; excludes data-load,warm-up and tuning cost. Query-only advantage therefore cannot establish end-to-end savings. No arbitrary conversion of seconds to dollars. New external spendUSD0; electricity/hardware unknown. No new downloads or model calls; cumulative model requests2156 and downloaded4817487882bytes unchanged,551221238bytes remaining under5GiB.

Per process:60second cap,512MiBJavaheap,sampledRSS2GiB,scratch128MiB; stage1800seconds and launch reserve enforced. No bound triggered. Initial sandbox `ps` denial occurred before output creation/collection; the identical frozen command ran with process-inspection permission. No native trial was retried. All processes terminated.

## Evidence and reproducibility

`results/v84_h2_classical/` contains all charges, commands, acquired traces, settings,index metadata, independent exact answers, process receipts, five immutable prefixes and locked incumbents. The frozen analyzer reconstructs every RF/random choice, checks shared prefixes and round order, charges and native commands, and independently verifies **1013760scored query answers**. It does not manufacture unacquired values.

Precollection explicit full suite: **608tests passed** (`artifacts/study_v84/tests_all.log`). The additional tests cover acquired-only decisions, branch state, deterministic selection and budget charging. Synthetic fixtures remain excluded from measured aggregates. The executable protocol hash is f648dd7e4598f207dfc22e301b6fb408cc50f1ab43b5a71dcb0b8226b24ec51f.

Commands actually used: `run_h2_v84.py`, `analyze_h2_v84.py`, `write_h2_v84_report.py`, followed by evidence sealing and local portable reconstruction. The runner/analyzer refuse overwriting existing outputs. For read-only policy replay, import `analyze` from `scripts/analyze_h2_v84.py` and call it in the pinned environment. Full history/integrity verification: `.venv/bin/python scripts/seal_h2_v84.py --verify-only`.

Local portable archive `output/h2_v84_outcome_reconstruction.zip` is built by `scripts/bundle_h2_v84.py`. Its actual replay/corruption-test receipt is `artifacts/reproduction_v84/verification.json`; that file is authoritative for whether verification passed. It includes raw saved outcomes and a standard-library verifier, not the Java runtime/JAR, RF environment or prior whole-study history. Saved-outcome reconstruction is not native or clean-machine remeasurement. No artifact was published or pushed.

## Interpretation and remaining gap

{next_action}

This generated workload and hand-defined index domain do not represent a broad production DB benchmark. The cheap prior is intentionally strong and potentially close to optimal; none of the results establish a global optimum or total absent LLM headroom. Neither additional seeds nor arbitrary prompt changes can substitute for independent software groups. Existing V80's negative LLM result against its cheap preset remains unchanged. [Focused prior-work audit](novelty_boundary_v84.md) identifies overlapping hybrid/reliability ideas and cautions against generalizing3B results to all LLMs. A positive useful router, external validity, a substantial novel contribution and Q2 readiness remain unproved.
'''
    (R/'reports/h2_v84.md').write_text(report)
    (R/'artifacts/study_v84/findings.json').write_text(json.dumps(findings,indent=2)+'\n')
    ledger={'new_physical_trials':165,'new_valid_trials':165,'new_failed_trials':0,'new_unattempted':0,'cumulative_h2_trials':184,'cumulative_h2_valid':183,'cumulative_h2_validation_failures':1,'new_logical_rf_random_evaluations':200,'new_logical_prior_evaluations':15,'new_model_calls':0,'cumulative_model_calls':2156,'new_download_bytes':0,'cumulative_download_bytes':4817487882,'remaining_download_bytes':551221238,'external_spend_usd':0,'actual_native_wall_seconds':d['actual_native_wall_seconds'],'actual_decision_seconds':d['actual_decision_seconds'],'runner_wall_seconds':d['runner_wall_seconds']}
    (R/'artifacts/study_v84/cost_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
    status=f'''# STATUS — V84 H2 classical comparison completed

## Resume here

Read `reports/h2_v84.md` and frozen `reports/protocol_v84.md`. **165/165 actual native trials valid**, five saved10-evaluation prefixes, paired RF/random continuations, standalone cheap predicate-index baseline. RF/random each20logical evaluations including3confirmations; prior only3/20. {headline} No model calls in this stage. This is one exposed H2 development family with a generated workload. No active process, held-out result, positive router or Q2-readiness claim.

## Evidence and actual commands

Raw: `results/v84_h2_classical/`. Immutable prefixes: `prefix_11.json`,23,37,53,71 in that directory. Saved selected configurations and all acquisition/command/resource/output records retained. Analysis/figure: `results/v84_h2_analysis/`; findings/costs: `artifacts/study_v84/`. Full608tests passed before freeze. Frozen analyzer replayed all acquired-only RF/random choices and1013760exact scored query answers, budgets and ordering. No failure/retry; sandbox process inspection initially denied at preflight and exact command then ran with permission.

Executed run/analyze/write/seal H2V84 scripts. Verify complete current evidence/history with `.venv/bin/python scripts/seal_h2_v84.py --verify-only`; root document history is in `artifacts/study_v84/previous_snapshot/`. Do not mutate frozen artifacts. Local portable saved-outcome ZIP and actual isolated replay/corruption checks: `output/h2_v84_outcome_reconstruction.zip`, `artifacts/reproduction_v84/verification.json`. These do not rerun Java/RF/model or establish clean-machine reproduction. Read `reports/novelty_boundary_v84.md` for primary-source checks of related hybrid work/model-capacity limitations; no external code executed.

## Costs and limits

Physical165new; H2cumulative184=183valid+1historicalV81validationfailure, retaining8historicalunattempted. Logical215=200RF/random+15prior;50physical shared-prefix evaluations reused once logically. Runner{d['runner_wall_seconds']:.6f}s; native{d['actual_native_wall_seconds']:.6f}s; selectors{d['actual_decision_seconds']:.6f}s.1800second stage and165charge caps respected. No newmodelcalls/downloads/spend. Cumulative2156modelcalls;4817487882downloadbytes;551221238remaining under5GiB. Prior Kanzi1265/RocksDB350physical trials and26358recorded-table acquisitions unchanged. Electricity/hardware cost unknown. Modeled index amortization excludes loading,warm-up and tuning; do not claim production savings.

Prior V80 remains105realSmolLM3calls/450validtrials,0wins/10ties/5lossesagainstcheap preset,9.852seconds extra decision time/case. See `reports/kanzi_v80.md`. That model allowance is consumed; no new model stage is frozen or authorized here. Classical work and bounded preparation can continue; no paid/cloud/push/contact permissions.

## Single most important next action

{next_action}

Still missing for broad research claim: real H2 LLM continuation, sufficient independent group-held-out paired benefit evidence, practical deployment utility, stronger-model robustness, clean-machine native replication, and defensible novelty. More seeds on this same simple workload do not solve those gaps. Keep the research objective active; do not certify a journal tier from these checks.
'''
    (R/'STATUS.md').write_text(status)
    p=R/'README.md';s=p.read_text();anchor='A reproducible, bounded pilot on cost- and reliability-aware escalation in software-configuration optimization.';s=s.replace(anchor,anchor+'\n\n**Latest classical result (V84):** [H2 budgeted comparison](reports/h2_v84.md),165/165valid native trials,five10-evaluation prefixes,608tests passed. '+headline+' No H2LLM or generalization claim.');p.write_text(s)
    (R/'reports/next_experiment.md').write_text(f'''# Research decision after V84

{headline}

**Priority1:** {next_action}

Use V84 only as exposed development evidence. Any LLM study needs an explicit frozen inference budget, complete provenance and contemporaneous controls under the same memory conditions. Seven candidate requests plus three charged confirmations per continuation preserves the20-label arm budget. Do not silently reuse model-free timings while changing resource contention, or add uncharged reliability probes. Do not use other branches' outcomes in prompts.

**Priority2:** independent-family/model robustness and a prospectively selected realistic workload with correctness/resource guarantees. The generated H2 workload and strong hand-specified prior may leave little headroom; do not select new tasks because already inspected model results look favorable. Independent families matter more than more seeds. A larger model/resource envelope needs explicit scope; no paid/cloud access is assumed.

**Priority3:** clean-machine native/model reproduction and contribution audit against close primary work. Read `reports/novelty_boundary_v84.md`; hybrid optimization/reliability gating already have precedents. The small-model, baseline-sensitive negative finding remains valid but does not establish all-model failure or a novel effective router. Current evidence does not certify Q2 readiness.
''')
if __name__=='__main__':main()
