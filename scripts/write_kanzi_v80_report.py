"""Write the pilot report from verified raw-derived summaries; no new experiment."""
import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    data=read(ROOT/'results/v80_kanzi_analysis/summary.json');d=read(ROOT/'results/v80_kanzi_analysis/descriptive_summary.json');audit=read(ROOT/'artifacts/study_v80_execution/supplementary_verification.json');ledger=read(ROOT/'artifacts/study_v80_execution/resource_ledger.json');assert audit['verified']
    def tally(control,key):return sum(c[control][key] for c in d['comparisons'].values())
    report=f'''# V80: does a real local LLM improve over a cheap preset?

The approved batch completed **{data['requests']} real local SmolLM3 requests and 450 new physical trials** on three fixed corpus inputs and five seeds. All trials passed validation; {audit['invalid_responses']} invalid model responses and {audit['fallback_search_slots']} fallback search slots were recorded. This is one exposed Kanzi development family, not a held-out learned-router evaluation.

Across the 15 repeated-search cases, LLM versus RF yielded **{tally('rf_lcb','wins')} wins / {tally('rf_lcb','ties')} ties / {tally('rf_lcb','losses')} losses**; versus the cheap preset it yielded **{tally('preset','wins')} wins / {tally('preset','ties')} ties / {tally('preset','losses')} losses**. These counts are descriptive; workloads and seeds are not independent software systems.

## Confirmed quality

Lower compressed byte count is better. Each case uses three charged confirmations. The means below average five seed medians within each workload; savings compares the ratio of those means. Positive savings favors the LLM. There is no pooled raw-byte statistic across workloads.

| Input | RF mean bytes | Preset mean bytes | LLM mean bytes | LLM saved vs RF | LLM saved vs preset |
|---|---:|---:|---:|---:|---:|
'''
    for w,means in d['means'].items():
        a=d['comparisons'][w]
        report+=f"| {w} | {means['rf_lcb']:,.1f} | {means['preset']:,.1f} | {means['llm']:,.1f} | {a['rf_lcb']['ratio_of_means_saved_pct']:+.3f}% | {a['preset']['ratio_of_means_saved_pct']:+.3f}% |\n"
    report+='\nAll cases, including losses:\n\n| Input | Seed | RF bytes | Preset bytes | LLM bytes |\n|---|---:|---:|---:|---:|\n'
    for c in data['cases']:
        a=c['arms'];report+=f"| {c['workload']} | {c['seed']} | {a['rf_lcb']['median_bytes']:,} | {a['preset']['median_bytes']:,} | {a['llm']['median_bytes']:,} |\n"
    report+='\nProspective 1% descriptive margin (benefit / within margin / harm):\n\n| Input | Comparator | LLM wins/ties/losses | 1% flags | Extra mean decision seconds |\n|---|---|---|---|---:|\n'
    for w,cs in d['comparisons'].items():
        for control,c in cs.items():
            f=c['one_percent_flags'];report+=f"| {w} | {control} | {c['wins']}/{c['ties']}/{c['losses']} | {f['benefit']}/{f['within_margin']}/{f['harm']} | {c['mean_added_decision_seconds']:.3f} |\n"
    report+='''
The 1% flag is a practical descriptive convention, not a significance test, risk bound, or dollar-valued utility. Mean paired percentages are also preserved in JSON and can differ from ratios of means. No threshold was fitted to these outcomes.

![Paired quality and selector time](../results/v80_kanzi_analysis/paired_results.png)

## Protocol, baseline and provenance

User's “Continue” answered the immediately preceding explicit 105-call/450-trial/30-minute/$0/no-download approval question. Receipt: `artifacts/study_v80_execution/user_approval.json`. Original freeze SHA256 `9369379ed6b74d19b5eb031875314ee27303d57027f7783fe525437e688d6814` is unchanged. Initial sandbox process-inspection denial occurred before collection; the exact command then ran with local execution permission. There was no experiment restart.

All three inputs and all five seeds were fixed, including unfavorable classical cases. Each saved V79 ten-label prefix was cloned into fresh RF, preset and LLM arms, each with seven search acquisitions and three charged incumbent confirmations. Thus 900 logical charges include 150 historical prefix trials shared across arms; 450 new physical trials comprise 315 search and 135 confirmation trials. No hidden terminal outcomes or unacquired labels entered decisions. Arm state was isolated and round order randomized as frozen. The model remained resident for every new arm; V79 model-free control timings were not substituted.

The preset is a V78-informed development choice: owner level-7 transform/entropy pair, descending block sizes, with acquired duplicates skipped and RF only after exhaustion of its fixed list. It is not a newly learned gate or a universal preset claim. The LLM prompt uses only fixed input category/size, configuration definitions and acquired observations; corpus filename is omitted. Public-corpus/model pretraining contamination nevertheless remains unknowable.

Same real model and runtime as V78: SmolLM3-3B-Q4_K_M, revision `4965cb60b150737b68a0408c36aeefb65078f894`, GGUF SHA256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`; llama.cpp b11146 offline/loopback, temperature 0, requested seed, 64 output-token cap. Cross-device determinism is not established. Kanzi uses the isolated V76 buffer-reference repair, an explicitly labeled adaptation, not an unmodified owner release. Input owner URLs, MD5 and SHA256 are preserved in the V79 manifest; no raw corpus redistribution rights are asserted.

## Actual collection versus hypothetical deployment cost

'''
    l=data['ledger'];u=data['usage']
    report+=f"Actual wall time: **{l['seconds']:.2f} seconds**, within the 1,800-second cap; 900 native JVM processes. Generation requests: {l['generation_requests']}; all HTTP requests including health/template/tokenization: {l['http_requests']}; retries: {l['retries']}. Observed input tokens: {u['tokens_evaluated']['observed_sum']:,} ({u['tokens_evaluated']['unknown_requests']} requests unknown); output tokens: {u['tokens_predicted']['observed_sum']:,} ({u['tokens_predicted']['unknown_requests']} requests unknown). Startup: {l['startup_seconds']:.3f} seconds; sampled peak model-server RSS: {l['resource_guard']['peak_server_rss_bytes']:,} bytes.\n\n"
    report+='Total continuation decision time across all 15 cases: '+', '.join(f"{m} {seconds:.3f} seconds" for m,seconds in audit['selection_seconds'].items())+'. Native trial-supervision time is recorded separately. Zero new downloads or external spending; hardware and electricity costs are unknown.\n\n'
    report+='''`deployment_estimates.json` accounts for a hypothetical single chosen branch: recorded historical prefix process time plus the selected model-resident continuation and selection time. Model cold startup is separate. Prefix verification/I/O/selection and future router overhead are excluded. These estimates are not new production measurements, monetary valuations, or the actual amount collected: the experiment paid for all three continuations. Confirmed incumbent compression/decompression times are saved in `cases.csv`, separately from size and selector overhead.

## What this does and does not establish

'''
    for control in ['rf_lcb','preset']:
        has_benefit=sum(cs[control]['one_percent_flags']['benefit'] for cs in d['comparisons'].values())
        report+=f"Against {control}, {has_benefit}/15 cases exceeded the prespecified 1% LLM benefit flag. "
    if tally('preset','wins')==0:
        report+='**There is zero observed compressed-size routing headroom beyond the preset in this finite batch.** A hindsight preset/LLM selector gives exactly the preset result in every case, while actual LLM continuation adds decision cost. The four wins against RF therefore do not establish useful escalation beyond this stronger comparator. All requests were valid and no fallback occurred, so malformed responses do not explain this result.\n\n'
    report+='A useful controller would have to identify such cases using only pre-decision information on independent systems; their existence alone does not establish predictability. If no material benefit remains against a strong cheap comparator, learning a gate cannot manufacture it.\n\n'
    diagnostic=read(ROOT/'results/v80_proposal_diagnostic/summary.json')
    same=sum(sum(i==439 for i in w['incumbent_ids_in_seed_order']) for w in diagnostic['workloads'].values())
    report+=f"Post-hoc observed-choice diagnostic: {diagnostic['within_preset_candidate_family']}/{diagnostic['valid_observed_proposals']} valid proposals were in the preset transform/entropy family, and {same}/15 LLM incumbents were candidate439 (the same 2MiB preset setting). This is an observed pattern, not proof of model reasoning, causal mechanism or unseen counterfactual outcomes. No additional calls were made for the diagnostic.\n\n"
    report+='''The JSON includes a hindsight better-of-control-and-LLM reference, explicitly nondeployable. No controller was fitted here. V72's same-model RocksDB comparison remains a separate negative result with a different objective; milliseconds and compression bytes are not pooled. Older router results and cross-platform bundles retain their historical scopes. Neither more seeds nor three Kanzi files creates independent software families. A broadly beneficial escalation result and Q2 readiness remain unestablished.

## Validation and reproducibility

All new trials passed stream checksum, independent header/settings checks and exact decompression at collection. All intended trials are retained in the denominator. Successful bulky outputs were removed only after validation under the frozen retention rule; hashes, raw headers, commands, logs and receipts remain. Offline replay validates those receipts rather than recreating deleted payloads.

The frozen analyzer replays acquired-only classical choices, legal model proposals, shared prefixes, chosen incumbents, round ordering, budgets and saved usage. The supplementary verifier independently checks exact native commands, request order, complete fallback tails, payload parameters and cost/resource counters. Both must pass before this report is generated. The pre-collection frozen suite had 594 passing tests. Synthetic tests are excluded from all measured aggregates.

Raw evidence: `results/v80_kanzi_paired/`. Verified tables/figures/JSON: `results/v80_kanzi_analysis/`. Approval/cost/audit records: `artifacts/study_v80_execution/`. Commands executed: frozen `scripts/run_kanzi_v80.py` with its approval digest, then `scripts/analyze_kanzi_v80.py`, `scripts/verify_kanzi_v80_addendum.py`, `scripts/report_kanzi_v80.py` and `scripts/write_kanzi_v80_report.py`, using `.venv/bin/python`.

A separate local portable bundle supports standard-library reconstruction of saved outcomes without model/runtime binaries or corpus payloads. Its execution and corruption-check receipts, if completed, are under `artifacts/reproduction_v80/`; the bundle is not fresh inference, full RF decision replay, native remeasurement or a clean-machine runtime replication. No publication or push is performed.

Remaining limitations: one exposed patched software family, three historical corpus files, one model and host, a fixed twenty-label budget, small repeated-seed sample, no held-out learned-router study or fresh cross-machine collection. Research conclusions follow all observed cases, not a search for a favorable subset.
'''
    (ROOT/'reports/kanzi_v80.md').write_text(report)
    print(json.dumps({'report':'reports/kanzi_v80.md','versus_rf':{k:tally('rf_lcb',k) for k in ['wins','ties','losses']},'versus_preset':{k:tally('preset',k) for k in ['wins','ties','losses']}}))
if __name__=='__main__':main()
