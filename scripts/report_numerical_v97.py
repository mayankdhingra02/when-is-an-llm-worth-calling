"""Render saved-data results; no collection, tuning or hidden-label policy input."""
import json, statistics
import numpy as np
from collect_smollm_v47 import ROOT,read,write

def main():
    out=ROOT/'results/v97_analysis';s=read(out/'summary.json');noise=read(out/'cost_noise.json')
    old=read(ROOT/'artifacts/study_v94/router_precommit.json')
    assert old['benefit']['threshold'] is None and old['uncertainty']['threshold'] is None
    cases=s['cases'];assert len(cases)==5
    policies={}
    for policy in ['never','always','random_matched_zero','uncertainty_frozen','benefit_frozen','hindsight_oracle']:
        call=[policy=='always' or (policy=='hindsight_oracle' and c['relative_gains']['full_sequential_3nn']>0) for c in cases]
        gains=[c['relative_gains']['full_sequential_3nn'] if yes else 0. for c,yes in zip(cases,call)]
        policies[policy]=dict(call_mask=call,calls=sum(call),mean_relative_gain=statistics.mean(gains),
            missed_useful=sum(c['relative_gains']['full_sequential_3nn']>=.05 and not yes for c,yes in zip(cases,call)),
            status='nondeployable diagnostic' if policy=='hindsight_oracle' else 'fixed policy; no fitting')
    write(out/'policies.json',{'scope':'frozen degenerate zero-rate router transfer; no learned discrimination',
        'policies':policies,'random_rate':0.,'independent_test_groups':0})
    responses=[json.loads(x) for x in (ROOT/'results/v97_qwen/responses.jsonl').read_text().splitlines()]
    tokens=[r['response'].get('timings',{}).get('prompt_n') for r in responses]
    usage={'returned_actual_prefill_tokens':sum(tokens) if all(v is not None for v in tokens) else None,
           'model_lifecycle':read(ROOT/'results/v97_qwen/ledger.json'),
           'usage_source':'returned response timing counters; missing values remain unknown'}
    write(out/'usage.json',usage)
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    controls=['batch_3nn','full_sequential_3nn','random_full']
    fig,ax=plt.subplots(figsize=(8,4.5))
    for x,control in enumerate(controls):
        gains=[100*c['relative_gains'][control] for c in cases]
        ax.scatter(x+np.linspace(-.12,.12,len(gains)),gains,color='#286DA8',s=36)
        ax.plot([x-.2,x+.2],[statistics.mean(gains)]*2,color='black',lw=2)
    ax.axhline(0,color='gray',lw=1)
    for level in [-5,5]:ax.axhline(level,color='gray',ls='--',lw=.8)
    ax.set_xticks(range(3),['Batch 3NN','Sequential 3NN','Random'])
    ax.set_ylabel('LLM relative incumbent runtime gain (%)')
    ax.set_title('V97: restricted domain, five seeds, one exposed system')
    fig.text(.5,.01,'Dots: paired seeds. Black bars: means. Dashed lines: ±5% practical margin.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.035,1,1]);fig.savefig(out/'paired_gains.png',dpi=180)
    fig.savefig(out/'paired_gains.svg');plt.close(fig)
    g=s['groups']['superlu'];a=s['audit'];n=noise['families']['superlu']
    both=sum(all(c['relative_gains'][k]>=.05 for k in controls[:2]) for c in cases)
    rows=['# V97: restricted-domain paired result','',
        '**Exploratory follow-up on one previously studied system.** No new independent test group, '
        'no retuned controller and no claim of journal readiness. All original V94–V96 evidence is preserved.','',
        '| Comparator | LLM mean relative gain | >=5% benefit cases | >=5% harm cases |',
        '|---|---:|---:|---:|']
    for k in controls:rows.append(f"| {k} | {g[k]['mean_relative_gain']:+.2%} | {g[k]['useful_at_5pct']}/5 | {g[k]['harmful_at_5pct']}/5 |")
    rows+=['',f'LLM cases beating BOTH strong controls by at least5%: **{both}/5**. Positive gain means a faster '
        'measured incumbent. All seeds, including failures, are retained. No population interval is appropriate '
        'for one software system.','',
        '| Seed | Batch 3NN seconds | Sequential 3NN seconds | Random seconds | LLM seconds |',
        '|---|---:|---:|---:|---:|']
    for c in cases:rows.append('| '+str(c['seed'])+' | '+' | '.join(f"{c['arms'][k]:.8f}" for k in controls+['llm'])+' |')
    rows+=['','## Executed scope','',
        f"{a['acquisitions']} freshly charged native acquisitions; {a['valid_acquisitions']} valid, "
        f"{a['failed_worker_acquisitions']} failed workers. Physical journal: {a['physical_starts']} starts / "
        f"{a['physical_return_events']} returns. Independently recomputed {a['certificates_recomputed']} "
        'numerical certificates from saved solution vectors. Each branch uses its identical saved10-label '
        'prefix and10 additional labels. Every selection is replayed from pre-decision/acquired data.','',
        f"Real Qwen3: {a['generation_requests']} requests / {a['responses']} returned responses, "
        f"{a['returned_generated_tokens']} generated tokens; {a['full_context_tokens_summed']} summed context "
        f"tokens and {usage['returned_actual_prefill_tokens']} reported actual prefill tokens. Zero retries. "
        'Model/prompt/runtime provenance and raw responses are saved.','',
        f"Native collection {a['native_stage_seconds']:.3f}s; model lifecycle {a['model_stage_seconds']:.3f}s. "
        f"Peak sampled model RSS {a['peak_model_rss_bytes']:,}bytes. External spendingUSD0; electricity and "
        'hardware cost unknown. No download or installation.','',
        '## Frozen policies and costs','',
        '| Policy | Calls / cases | Mean gain vs sequential | Missed >=5% cases |','|---|---:|---:|---:|']
    for policy,r in policies.items():rows.append(f"| {policy} | {r['calls']}/5 | {r['mean_relative_gain']:+.2%} | {r['missed_useful']} |")
    rows+=['','Benefit/uncertainty thresholds were fixed to never-call by the older development fit; '
        'matched-rate random therefore has zero calls too. Their equality is not a learned-router success. '
        'The hindsight oracle uses both outcomes and is not deployable.','',
        'Actual collection:250 labels (50 shared-prefix+200 continuation), up to750 physical solves, '
        'plus every model request/startup. Estimated deployment of one arm per case:100 total labels '
        '(5×20), up to300 physical solves; always-call would add50 model requests, never-call adds0. '
        'These are accounting scenarios, not a new deployment measurement. The per-case inference-only '
        'break-even reuse counts in summary.json exclude model startup, search differences and noise.','',
        '## Limits and next action','',
        f"Median within-acquisition relative timing range: {n['median_within_acquisition_relative_range']:.2%}. "
        f"Repeated configurations: {n['repeated_configurations_across_collection']}; median relative range "
        f"{n['median_repeated_configuration_relative_range']:.2%}. These are descriptive ranges, not uncertainty bounds. "
        'Selecting the best noisy median can bias apparent runtime improvements. One input/machine and '
        'a changed candidate domain limit comparison with V94; do not attribute differences solely to one '
        'parameter or count these five seeds as independent systems. A clean run does not prove reliability.','',
        'Next decisive research step remains independent replication and additional systems. The next '
        'locally available methodological test is a separately frozen reasoning procedure that reserves '
        'tokens for its final answer; run only on development data until its procedure is validated. '
        'Do not tune against these outcomes or reopen completed V95 collection.','',
        'Raw: `results/v97_native/`, `results/v97_qwen/`. Protocol and hashes: '
        '`reports/protocol_v97.md`, `reports/protocol_v97.freeze.json`. Regenerate with '
        '`scripts/analyze_numerical_v97.py`, `scripts/cost_noise_numerical_v97.py` and '
        '`scripts/report_numerical_v97.py` in the pinned environment. All three are saved-data-only analyses.']
    (ROOT/'reports/numerical_v97.md').write_text('\n'.join(rows)+'\n')
    print(json.dumps({'both_strong_controls_5pct':both,'policies':policies,'usage':usage},indent=2))

if __name__=='__main__':main()
