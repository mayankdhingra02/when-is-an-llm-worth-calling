"""Descriptive reporting of verified real V78 outputs; no collection or tuning."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    out=ROOT/'results/v78_kanzi_analysis';data=read(out/'summary.json')
    audit=read(ROOT/'artifacts/study_v78_execution/supplementary_verification.json');assert audit['verified']
    raw=ROOT/'results/v78_kanzi_paired';events=read(raw/'acquisitions.json')
    costs=[json.loads(s) for s in (raw/'selection_costs.jsonl').read_text().splitlines()]
    rows=[]
    for case in data['cases']:
        seed=case['seed'];llm=case['arms']['llm']['median_bytes']
        for method,a in case['arms'].items():
            decision=sum(c['seconds'] for c in costs if c['seed']==seed and c['arm']==method)
            physical=sum(e['supervision']['wall_seconds'] for e in events if e['seed']==seed and e['arm']==method)
            rows.append({'seed':seed,'method':method,'config_id':a['config_id'],'confirmed_bytes':a['median_bytes'],'decision_seconds':decision,
                         'continuation_collection_seconds':physical,'confirmation_equal':len(set(a['confirmation_bytes']))==1})
    pairs=[]
    for case in data['cases']:
        seed=case['seed'];by_method={r['method']:r for r in rows if r['seed']==seed}
        for control in ['rf_lcb','nn']:
            base=by_method[control];model=by_method['llm'];saved=base['confirmed_bytes']-model['confirmed_bytes']
            added=model['decision_seconds']-base['decision_seconds'];pct=100*saved/base['confirmed_bytes']
            pairs.append({'seed':seed,'control':control,'saved_bytes':saved,'saved_pct':pct,'added_decision_seconds':added,
                          'bytes_saved_per_added_decision_second':saved/added if added>0 else None,
                          'one_percent_flag':'benefit' if pct>=1 else 'harm' if pct<=-1 else 'within_margin'})
    for filename,records in [('cases.csv',rows),('paired_differences.csv',pairs)]:
        with (out/filename).open('w') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    summary={'comparisons':{control:{'wins':sum(r['saved_bytes']>0 for r in pairs if r['control']==control),
        'ties':sum(r['saved_bytes']==0 for r in pairs if r['control']==control),'losses':sum(r['saved_bytes']<0 for r in pairs if r['control']==control),
        'ratio_of_mean_sizes_saved_pct':100*(data['mean_seed_median_bytes'][control]-data['mean_seed_median_bytes']['llm'])/data['mean_seed_median_bytes'][control],
        'mean_saved_pct':statistics.mean(r['saved_pct'] for r in pairs if r['control']==control),
        'one_percent_flags':{flag:sum(r['one_percent_flag']==flag for r in pairs if r['control']==control) for flag in ['benefit','within_margin','harm']}}
        for control in ['rf_lcb','nn']},
        'llm_incumbents_from_model':sum(c['arms']['llm']['incumbent_from_real_model_proposal'] for c in data['cases']),
        'all_confirmation_bytes_equal':all(r['confirmation_equal'] for r in rows),
        'selection_seconds':audit['selection_seconds'],'summed_continuation_collection_seconds':sum(r['continuation_collection_seconds'] for r in rows),
        'hindsight_rf_llm_mean_bytes':statistics.mean(min(c['arms']['rf_lcb']['median_bytes'],c['arms']['llm']['median_bytes']) for c in data['cases']),
        'hindsight_label':'Nondeployable observed upper reference; no controller fitted',
        'mean_seed_median_bytes':data['mean_seed_median_bytes'],'pairs':pairs}
    (out/'descriptive_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    # Modeled deployment is a replay of ONE selected branch, not actual paired collection cost.
    estimates=[]
    prefixevents=read(ROOT/'results/v77_kanzi_classical/acquisitions.json')
    for r in rows:
        prefix=sum(e[p]['wall_seconds'] for e in prefixevents if e['seed']==r['seed'] and e['arm']=='prefix' for p in ['compression','decompression'])
        startup=data['ledger']['startup_seconds'] if r['method']=='llm' else 0
        estimates.append({'seed':r['seed'],'policy':'always_'+r['method'],'logical_objective_evaluations':20,
            'historical_prefix_process_seconds':prefix,'observed_continuation_collection_seconds':r['continuation_collection_seconds'],
            'observed_decision_seconds':r['decision_seconds'],'estimated_seconds_excluding_startup':prefix+r['continuation_collection_seconds']+r['decision_seconds'],
            'cold_model_startup_seconds_if_charged_to_this_case':startup,
            'limits':'Retrospective one-branch accounting; prefix verification/I/O overhead excluded; model-resident control times; no new production runtime measurement, router overhead or dollar estimate'})
    (out/'deployment_estimates.json').write_text(json.dumps(estimates,indent=2)+'\n')
    cache=ROOT/'.cache/kanzi-v78-plot';cache.mkdir(parents=True,exist_ok=True);os.environ.setdefault('MPLCONFIGDIR',str(cache));os.environ.setdefault('XDG_CACHE_HOME',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained');seeds=[11,23,37,53,71];methods=['rf_lcb','nn','llm']
    for m,marker,label in zip(methods,['^','s','o'],['RF-LCB','3NN','SmolLM3']):
        axes[0].plot(seeds,[r['confirmed_bytes']/1024**2 for r in rows if r['method']==m],marker=marker,label=label)
    axes[0].set_xticks(seeds);axes[0].set_xlabel('Seed (one development family)');axes[0].set_ylabel('Confirmed compressed MiB (lower is better)');axes[0].legend()
    axes[1].bar(['RF-LCB','3NN','SmolLM3'],[audit['selection_seconds'][m]/5 for m in methods],color=['#326b9e','#dc9145','#558450']);axes[1].set_ylabel('Mean decision seconds per seed')
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Kanzi: real paired continuations, 20 evaluations per arm\nSame 10-evaluation prefix; generated 16 MiB input; repaired adaptation')
    fig.savefig(out/'paired_results.png',dpi=160);fig.savefig(out/'paired_results.svg');plt.close(fig)
    print(json.dumps({k:v for k,v in summary.items() if k!='pairs'},indent=2))
if __name__=='__main__':main()
