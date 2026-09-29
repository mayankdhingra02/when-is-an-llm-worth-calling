"""Write research checkpoint from actually collected, independently checked receipts."""
import json,shutil,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def main():
    a=read('results/v82_h2_analysis/summary.json');b=read('results/v83_h2_analysis/summary.json')
    summaries=[read(f'results/v{v}_h2_feasibility/summary.json') for v in [81,82,83]]
    snap=R/'artifacts/study_v83/previous_snapshot';snap.mkdir(exist_ok=False);mapping={}
    for n in ['STATUS.md','README.md','reports/next_experiment.md']:
        dest=snap/n;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(R/n,dest);mapping[n]={'snapshot_path':str(dest.relative_to(R)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    (snap/'mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    charges=sum(s['charged_trials'] for s in summaries);valid=sum(s['valid_trials'] for s in summaries);seconds=sum(s['seconds'] for s in summaries)
    disposition='passes the coarse same-host precision screen' if b['precision_pass'] else 'fails the predeclared timing-precision screen'
    table='| Protocol | Profile | Median query seconds | Range / median | Precision pass | Median index/analyze seconds |\n|---|---|---:|---:|---|---:|\n'
    for data in [a,b]:
        for n,p in data['profiles'].items():table+=f"| V{data['version']} | {n} | {p['median_seconds']:.6f} | {p['range_over_median']:.3%} | {p['precision_pass']} | {p['median_index_analyze_seconds']:.6f} |\n"
    next_action=('Freeze a classical-only H2 comparison with the predicate-index prior, a deterministic optimizer, five fixed seeds,20 evaluations/checkpoint10, and independent final confirmations; include index-building amortization and predeclare a practically relevant gain threshold. Do not add model calls before that baseline check.' if b['precision_pass'] else 'Diagnose timing variance with per-suite JIT/GC and process-load instrumentation before further optimizer or model trials. Freeze one bounded diagnostic, retain every repeat, and do not change settings or discard trials to chase a passing threshold.')
    report=f'''# H2 native admission and measurement result, V81–V83

H2 adds a real third native software-family harness. Across these stages, **{charges} physical trials were charged: {valid} validated and one validation failure retained**. V82 and V83 each completed nine correctness-checked trials. V83 **{disposition}**. This is a measurement feasibility result; no optimizer, LLM or router was evaluated on H2.

## Fixed design and adaptations

The query-predicate baseline was selected before timings: indexes `(grp,score)`, `(acct,grp)`, and `tick`, with recompilation off and explicit analysis10000. Reference has no added indexes; contrast retains baseline indexes but forces recompilation and analyzes100rows. A fixed Latin ordering yields three fresh processes/profile. These are feasibility repeats, not independent systems or optimizer seeds.336canonical future configurations are enumerated, but336distinct effective behaviors are not established.

H2 2.3.232 is an unmodified owner/registry dependency. Own generated workload:100000rows, three aggregate SQLtemplates,16parameter sets/template. Java checks every query and Python independently checks stored counts/sums. Warm-up, setup, index-build and inference costs are not silently part of the query-only metric; process cost is retained separately. See [source audit](source_audit_v81.md), [license record](third_party_v81.md), frozen protocols and hashed runtime locks.

V81 stopped after the first physical invocation because INFORMATION_SCHEMA.SETTINGS omitted OPTIMIZE_REUSE_RESULTS. The process exited0 and emitted answers, but protocol validation failed; eight intended trials were unattempted. Do not reinterpret that run as a valid repeat. V82 prospectively switched to the actual embedded Database getter, asserted reuse=false, and kept the original workload. This API is verified against [tagged owner Database.java](https://raw.githubusercontent.com/h2database/h2database/version-2.3.232/h2/src/main/org/h2/engine/Database.java) and [JdbcConnection.java](https://raw.githubusercontent.com/h2database/h2database/version-2.3.232/h2/src/main/org/h2/jdbc/JdbcConnection.java).

V82 correctly returned1728scored aggregate answers, but prior/contrast medians were under0.1seconds; prior range/median exceeded20%. V83 therefore froze32warm-up suites and128scored suites per trial (6144queries), versus1/4inV82. V83 checked55296scored answers. This was a disclosed development measurement amendment, not a hidden rerun or independent confirmation. Criteria remained median>=0.1seconds and range/median<=20% for every profile. This is a coarse diagnostic, not1%measurement precision or formal uncertainty coverage.

## Actual timing evidence

{table}
V82 and V83 have different measurement lengths; do not compare their raw suite seconds as performance changes. All individual repeats remain in machine-readable analysis. Three samples per profile do not establish significance. Index build/analyze costs are excluded from query times; any practical deployment claim must include or amortize them. Timing includes result verification and answer-log construction. No production workload or cross-machine reliability claim follows.

![V83 observed timings](../results/v83_h2_analysis/timings.png)

## Actual costs, limits and failures

Actual stage wall-clock totals: {seconds:.6f}seconds across V81–V83, measured inside runners after hash/preflight/Python-oracle setup. These are not complete human/setup/analysis costs. Each native process, including Java oracle creation, loading, warm-up, query, output, index and analysis, is charged and has a receipt. All completed processes used at most60seconds each and no resource cap was hit. One failed measurement is included, no retries;27intended slots across three protocols,19charged and8unattempted. Each workload invocation is one charge, not one per SQL query. No optimizer arm budget has been consumed by these feasibility profiles.

New model calls0, cumulative2156 unchanged; external spendUSD0. Downloaded2692781bytes, cumulative4817487882bytes,551221238bytes remaining under5GiB. Existing Java/ECJ reused. Earlier Kanzi1265 and RocksDB350 physical trials remain separately counted; recorded-table acquisitions26358 unchanged. Electricity and hardware costs unknown. H2 deployment cost is not yet modeled.

V81/V82/V83 sandbox process-inspection denials happened at preflight before collection, then identical commands ran with permission. Initial retrieval DNS failure transferred zero bytes. V82 initial compilation preparation failed on a missing output-parent directory, corrected before compilation/freeze; no native trial resulted. No experimental repair or retry was hidden. All benchmark processes finished; no continuing background experiment.

## Reproduction and tests

Full explicit test discovery: `.venv/bin/python -m pytest tests -q` → **604passed**, including synthetic rejection tests for incorrect SQL answers, indexes and result-reuse settings. Synthetic fixtures are not measured outcomes. V82 default discovery had573tests; full discovery had600. V81 full discovery had596. Compilation/build receipts, tests and freeze timestamps are retained.

Revalidate saved outputs without new collection: import `analyze` from `scripts/analyze_h2_v82.py` and call `analyze(82)` / `analyze(83)`; the CLI also writes the plots and requires a fresh output directory. Resource/native-command/configuration/output hashes and all exact answers are checked. End-to-end evidence/history check: `.venv/bin/python scripts/seal_h2_v83.py --verify-only`. Runners intentionally refuse existing output directories; fresh collection requires a separate workspace copy preserving the versioned snapshots. No clean-machine remeasurement was performed.

## Research interpretation and next action

H2 is distinct from RocksDB/Kanzi, but its metadata was inspected inV73: it is exposed development data, not a pristine held-out family. This generated workload is not itself a positive escalation finding. Existing V80 remains0wins/10ties/5losses against the cheap preset despite105valid real model calls; that negative result is unchanged. This stage does not establish Q2 readiness, novelty or generalization.

**Next:** {next_action}
'''
    (R/'reports/h2_v83.md').write_text(report)
    status=f'''# STATUS — H2 V81–V83 native feasibility completed

## Resume here

Read `reports/h2_v83.md` and frozen `reports/protocol_v83.md`. H2 source admission, original JDBC harness and actual trials are complete. **{charges} physical charges;{valid} validated,one retained V81 validation failure;eight V81 slots unattempted.** V82/V83 each nine correct trials. V83 **{disposition}**. No new LLM calls; no process remains running. H2 is one exposed development family, distinct from prior Kanzi/RocksDB. This stage does not establish a positive routing result or Q2 readiness.

## Evidence and commands

Raw commands,settings,index metadata,exact answers,times and receipts: `results/v81_h2_feasibility/`, `results/v82_h2_feasibility/`, `results/v83_h2_feasibility/`. Revalidated summaries and inspected figures: `results/v82_h2_analysis/`, `results/v83_h2_analysis/`. Source audit `reports/source_audit_v81.md`; third-party attribution `reports/third_party_v81.md`; source receipts `artifacts/study_v81/download_ledger.json`. Each protocol/compiled harness/runtime is pinned before its measurements. V81 failed because H2 omitted a metadata field; V82 verifies the engine flag directly. V82 timings violated the precision floor/spread; V83 lengthened fixed warm-up and measurement prospectively, without changing configurations. Preserve all stages.

Executed fetch/prepare/run H2 scripts V81–V83 and `analyze_h2_v82.py` for82/83. Full explicit suite:604passed (`artifacts/study_v83/tests_all.log`). Synthetic wrong-answer/index/reuse fixtures excluded from research data. Initial sandbox network/process denials were preflight-only; reruns had required permission. V82 missing build-directory parent fixed before freeze. All native application processes exited0; V81 validation still counted as failure. No model retry, fabricated output or paid request.

Current evidence/history check: `.venv/bin/python scripts/seal_h2_v83.py --verify-only`. Previous root docs preserved at `artifacts/study_v83/previous_snapshot/`; never rewrite frozen old evidence. Timing criteria and limitations are explicit in the report. Saved-output verification is not a clean-machine rerun.

## Costs and prior result

New native H2 trials{charges}; native valid{valid}; native validation failures1. Runner-measured total{seconds:.6f}s excludes initial pin checks/Python oracle and analysis. Model calls0new,2156cumulative. Download2692781newbytes,4817487882cumulative,551221238remaining under5GiB. USD0external spend; electricity/hardware unknown. Recent Kanzi physical trials1265 and RocksDB350 remain separate; recorded-table acquisitions26358 unchanged. H2 querytime excludes setup/index-build; deployment utility is untested.

V80 remains a credible bounded negative result:105realSmolLM3calls,450validtrials;0wins/10ties/5lossesvscheap preset,4/6/5vsRF;9.852seconds extra decisiontime/case. Three inputs are one Kanzi family. See `reports/kanzi_v80.md`, `reports/reproduction_v80.md` and portable ZIP. V80 inference allowance is consumed; no new model batch defined. Read-only/source/classical/reproduction work remains authorized within limits; no paid/cloud/push/contact.

## Single most important next action

{next_action}

Remaining untested: H2 classical budgeted optimization, real model continuation on H2, baseline-adjusted transfer to independent untouched software groups, useful learned routing, practical deployment utility, and clean-machine native/model replication. Scientific honesty takes priority over a positive outcome.
'''
    (R/'STATUS.md').write_text(status)
    p=R/'README.md';s=p.read_text();s=s.replace('**Latest completed experiment (V80):**','**Latest native feasibility (V81–V83):** [H2 report](reports/h2_v83.md).19new physical charges,18validated,one retained validation failure. V83 '+disposition+'. No new model calls or H2 optimization evidence;604tests passed. Start at [STATUS](STATUS.md).\n\n**Latest completed LLM experiment (V80):**');p.write_text(s)
    (R/'reports/next_experiment.md').write_text(f'''# Research decision after H2 V83

Highest priority: {next_action}

H2 admission advances the independent-family infrastructure but remains exposed development data. Do not count workload repeats as independent groups, or use the measurement pilots as hidden optimizer labels. V81 failure and V82 inadequate timing remain in the denominator; V83 {disposition}. See `reports/h2_v83.md`.

After a credible classical measurement/baseline exists, specify a bounded paired local-model study with saved prefixes and a concrete request/time envelope. CurrentV80 inference allowance is exhausted; no new request batch is implied. Any comparison must account for index creation, inference latency, failed trials, repeated confirmations, and amortization rather than raw query-time wins alone.

Next priorities remain clean-machine native/model reproduction; focused primary-source novelty audit of the supported baseline-adjusted negative finding; then adequate independent development/test families before another learned-router claim. V80's cheap preset was never beaten on size (0wins/10ties/5losses), so fitting a gate to those seeds cannot establish advantage. No promise of journal tier/acceptance follows.
''')
    ledger={'h2_charged_trials':charges,'h2_valid_trials':valid,'h2_failed_trials':charges-valid,'h2_unattempted':sum(s['unattempted'] for s in summaries),'runner_wall_seconds':seconds,'new_model_calls':0,'cumulative_model_calls':2156,'new_download_bytes':2692781,'cumulative_download_bytes':4817487882,'remaining_download_bytes':551221238,'external_spend_usd':0,'prior_kanzi_physical_trials':1265,'prior_rocksdb_physical_trials':350,'recorded_table_acquisitions':26358}
    (R/'artifacts/study_v83/cost_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
if __name__=='__main__':main()
