"""Saved-evidence coverage/quality/cost report; no tuning or new acquisitions."""
import json,os,statistics
from datetime import datetime
from collections import Counter
from collect_smollm_v47 import ROOT,read,write

def main():
    out=ROOT/'results/v98_analysis';s=read(out/'summary.json');rows=s['cases']
    extra={}
    for mode in ['thinking','nonthinking']:
        rs=[r for r in rows if r['mode']==mode];valid=[r for r in rs if not r['fallback']]
        families=sorted({r['family'] for r in valid})
        means={f:{k:statistics.mean(r['gains'][k] for r in valid if r['family']==f)
                  for k in ['full_sequential_3nn','batch_3nn']} for f in families}
        extra[mode]={'intended':len(rs),'valid':len(valid),'covered_valid_families':families,
            'valid_only_family_means':means,
            'valid_only_group_mean_vs_sequential':statistics.mean(v['full_sequential_3nn'] for v in means.values()) if means else None,
            'valid_only_group_mean_vs_batch':statistics.mean(v['batch_3nn'] for v in means.values()) if means else None,
            'valid_model_both_strong_controls_5pct':sum(all(r['gains'][k]>=.05 for k in ['full_sequential_3nn','batch_3nn']) for r in valid),
            'policy_including_fallback_both_strong_controls_5pct':sum(all(r['gains'][k]>=.05 for k in ['full_sequential_3nn','batch_3nn']) for r in rs),
            'status_counts':dict(Counter(r['status'] for r in rs)),
            'charged_requests':sum(r['charged_requests'] for r in rs),
            'returned_responses':sum(r['returned_responses'] for r in rs),
            'missing_request_usage':sum(r['missing_request_usage'] for r in rs)}
    write(out/'coverage_quality.json',extra)
    responses=[json.loads(x) for x in (ROOT/'results/v98_reasoning/responses.jsonl').read_text().splitlines()]
    costs={}
    for phase in ['thought','final']:
        rs=[r for r in responses if r['phase']==phase]
        costs[phase]={'responses':len(rs),'generated_tokens':sum(r['response']['tokens_predicted'] for r in rs),
            'actual_prefill_tokens':sum(r['response']['timings']['prompt_n'] for r in rs),
            'summed_full_context_tokens':sum(r['response']['tokens_evaluated'] for r in rs),
            'response_wall_seconds_sum':sum(r['wall_seconds'] for r in rs),
            'stop_counts':dict(Counter(r['response']['stop_type'] for r in rs))}
    write(out/'phase_costs.json',costs)
    os.environ['SOURCE_DATE_EPOCH']=str(int(datetime.fromisoformat(read(ROOT/'reports/protocol_v98.freeze.json')['at']).timestamp()))
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib-v98'))
    import matplotlib;matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='llm-escalation-v98'
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    modes=['thinking','nonthinking'];labels=['Reasoning + reserve','Nonthinking']
    axes[0].bar(range(2),[extra[m]['valid'] for m in modes],color=['#286DA8','#737373'])
    axes[0].set_ylim(0,20);axes[0].set_ylabel('Valid final answers / 18 intended')
    axes[0].set_xticks(range(2),labels,fontsize=9)
    for x,m in enumerate(modes):axes[0].text(x,extra[m]['valid']+.3,f"{extra[m]['valid']}/18",ha='center')
    for x,m in enumerate(modes):
        vals=[100*g['full_sequential_3nn'] for g in s['family_means'][m].values()]
        axes[1].scatter([x]*len(vals),vals,s=35,color=['#286DA8','#737373'][x])
        axes[1].plot([x-.2,x+.2],[statistics.mean(vals)]*2,color='black',lw=2)
    axes[1].axhline(0,color='gray',lw=1)
    for y in [-5,5]:axes[1].axhline(y,color='gray',ls='--',lw=.8)
    axes[1].set_xticks(range(2),labels,fontsize=9)
    axes[1].set_ylabel('Policy gain vs sequential 3NN (%)')
    axes[1].set_title('Six system means; includes fallback')
    fig.suptitle('V98: development-only final-answer reserve')
    fig.tight_layout();fig.savefig(out/'coverage_quality.png',dpi=180);fig.savefig(out/'coverage_quality.svg');plt.close(fig)
    lines=['# V98: reasoning with a final-answer reserve','',
        '**Development-only methodological comparison.** The previous V95 and V97 studies remain unchanged. '
        'This adds no independent held-out software systems and does not establish a learned router.','',
        '| Procedure | Valid finals / intended | Mean policy gain vs sequential | Valid model >=5% wins vs BOTH strong controls |',
        '|---|---:|---:|---:|']
    for m in modes:lines.append(f"| {m} | {extra[m]['valid']}/18 | {s['modes'][m]['mean_gain_vs_sequential']:+.2%} | {extra[m]['valid_model_both_strong_controls_5pct']} |")
    lines+=['','Thinking uses up to512 tokens followed by a separate128-token final-answer request. '
        'The actual first response is reused verbatim; the end-of-thinking delimiter is explicit prompt '
        'control, not recorded as model output. Nonthinking has one128-token request. Both use native '
        'decoding and owner-informed mode-specific sampling. Strict ten-unique-ID parsing is unchanged. '
        'Mode and sampling differ together, so this is not a pure causal ablation of reasoning alone.','',
        '## All system groups','',
        '| System | Reasoning policy vs sequential | Nonthinking policy vs sequential | Reasoning policy vs batch | Nonthinking policy vs batch |',
        '|---|---:|---:|---:|---:|']
    for f in sorted(s['family_means']['thinking']):
        values=[s['family_means'][m][f][k] for k in ['full_sequential_3nn','batch_3nn'] for m in modes]
        lines.append('| '+f+' | '+' | '.join(f'{v:+.2%}' for v in values)+' |')
    lines+=['','Each group has three seeds per mode. System means, not seed counts, are the independent-domain '
        'unit; all six systems were already exposed during development. Full intended-policy means include '
        'the fixed classical fallback for failures/unattempted cases. Such gains are not attributed to the LLM. '
        'Valid-only coverage and means are retained separately in `coverage_quality.json`; do not silently '
        'drop failures or confuse partial coverage with the intended36-condition comparison.','',
        '## Reliability and actual cost','',f"Charged model requests:{s['requests']}; returned responses:{s['responses']}; "
        f"lifecycle:{s['ledger']['stage_seconds']:.3f}s; peakRSS:{s['ledger']['peak_server_rss_bytes']:,}bytes. "
        f"Allocated output ceiling consumed:{s['ledger']['allocated_output_tokens']:,}tokens. No retries. "
        f"Returned generated tokens:{sum(c['generated_tokens'] for c in costs.values()):,}; "
        f"reported actual prefill:{s['reported_actual_prefill_tokens']:,}; summed full context:{s['summed_full_context_tokens']:,}. "
        'Both inference phases and repeated prefill are counted. Missing response usage, if any, remains unknown.','',
        f"Newly charged recorded-table accesses:{s['actual_new_recorded_acquisitions']}, covering all36 intended "
        'arms with ten continuation labels each. Each uses its saved10-label prefix for logicalB20. '
        'Old prefix/classical-reference collection is historical cost and is not free. No native numerical '
        'workload was executed in this stage. New downloads0, external spendUSD0; electricity/hardware unknown.','',
        'For modeled deployment, a thinking escalation uses up to2 model requests and640 allocated output '
        'tokens; nonthinking uses1 request and128 tokens. Both select at most10 new configurations after '
        'the same10-label checkpoint. This is an accounting scenario, not measured deployed savings.','',
        '## Limits and interpretation','',
        'This is an adaptation of prior budget-forcing ideas with a small quantized model and a short '
        'reasoning allowance. Final-answer delivery and selection quality are separate outcomes. No result '
        'here establishes unrestricted reasoning quality, model-wide behavior, novel routing ability or '
        'publication readiness. Public-benchmark contamination and exposed development data remain limitations. '
        'Do not choose a new threshold, prompt or budget using held-out outcomes.','',
        'Raw prompts, thought/final responses, controls, usage and failures: `results/v98_reasoning/`. '
        'Saved acquired labels and outcomes: `results/v98_analysis/`. Protocol/code/model/data freeze: '
        '`reports/protocol_v98.freeze.json`. The budget-forcing source audit explicitly distinguishes '
        'prior work from this adaptation.','',
        'Reproduce saved-data audit with `scripts/verify_reasoning_v98.py` and report with '
        '`scripts/report_reasoning_v98.py`. Do not rerun `analyze_reasoning_v98.py` into existing results: '
        'it is the once-only charged acquisition step.']
    (ROOT/'reports/reasoning_v98.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'coverage_quality':extra,'phase_costs':costs},indent=2))

if __name__=='__main__':main()
