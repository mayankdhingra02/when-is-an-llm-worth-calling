"""Report all intended V95 conditions, including generation/format failures."""
import json
from collect_smollm_v47 import ROOT,read

def main():
    s=read(ROOT/'results/v95_analysis/summary.json');rows=s['cases']
    model=ROOT/'results/v95b_reasoning'
    starts=[json.loads(r) for r in (model/'generation_starts.jsonl').read_text().splitlines()]
    responses=[json.loads(r) for r in (model/'responses.jsonl').read_text().splitlines()]
    charged={r['identity'] for r in starts};returned={r['key'] for r in responses}
    coverage={mode:{'intended':18,'charged':sum(r['key'] in charged for r in rows if r['mode']==mode),
        'returned':sum(r['key'] in returned for r in rows if r['mode']==mode),
        'valid':s['modes'][mode]['valid'],
        'unattempted':sum(r['key'] not in charged for r in rows if r['mode']==mode),
        'charged_without_response':sum(r['key'] in charged and r['key'] not in returned for r in rows if r['mode']==mode)}
        for mode in ['thinking','nonthinking']}
    from collect_smollm_v47 import write
    write(ROOT/'results/v95_analysis/coverage.json',coverage)
    lines=['# V95: owner-informed, budget-constrained native decoding','',
        'This development-only comparison changes both thinking mode and owner-recommended sampling policy. '
        'It uses explicit thinking-control prompt prefixes and short generation limits; it is not unrestricted '
        'Qwen3 reasoning, a pure thinking-only causal intervention, or a new held-out evaluation.', '',
        '| Mode | Charged / intended | Valid / returned | Fallbacks | Mean gain vs sequential 3NN | >=5% wins | >=5% harms |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for mode,m in s['modes'].items():
        c=coverage[mode]
        lines.append(f"| {mode} | {c['charged']} / 18 | {m['valid']} / {c['returned']} | {m['fallbacks']} | {m['mean_gain_vs_sequential']:+.2%} | {m['useful_at_5pct_vs_sequential']} | {m['harmful_at_5pct_vs_sequential']} |")
    lines += ['', 'Gain includes the frozen batch-3NN fallback for invalid or unattempted model conditions. '
        'A fallback is never labeled successful LLM selection. Family means weight the six development groups '
        'equally; seeds remain grouped. Every intended condition is retained.', '',
        'Unattempted conditions stopped by a study-level cap are NOT model generation failures. '
        'Their predeclared fallback is included only in the full intended-cohort analysis. '
        'Use charged/returned denominators for model reliability. Unknown usage applies to charged requests '
        'without responses; unattempted conditions made zero requests. See `coverage.json`.', '',
        '| Family | Charged thinking / non-thinking | Thinking + fallback gain | Non-thinking + fallback gain |','|---|---:|---:|---:|']
    for f in sorted(s['family_means']['thinking']):
        counts=[sum(r['key'] in charged for r in rows if r['family']==f and r['mode']==mode) for mode in ['thinking','nonthinking']]
        lines.append(f"| {f} | {counts[0]} / {counts[1]} | {s['family_means']['thinking'][f]['full_sequential_3nn']:+.2%} | {s['family_means']['nonthinking'][f]['full_sequential_3nn']:+.2%} |")
    reasons={}
    for r in rows:
        if r['status']=='completed':continue
        for reason in r['failure_reasons'] or [r['status']]:reasons[reason]=reasons.get(reason,0)+1
    errors=[json.loads(r) for r in (model/'errors.jsonl').read_text().splitlines()] if (model/'errors.jsonl').exists() else []
    lines += ['', 'Failure reasons (a case may have several): `'+json.dumps(reasons,sort_keys=True)+'`.', '',
        'Collector stop/errors: `'+json.dumps(errors,sort_keys=True)+'`.', '',
        '## Actual collection','',
        f"{s['requests']} charged requests, {s['responses']} responses, {s['actual_new_recorded_acquisitions']} new recorded-table acquisitions. "
        f"Model lifecycle {s['ledger']['stage_seconds']:.3f}s plus preserved failed preflight {s['prior_preflight_seconds']:.3f}s; "
        f"peak RSS {s['ledger']['peak_server_rss_bytes']:,} bytes; resource stop {s['ledger']['resource_stop_reason']!r}. "
        'The adapter charged every request before sending. No retries/downloads/paid or cloud calls.', '',
        f"Returned output tokens: {sum(m['generated_tokens_returned'] for m in s['modes'].values()):,}; "
        f"missing usage cases: {sum(m['missing_token_usage_cases'] for m in s['modes'].values())}. "
        f"Summed full-context tokens: {s['summed_full_context_tokens']:,}; reported actual prefill tokens: {s['reported_actual_prefill_tokens']:,}. "
        'Missing/unreturned usage is unknown, never free. The existing shared prefixes and classical branches '
        'have historical collection costs. Deployment would use one 20-label arm, with model cost only when called; '
        'this analysis is not a measured end-to-end deployment benchmark.', '',
        '## Interpretation and limits','',
        'The original V95 preflight made zero generations and stopped at a wrong template-boundary assumption. '
        'V95b corrected the template scaffold and stop_type parser before the first generation, preserving the '
        'original failure and shared request/time limits. Owner sampling settings were checked against server '
        'response metadata. No output repair or outcome-based filtering was performed.', '',
        'The owner recommends much longer output capacity than this local budget. Unfinished thinking proves '
        'failure under this declared budget, not failure of unrestricted thinking. This experiment cannot '
        'establish Q2 readiness, broad model inferiority, router benefit prediction, or new-system generalization. '
        'The V94 two-engine test remains unchanged. Further policy development must use development groups '
        'and receive a new untouched-system evaluation before any confirmatory claim.', '',
        'Raw prompts, outputs, token metadata and failures: `results/v95b_reasoning/`. '
        'Paired branches and acquisition logs: `results/v95_analysis/`. '
        'Original/amended freezes: `reports/protocol_v95.freeze.json`, `reports/protocol_v95b.freeze.json`. '
        'Recreate this report and figure from saved outcomes with `scripts/report_reasoning_v95.py`; '
        'do not rerun `analyze_reasoning_v95.py` over existing outputs, as it is a charged acquisition stage.']
    usage=ROOT/'results/v95_analysis/transport_timeout_usage.json'
    if usage.exists():
        u=read(usage)
        lines += ['', '## Additional observable usage for the timed-out request','',
            f"The sole final request without an HTTP response has server-log usage: {u['server_reported_generated_tokens']:,} generated "
            f"and {u['server_reported_prefill_tokens']:,} prefill tokens. Together with returned responses, "
            f"{u['total_observable_generated_tokens']:,} generated tokens are observable. "
            'The original response-only aggregates remain unchanged. The missing answer cannot be recovered from these counts '
            'and was not fabricated. The request stays a transport timeout and the arm uses its predefined fallback. '
            'See `results/v95_analysis/transport_timeout_usage.json` for the hashed log and exact source lines.']
    (ROOT/'reports/reasoning_v95.md').write_text('\n'.join(lines)+'\n')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    families=sorted(s['family_means']['thinking']);x=np.arange(len(families))
    fig,ax=plt.subplots(figsize=(10,4))
    for offset,mode,color in [(-.18,'thinking','#286DA8'),(.18,'nonthinking','#D17A22')]:
        ys=[100*s['family_means'][mode][f]['full_sequential_3nn'] for f in families]
        label=f"{mode} policy ({s['modes'][mode]['valid']}/18 valid model answers)"
        ax.bar(x+offset,ys,width=.35,label=label,color=color)
    labels=[f+f"\n{sum(r['key'] in charged for r in rows if r['family']==f and r['mode']=='thinking')}/{sum(r['key'] in charged for r in rows if r['family']==f and r['mode']=='nonthinking')} calls" for f in families]
    ax.axhline(0,color='black',lw=.8);ax.set_xticks(x,labels,rotation=15);ax.set_ylabel('Policy gain vs sequential 3NN (%)')
    ax.set_title('V95 development groups: fixed fallback included; no held-out claim');ax.legend()
    fig.tight_layout();out=ROOT/'results/v95_analysis';fig.savefig(out/'mode_gains.png',dpi=180);fig.savefig(out/'mode_gains.svg');plt.close(fig)
    print('Report and figure written; all 36 intended conditions retained')
if __name__=='__main__':main()
