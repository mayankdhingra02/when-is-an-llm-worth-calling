"""Deterministic descriptive report from the two-family real-response extension."""
import json,statistics,os,sys
from collect_smollm_v47 import ROOT,read,write
sys.path.insert(0,str(ROOT/'src'))
from escalation.transfer_v41 import relative_gain

OUT=ROOT/'results/v128_analysis'
def main():
    s=read(OUT/'summary.json');assert s['complete'];arms=s['arms'];am={a['key']:a for a in arms}
    diag=read(OUT/'diagnostics.json');ledger=read(ROOT/'results/v128_proposals/ledger.json')
    raw=[json.loads(x) for x in (ROOT/'results/v128_proposals/responses.jsonl').read_text().splitlines()]
    rows=[]
    for a in arms:
        if a['mode']!='model':continue
        refs={**a['references'],**{m:am[a['base_key']+'_'+m]['target'] for m in ['random_projection','full_batch_3nn']}}
        rows.append({'key':a['base_key'],'dataset':a['dataset'],'system_group':a['system_group'],'seed':a['seed'],
          'target':a['target'],'fallback':a['fallback'],'references':refs,'gains':{m:relative_gain(v,a['target'],a['direction']) for m,v in refs.items()}})
    groups=sorted({r['system_group'] for r in rows});modes=sorted(rows[0]['gains']);families=[]
    for g in groups:
        rs=[r for r in rows if r['system_group']==g]
        families.append({'system_group':g,'cases':len(rs),'means':{m:statistics.mean(r['gains'][m] for r in rs) for m in modes}})
    contrasts={m:{'cases':len(rows),'equal_family_mean':statistics.mean(f['means'][m] for f in families),
        'wins':sum(r['gains'][m]>1e-12 for r in rows),'ties':sum(abs(r['gains'][m])<=1e-12 for r in rows),
        'losses':sum(r['gains'][m]<-1e-12 for r in rows),
        'gain_at_least':{str(th):sum(r['gains'][m]>=th for r in rows) for th in [0,.02,.05,.10]}} for m in modes}
    usage={}
    for field in ['tokens_predicted','tokens_evaluated']:
        vals=[r['response'].get(field) for r in raw]
        usage[field]={'observed_sum':sum(v for v in vals if type(v) is int),'missing_responses':ledger['generation_requests']-sum(type(v) is int for v in vals)}
    normal=[r for r in diag['requests'] if r['condition']=='normal'];projection=[p for r in normal for p in r['projection']]
    result={'scope':'Two exposed families, five paired seeds each; exploratory method extension, not fresh held-out routing',
      'cases':rows,'families':families,'contrasts':contrasts,'normal_valid':sum(r['status']=='valid' for r in normal),
      'intended_requests':12,'returned_responses':len(raw),'label_rotation_probes':diag['label_rotation_probes'],
      'projection':{'decoded':len(projection),'nonzero_distance':sum(p['hamming_distance']>0 for p in projection),
        'repeated':sum(p['repeated_proposal'] for p in projection),'already_observed':sum(p['matches_initial_observation'] for p in projection)},
      'actual_cost':{'ledger':ledger,'usage':usage,'new_recorded_acquisitions':s['actual_new_acquisitions'],'evaluation_seconds':s['stage_seconds']},
      'deployment_model':{'requests_per_escalation':1,'maximum_output_tokens':1024,'new_objective_evaluations':10,
        'historical_prefix_evaluations':10,'future_runtime':'unknown; per-call observations not an end-to-end deployment trace'}}
    write(OUT/'comparison.json',result)
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'artifacts/study_v128/mpl_cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    primary=['full_sequential_3nn','random_projection','full_batch_3nn']
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
    for k,m in enumerate(primary):
        ax.bar([i+(k-1)*.24 for i in range(len(groups))],[100*f['means'][m] for f in families],width=.23,label=m)
    ax.axhline(0,color='black',linewidth=.8);ax.set_xticks(range(len(groups)),groups)
    ax.set_ylabel('Mean relative gain (%)');ax.set_title('Full-domain Qwen3-8B proposals: two exposed families')
    ax.legend(fontsize=8);fig.savefig(OUT/'proposals.png',dpi=150,metadata={'Software':'llm-escalation-study V128'});plt.close(fig)
    lines=['# V128: real full-domain proposals on Storm and MongoDB','',
      'This fixed extension uses two additional software families, both previously exposed. Five seeds per family are repeated cases, not ten independent systems. Source limitations and stricter V52 exclusions remain. No learned controller or new untouched holdout is claimed.','',
      '| Comparator | Mean gain | Wins/ties/losses |','|---|---:|---:|']
    for m,v in contrasts.items():lines.append(f"| {m} | {100*v['equal_family_mean']:.3f}% | {v['wins']}/{v['ties']}/{v['losses']} |")
    lines+=['','| Family | Sequential3NN | Random projection | Full batch3NN |','|---|---:|---:|---:|']
    for f in families:lines.append('| '+f['system_group']+' | '+' | '.join(f"{100*f['means'][m]:.3f}%" for m in primary)+' |')
    lines+=['',f"Normal valid responses: {result['normal_valid']}/10. Additional rotation probes: {json.dumps(result['label_rotation_probes'])}.",
      '',f"Projection diagnostics on {len(projection)} decoded normal proposals: {result['projection']['nonzero_distance']} nonzero-distance, {result['projection']['repeated']} repeated, {result['projection']['already_observed']} matching acquired settings. Failed/missing cases use the frozen full-domain batch fallback and remain in every denominator.",
      '',f"Actual new research collection: {ledger['generation_requests']} real requests/{len(raw)} returns, {ledger['allocated_output_tokens']} allocated tokens; observed generated/prefill tokens {usage['tokens_predicted']['observed_sum']}/{usage['tokens_evaluated']['observed_sum']}. Missing new usage receipts: {usage['tokens_predicted']['missing_responses']}. Model lifecycle {ledger['stage_seconds']:.3f}s; peak sampled RSS {ledger['peak_server_rss_bytes']:,} bytes; server exit {ledger['server_exit_code']}; no retries. Three paired arms per prefix acquired {s['actual_new_acquisitions']} new recorded outcomes in {s['stage_seconds']:.3f}s; every arm shares B10 and ends at B20. Historical prefix/control collection remains charged historically.",
      '', 'All12 intended prompt/grammar contracts were checked and sealed before generation. Strict fixed-width, whitespace-free JSON can be constructed from the pinned vocabulary in at most82 tokens for Storm and202 for MongoDB including EOS; both fit1024. Exact prompt tokens plus1024 fit4096. This prevents the earlier structural budget mistake; it does not guarantee useful predictions. The larger cap/bounded grammar are declared adapter changes from V127, so pooled results are not an identical-treatment confirmation.',
      '', 'Estimated deployment uses one request and ten new objective evaluations when escalating; the two rotation requests and extra paired arms are research overhead. Native runtime, dollars, energy and unseen-system routing benefit remain unmeasured. No cost saving is inferred from recorded-label gains.',
      '', 'These are a limited descriptive check of a method on two further exposed application families, not an unbiased generalization estimate. Do not tune on these outcomes and relabel the same families as test. Do not select whichever comparator gives a favorable mean. The comparison JSON retains every seed, failure and threshold count.',
      '', '![Family comparisons](../results/v128_analysis/proposals.png)', '',
      'Evidence: reports/protocol_v128.md and freeze; artifacts/study_v128/jobs.json; results/v128_proposals raw requests/returns/preflights/ledger; results/v128_analysis sealed choices, acquisition journal and paired states. Source lineage: data/manifest_v119.json (Storm owner DOI10.5281/zenodo.56238), data/manifest_v121.json (MongoDB owner commit a31a1c0411f667728ee5069ae71f2927e6c146c6). No new source-body downloads, native trials or paid/cloud inference.']
    (ROOT/'reports/proposals_v128.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'contrasts':contrasts,'normal_valid':result['normal_valid']},indent=2))
if __name__=='__main__':main()
