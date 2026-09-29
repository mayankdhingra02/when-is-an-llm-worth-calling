"""Describe verified V80 paired outcomes; never optimize on these results."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
METHODS=['rf_lcb','preset','llm'];CONTROLS=['rf_lcb','preset']
def main():
    out=ROOT/'results/v80_kanzi_analysis';data=read(out/'summary.json');raw=ROOT/'results/v80_kanzi_paired'
    audit=read(ROOT/'artifacts/study_v80_execution/supplementary_verification.json');assert audit['verified']
    events=read(raw/'acquisitions.json');costs=[json.loads(s) for s in (raw/'selection_costs.jsonl').read_text().splitlines()]
    rows=[];pairs=[];prefixevents=read(ROOT/'results/v79_kanzi_classical/acquisitions.json');estimates=[]
    for c in data['cases']:
        w,seed=c['workload'],c['seed']
        for method,a in c['arms'].items():
            physical=[e for e in events if e['workload']==w and e['seed']==seed and e['arm']==method]
            confirmations=[read(ROOT/e['path']/'result.json') for e in physical if e['purpose']=='confirmation'];assert len(physical)==10 and len(confirmations)==3
            decision=sum(r['seconds'] for r in costs if r['workload']==w and r['seed']==seed and r['arm']==method)
            trialtime=sum(e['supervision']['wall_seconds'] for e in physical)
            rows.append({'workload':w,'seed':seed,'method':method,'config_id':a['config_id'],'confirmed_bytes':a['median_bytes'],'decision_seconds':decision,'continuation_collection_seconds':trialtime,'confirmed_compression_seconds':statistics.median(r['compression']['wall_seconds'] for r in confirmations),'confirmed_decompression_seconds':statistics.median(r['decompression']['wall_seconds'] for r in confirmations),'confirmation_equal':len(set(a['confirmation_bytes']))==1})
            prefix=sum(e[p]['wall_seconds'] for e in prefixevents if e['workload']==w and e['seed']==seed and e['arm']=='prefix' for p in ['compression','decompression'])
            estimates.append({'workload':w,'seed':seed,'policy':'always_'+method,'logical_objective_evaluations':20,'historical_prefix_process_seconds':prefix,'observed_continuation_collection_seconds':trialtime,'observed_decision_seconds':decision,'estimated_seconds_excluding_startup':prefix+trialtime+decision,'cold_model_startup_seconds_if_charged_to_this_case':data['ledger']['startup_seconds'] if method=='llm' else 0})
        bymethod={r['method']:r for r in rows if r['workload']==w and r['seed']==seed}
        for control in CONTROLS:
            base=bymethod[control];llm=bymethod['llm'];saved=base['confirmed_bytes']-llm['confirmed_bytes'];pct=100*saved/base['confirmed_bytes'];added=llm['decision_seconds']-base['decision_seconds']
            pairs.append({'workload':w,'seed':seed,'control':control,'saved_bytes':saved,'saved_pct':pct,'added_decision_seconds':added,'one_percent_flag':'benefit' if pct>=1 else 'harm' if pct<=-1 else 'within_margin'})
    for name,records in [('cases.csv',rows),('paired_differences.csv',pairs)]:
        with (out/name).open('w') as f:wri=csv.DictWriter(f,fieldnames=list(records[0]));wri.writeheader();wri.writerows(records)
    comparisons={}
    for w,means in data['mean_seed_median_bytes_by_workload'].items():
        comparisons[w]={}
        for control in CONTROLS:
            subset=[p for p in pairs if p['workload']==w and p['control']==control]
            comparisons[w][control]={'wins':sum(p['saved_bytes']>0 for p in subset),'ties':sum(p['saved_bytes']==0 for p in subset),'losses':sum(p['saved_bytes']<0 for p in subset),'ratio_of_means_saved_pct':100*(means[control]-means['llm'])/means[control],'mean_paired_saved_pct':statistics.mean(p['saved_pct'] for p in subset),'mean_added_decision_seconds':statistics.mean(p['added_decision_seconds'] for p in subset),'one_percent_flags':{flag:sum(p['one_percent_flag']==flag for p in subset) for flag in ['benefit','within_margin','harm']},'hindsight_control_llm_mean_bytes':statistics.mean(min(c['arms'][control]['median_bytes'],c['arms']['llm']['median_bytes']) for c in data['cases'] if c['workload']==w)}
    summary={'comparisons':comparisons,'means':data['mean_seed_median_bytes_by_workload'],'selection_seconds':audit['selection_seconds'],'all_confirmation_bytes_equal':all(r['confirmation_equal'] for r in rows),'llm_incumbents_from_model':sum(c['arms']['llm']['incumbent_from_real_model_proposal'] for c in data['cases']),'hindsight_label':'Nondeployable retrospective diagnostic; no fitted or deployable router','summed_continuation_collection_seconds':sum(r['continuation_collection_seconds'] for r in rows)}
    (out/'descriptive_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'deployment_estimates.json').write_text(json.dumps({'label':'Modeled one-branch accounting, distinct from actual collection of all three branches','limits':'Historical model-free prefix process time plus model-resident continuation time. Prefix verification/I/O/selection and router overhead excluded. No deployed measurement or dollar valuation. Startup explicitly separate; never sum per-case cold startup as actual batch collection.','branches':estimates},indent=2)+'\n')
    prior=read(ROOT/'artifacts/study_v79/resource_ledger.json')
    ledger={'new_model_requests':data['requests'],'cumulative_model_requests':prior['cumulative_model_requests']+data['requests'],'new_physical_trials':data['new_physical_trials'],'new_native_application_processes':2*data['new_physical_trials'],'new_search_trials':315,'new_confirmation_trials':135,'logical_arm_charges':900,'historical_prefix_physical_trials_reused':150,'actual_collection_seconds':data['ledger']['seconds'],'model_ledger':data['ledger'],'usage':data['usage'],'selection_seconds':audit['selection_seconds'],'summed_continuation_collection_seconds':summary['summed_continuation_collection_seconds'],'new_download_bytes':0,'cumulative_download_bytes':prior['cumulative_download_bytes'],'remaining_download_bytes':prior['remaining_download_bytes'],'external_spend_usd':0,'other_monetary_cost':'unknown','recent_kanzi_v74_through_v80_physical_trials':prior['v74_through_v79_kanzi_physical_trials']+data['new_physical_trials'],'recent_kanzi_historical_application_failures':2,'prior_rocksdb_v71_v72_trials':350,'recorded_table_acquisitions_unchanged':26358,'remaining_generation_allowance':105-data['requests'],'scope_complete':True,'deployment_estimates':'results/v80_kanzi_analysis/deployment_estimates.json'}
    (ROOT/'artifacts/study_v80_execution/resource_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
    cache=ROOT/'.cache/kanzi-v80-plot';cache.mkdir(parents=True,exist_ok=True);os.environ.setdefault('MPLCONFIGDIR',str(cache));os.environ.setdefault('XDG_CACHE_HOME',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(12,7),layout='constrained');seeds=[11,23,37,53,71]
    for j,w in enumerate(data['mean_seed_median_bytes_by_workload']):
        for m,marker,label in zip(METHODS,['^','s','o'],['RF-LCB','Preset','SmolLM3']):
            subset=[r for r in rows if r['workload']==w and r['method']==m]
            axes[0,j].plot(range(5),[r['confirmed_bytes']/1024**2 for r in subset],marker=marker,label=label)
            axes[1,j].plot(range(5),[r['decision_seconds'] for r in subset],marker=marker,label=label)
        axes[0,j].set_title(w)
        for ax in axes[:,j]:ax.set_xticks(range(5),seeds);ax.set_xlabel('Search seed');ax.spines[['top','right']].set_visible(False)
    axes[0,0].set_ylabel('Confirmed compressed MiB (lower is better)');axes[1,0].set_ylabel('Decision seconds');axes[0,0].legend()
    fig.suptitle('V80: real model versus RF and cheap preset, shared prefix of 10\n20 evaluations per arm; three inputs in ONE Kanzi development family')
    fig.savefig(out/'paired_results.png',dpi=160);fig.savefig(out/'paired_results.svg');plt.close(fig)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
