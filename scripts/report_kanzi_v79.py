"""Generate descriptive tables and separate actual versus branch cost accounting."""
import csv,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    data=read(ROOT/'results/v79_kanzi_analysis/summary.json');assert data['verified']
    raw=ROOT/'results/v79_kanzi_classical';events=read(raw/'acquisitions.json');out=ROOT/'results/v79_kanzi_analysis'
    pairs=[];deploy=[]
    for c in data['cases']:
        a=c['arms'];rf=a['rf_lcb']['confirmed_median_bytes'];preset=a['preset']['confirmed_median_bytes'];delta=rf-preset
        pairs.append({'workload':c['workload'],'seed':c['seed'],'rf_bytes':rf,'preset_bytes':preset,'preset_saved_bytes':delta,'preset_saved_pct':100*delta/rf,'preset_incumbent_config_id':a['preset']['config_id'],'rf_incumbent_config_id':a['rf_lcb']['config_id'],'preset_decision_seconds':a['preset']['decision_seconds'],'rf_decision_seconds':a['rf_lcb']['decision_seconds']})
        for method in ['rf_lcb','preset']:
            subset=[e for e in events if e['workload']==c['workload'] and e['seed']==c['seed'] and e['arm'] in ['prefix',method]]
            assert len(subset)==20
            deploy.append({'workload':c['workload'],'seed':c['seed'],'selected_branch':method,'logical_evaluations':20,'recorded_process_and_verification_seconds':sum(e[p]['wall_seconds'] for e in subset for p in ['compression','decompression'])+sum(e['verification_seconds'] for e in subset),'continuation_decision_seconds':a[method]['decision_seconds'],'confirmed_compression_median_seconds':statistics.median(e['compression']['wall_seconds'] for e in subset if e['purpose']=='confirmation'),'confirmed_decompression_median_seconds':statistics.median(e['decompression']['wall_seconds'] for e in subset if e['purpose']=='confirmation')})
    with (out/'paired_differences.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
    (out/'deployment_estimates.json').write_text(json.dumps({'label':'retrospective single-classical-branch accounting; not measured deployed wall time or monetary valuation','excluded':['prefix selection computation','other orchestration and receipt I/O','any future controller cost'],'model_residency':'No model was loaded for V79; do not substitute for V78 model-resident timings.','branches':deploy},indent=2)+'\n')
    download=read(ROOT/'artifacts/study_v79/download_ledger.json')
    ledger={'new_model_requests':0,'cumulative_model_requests':2051,'new_physical_trials':450,'valid_trials':450,'failed_trials':0,'unattempted_trials':0,'new_application_processes':900,'logical_arm_charges':600,'new_prefix_trials':150,'search_continuation_trials':210,'confirmation_trials':90,'actual_collection_seconds':data['stage_seconds'],'application_process_seconds':data['application_process_seconds'],'peak_sampled_rss_bytes':data['peak_sampled_rss_bytes'],'selection_seconds':{m:sum(c['arms'][m]['decision_seconds'] for c in data['cases']) for m in ['rf_lcb','preset']},'new_download_bytes':download['new_download_bytes'],'cumulative_download_bytes':download['cumulative_download_bytes'],'remaining_download_bytes':download['remaining_download_bytes'],'external_spend_usd':0,'other_monetary_cost':'unknown','v74_through_v79_kanzi_physical_trials':815,'v74_through_v79_kanzi_application_failures':2,'prior_rocksdb_v71_v72_trials':350,'recorded_table_acquisitions_unchanged':26358,'deployment_estimates':'results/v79_kanzi_analysis/deployment_estimates.json','classical_trial_limit':450,'stage_wall_limit_seconds':1800,'no_model_allowance_consumed_or_extended':True}
    (ROOT/'artifacts/study_v79/resource_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
    report='''# V79: cheap preset control on new compression workloads

This is a prospective classical-only follow-up to the exposed V78 result. It compares a V78-informed owner-preset/block strategy with RF on three complete Silesia files. **No LLM was run on these inputs**, so this study cannot establish that the preset matches an unmeasured LLM continuation or that an escalation controller would improve.

## Actual collection and scope

All 450 physical trials completed, with zero failures or retries, across 15 workload/seed pairs. Each of 30 arms used 20 logical labels: ten shared prefix acquisitions, seven arm-specific searches and three charged confirmations. Actual collection totals 150 prefix + 210 continuation-search + 90 confirmation = 450 physical trials, while logical per-arm accounting totals 600. All 90 confirmation byte counts agree within their own three-repeat sets.

The protocol and code were frozen before collection. Inputs were selected by content category and size before any new Kanzi outcome; the preset itself was deliberately informed by V78. No settings or stopping criteria changed after outcomes. All workloads remain ONE Kanzi development group, not three software systems. Seeds are repeated searches, not independent groups. Runtime is the documented V76 buffer-fix adaptation; no model was resident.

## Confirmed sizes

Lower is better. Each case uses the median of three charged confirmations; means average the five fixed seeds within each workload. Percentage savings is (meanRF−meanPreset)/meanRF.

| Workload | RF mean bytes | Preset mean bytes | Preset savings | Wins/ties/losses |
|---|---:|---:|---:|---|
'''
    for name,g in data['workloads'].items():
        report+=f"| {name} | {g['mean_bytes']['rf_lcb']:,.1f} | {g['mean_bytes']['preset']:,.1f} | {g['preset_saved_pct_ratio_of_means']:+.2f}% | {g['preset_wins']}/{g['ties']}/{g['preset_losses']} |\n"
    report+='\nAll cases, including losses:\n\n| Workload | Seed | RF bytes | Preset bytes | Preset savings |\n|---|---:|---:|---:|---:|\n'
    for r in pairs:report+=f"| {r['workload']} | {r['seed']} | {r['rf_bytes']:,} | {r['preset_bytes']:,} | {r['preset_saved_pct']:+.2f}% |\n"
    report+='''
![Paired classical outcomes](../results/v79_kanzi_analysis/classical.png)

## Interpretation boundaries

A cheap preset sweep can test an alternative explanation for prior model-selected settings. Its performance here is measured prospectively on the selected new inputs, but its design is development-informed and the software family remains exposed. No outcome has been substituted for an LLM response. There is no held-out router fit, significance claim, cross-system inference, or pooled comparison of unlike objectives. A loss is retained exactly like a win. No new corpus or seed will be selected merely to improve this table.

## Costs and provenance

'''
    report+=f"Actual collection took {data['stage_seconds']:.2f} seconds, including 900 native application processes; summed process time was {data['application_process_seconds']:.2f} seconds. Peak sampled JVM process-group RSS was {data['peak_sampled_rss_bytes']:,} bytes. Total continuation decision time was RF {ledger['selection_seconds']['rf_lcb']:.6f} seconds and preset {ledger['selection_seconds']['preset']:.6f} seconds across 15 cases. Zero model calls, zero model downloads and zero external spending. Hardware/electricity costs are unknown.\n\n"
    report+='\nConfirmed incumbent process times (mean of five seed medians, seconds; descriptive and host-dependent):\n\n| Workload | RF compression | Preset compression | RF decompression | Preset decompression |\n|---|---:|---:|---:|---:|\n'
    for name in data['workloads']:
        def avg(method,key):return statistics.mean(r[key] for r in deploy if r['workload']==name and r['selected_branch']==method)
        report+=f"| {name} | {avg('rf_lcb','confirmed_compression_median_seconds'):.4f} | {avg('preset','confirmed_compression_median_seconds'):.4f} | {avg('rf_lcb','confirmed_decompression_median_seconds'):.4f} | {avg('preset','confirmed_decompression_median_seconds'):.4f} |\n"
    report+='\nA small selector overhead does not imply a faster selected compressor. Size and native application time remain separate; no arbitrary scalar utility or amortization advantage is asserted.\n\n'
    report+='''Owner-hosted corpus retrieval added 8,181,238 bytes; raw sizes and published MD5 values were checked and SHA256 pins retained. Remaining total-download allowance is 553,914,019 bytes. No blanket redistribution license was established; raw corpus bytes remain in ignored `data/raw/`, outside shareable artifacts. See [workload audit](workload_audit_v79.md) for original-source attribution and caveats. The fixed [protocol](protocol_v79.md) records the owner-preset strategy, duplicate handling and failure/resource rules.

`deployment_estimates.json` separately counts the recorded prefix plus only one chosen continuation. It is retrospective branch accounting and excludes prefix-selection computation, other orchestration/I/O and future controller overhead. Actual collection included both continuations. These estimates are not V78 model-resident costs and not a dollar estimate.

## Checks and reproducibility

The frozen analyzer replays every acquired-only decision, shared prefix, arm order, 20-label budget, charge and selected incumbent; it checks saved headers/settings, checksums and byte-equality receipts. At collection, every valid compressed stream was decompressed and compared exactly. Successful bulky payloads were then removed under the frozen retention rule. Offline replay checks retained evidence, not deleted bytes anew. No failed observations were dropped. 590 tests passed before collection; synthetic tests are separate from measured outcomes. After V80 adapter preparation, the full suite passed 594 tests in 4.04 seconds; V80 inference remains unexecuted.

Raw logs: `results/v79_kanzi_classical/`. Verified JSON, CSV and figures: `results/v79_kanzi_analysis/`. Costs, sources, snapshots and evidence manifest: `artifacts/study_v79/`.

Executed collector: `.venv/bin/python scripts/run_kanzi_v79.py`. Analysis/report: `.venv/bin/python scripts/analyze_kanzi_v79.py` and `.venv/bin/python scripts/report_kanzi_v79.py`. Run analysis regeneration only in a separate copy after sealing. Current read-only history verification: `.venv/bin/python scripts/seal_evidence_v79.py --verify-only`. A fresh collection needs a new output namespace and prospectively bounded scope. No current model process or background experiment remains.

Limitations: three historical public files, one patched software family, one machine, deterministic size objective, sampled resource monitoring, no independent-family holdout or clean-machine V79 rerun. Additional workload diversity is not a substitute for independent software systems. Journal readiness and broad beneficial escalation remain unestablished.
'''
    (ROOT/'reports/kanzi_v79.md').write_text(report)
    print(json.dumps({'paired_cases':len(pairs),'workloads':data['workloads'],'ledger':'artifacts/study_v79/resource_ledger.json'},indent=2))
if __name__=='__main__':main()
