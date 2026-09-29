"""Predeclared descriptive report; one family is not five independent systems."""
import json,statistics
from table_check_v119 import ROOT,read,write,MODES
from evaluate_table_v119 import known_sum
OUT=ROOT/'results/v119_analysis'

def report():
    s=read(OUT/'summary.json');assert s['complete'] and len(s['cases'])==5
    rs=s['cases'];comparisons={}
    for mode in MODES:
        gs=[r['gains'][mode] for r in rs]
        comparisons[mode]={'seed_mean':statistics.mean(gs),'wins':sum(g>1e-12 for g in gs),'ties':sum(abs(g)<=1e-12 for g in gs),'losses':sum(g< -1e-12 for g in gs),
          'valid_5pct_wins':sum(g>=.05 and not r['fallback'] for r,g in zip(rs,gs)),
          'threshold_grid':[{'margin':m,'valid_gain_ge':sum(g>=m and not r['fallback'] for r,g in zip(rs,gs)), 'strict_positive_gain_gt_margin':sum(g>m and not r['fallback'] for r,g in zip(rs,gs)),'policy_harm_ge':sum(g<=-m and g<0 for g in gs)} for m in [0,.02,.05,.1]],
          'nondeployable_observed_headroom':statistics.mean(max(g,0) for g in gs)}
    joint=sum(not r['fallback'] and all(r['gains'][m]>=.05 for m in MODES[:2]) for r in rs)
    pc=read(ROOT/'results/v119_classical/policy_precommit.json');assert [r['seed'] for r in pc['rows']]==[r['optimization_seed'] for r in rs]
    policies=[]
    for mode in MODES[:2]:
        gains=[r['gains'][mode] for r in rs]
        masks={**pc['masks'],'hindsight_oracle_diagnostic':[g>0 for g in gains]}
        for name,mask in masks.items():
            chosen=[r for r,m in zip(rs,mask) if m]
            policies.append({'control':mode,'policy':name,'diagnostic':name.endswith('_diagnostic'),
              'intended_cases':5,'escalations':sum(mask),'quality_gain_mean':statistics.mean(g if m else 0 for m,g in zip(mask,gains)),
              'missed_valid_5pct_opportunities':sum(not m and not r['fallback'] and g>=.05 for r,m,g in zip(rs,mask,gains)),
              'harmful_5pct_escalations':sum(m and g<=-.05 for m,g in zip(mask,gains)),
              'selected_model_failures':sum(r['fallback'] for r in chosen),'estimated_logical_objective_budget':100,
              'planned_deployment_requests':sum(mask),'observed_selected_requests':sum(r['charged_requests'] for r in chosen),
              'observed_selected_generated_tokens':known_sum([r['generated_tokens'] for r in chosen]),
              'observed_selected_model_seconds':known_sum([r['model_seconds'] for r in chosen]),
              'cost_scope':'Retrospective selected branch; excludes startup, objective access/controller overhead and unknown native execution cost. Historical/all-arm collection is not free.'})
    result={'scope':s['scope'],'groups':1,'intended_cases':5,'comparisons':comparisons,'joint_valid_5pct_wins':joint,
      'descriptive_success_criterion_met':joint>0 and all(comparisons[m]['seed_mean']>0 for m in MODES[:2]),
      'policies':policies,'new_collection_acquisitions':s['actual_classical_acquisitions']+s['actual_new_llm_acquisitions'],
      'new_model_requests':s['new_model_requests'],'fallbacks':sum(r['fallback'] for r in rs)}
    write(OUT/'comparison.json',result)
    import csv
    with (OUT/'cases.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['seed','llm_recorded_latency','status']+[m+'_relative_gain' for m in MODES])
        for r in rs:w.writerow([r['optimization_seed'],r['target'],r['status']]+[r['gains'][m] for m in MODES])
    text=['# V119: external WordCount recorded-table check','','This experiment evaluates selection of the original authors\' published latency labels, not independently validated execution time or output correctness. It is a separate table-only scope; stronger V52 admission stays closed. Five fixed optimization seeds are repetitions of one Storm family, not five independent systems.','','The source, table, controls, inference settings, controller masks and analysis criterion were fixed before continuation outcomes. No model or threshold was selected using this table\'s results. Existing source/metric limitations remain.','','| Classical control | Mean relative LLM gain | Wins / ties / losses | Valid gains ≥5% |','|---|---:|---:|---:|']
    for mode,c in comparisons.items():text.append(f"| {mode} | {100*c['seed_mean']:.3f}% | {c['wins']} / {c['ties']} / {c['losses']} | {c['valid_5pct_wins']}/5 |")
    text+=['',f"Valid joint ≥5% wins over both co-primary controls: **{joint}/5**. The predeclared descriptive success criterion (positive mean against both and at least one joint win) is **{'met' if result['descriptive_success_criterion_met'] else 'not met'}**. This is not a significance test or a journal-readiness criterion.",'','| Optimization seed | Published-label incumbent selected by LLM arm | Batch 3NN gain | Sequential 3NN gain |','|---|---:|---:|---:|']
    for r in rs:text.append(f"| {r['optimization_seed']} | {r['target']:.6g} | {100*r['gains']['batch_3nn']:.3f}% | {100*r['gains']['full_sequential_3nn']:.3f}% |")
    text+=['','## Frozen controller transfer','','The old V6 controller uses only prefix features and its original development-only preprocessing/thresholds. It was not retrained for this model or relative-gain metric; its transfer is a diagnostic, not calibrated benefit prediction. All policy rows, including development-rate random, matched-rate random and the non-deployable hindsight oracle, are saved in `comparison.json`.','','| Policy | Escalations /5 | Mean gain vs batch | Mean gain vs sequential |','|---|---:|---:|---:|']
    for name in pc['masks']:
        rows=[r for r in policies if r['policy']==name];text.append(f"| {name} | {rows[0]['escalations']} | {100*rows[0]['quality_gain_mean']:.3f}% | {100*rows[1]['quality_gain_mean']:.3f}% |")
    text+=['','## Actual collection and reproducibility','',f"{s['new_model_requests']} real local requests, {len(rs)-result['fallbacks']} valid continuations and {result['fallbacks']} fallbacks. Actual recorded acquisitions: {result['new_collection_acquisitions']} (50 shared-prefix +200 classical +50 LLM/fallback); every logical branch remains B20. Replaying saved evidence adds no acquisition. Model lifecycle: {s['ledger']['stage_seconds']:.3f}s, peak sampled server RSS: {s['ledger']['peak_server_rss_bytes']:,} bytes; actual generated tokens: {s['actual_generated_tokens']}; reported prefill tokens: {s['actual_prefill_tokens']}. Missing response usage: {s['missing_response_usage']}. Startup/loading is retained separately in the raw ledger. Zero new downloads, paid calls or external spending.",'','A deployed policy would use the prefix and one selected branch. Per-policy model-request/token/runtime components are retrospective estimates, excluding loading and unmeasured native application costs. They are not cloud-dollar or end-to-end latency savings. Research collection used all branches and is reported separately.','','Source and protocol: `data/manifest_v119.json`, `reports/protocol_v119.md`; raw prompts/responses: `results/v119_reasoning/`; prefix/control journals: `results/v119_classical/`; model-arm journal and figures: `results/v119_analysis/`. The source table comes directly from the pinned owner ZIP; no derivative target-direction assumption is needed. Throughput was not parsed.','','## Limits','','Only one external table/family and one sampled answer per prefix. The archive does not supply original per-run correctness/failure records or an executed-code manifest; metric-substitution and measurement-duration questions remain. These labels are not fresh native measurements. Public benchmark pretraining contamination is unknown. No pooled confirmatory inference with previously exposed groups, no useful learned-router generalization assertion, and no guarantee of Q2 acceptance. All seeds, failures and controls remain visible regardless of direction.']
    (ROOT/'reports/table_check_v119.md').write_text('\n'.join(text)+'\n')
    import matplotlib
    matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='table-v119'
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.3));xs=list(range(5))
    for j,m in enumerate(MODES):ax.plot(xs,[100*r['gains'][m] for r in rs],marker='o',label=m.replace('_',' '))
    ax.axhline(0,color='gray',linewidth=.8);ax.axhline(5,color='gray',linestyle=':',label='5% practical margin');ax.set_xticks(xs,[r['optimization_seed'] for r in rs]);ax.set_xlabel('Optimization seed — one software family');ax.set_ylabel('Relative gain in recorded latency (%)');ax.set_title('External WordCount table: local LLM versus fixed controls');ax.legend(fontsize=8);ax.grid(alpha=.15);fig.tight_layout();fig.savefig(OUT/'gains.png',dpi=170);fig.savefig(OUT/'gains.svg',metadata={'Date':None});plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k!='policies'},indent=2))

if __name__=='__main__':report()
