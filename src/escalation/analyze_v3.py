"""Frozen v1 analysis procedure applied to corrected exploratory v3 evidence.
Synthetic feasibility calls count as collection cost, never quality data.
"""
import csv,os,time
from pathlib import Path
import numpy as np
from .io import lines,read,write
from .data import read_table
from .evaluator import evaluate
from .router import GainRouter,UncertaintyRouter,FEATURES,GRID,group_mean

OUT=Path('results/v3/analysis')
def csvout(name,rows):
    if not rows:return
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def assess(rows,mask,name):
    mask=np.asarray(mask,dtype=bool);groups=[r['system_group'] for r in rows]
    loss=np.where(mask,[r['llm_loss'] for r in rows],[r['classical_loss'] for r in rows]);gain=np.asarray([r['gain'] for r in rows]);useful=gain>.02;harm=gain<-.02
    count=len(rows);miss=int(sum(useful&~mask));bad=int(sum(harm&mask))
    tokens=[r['llm']['input_tokens']+r['llm']['output_tokens'] if m and r['llm']['input_tokens'] is not None and r['llm']['output_tokens'] is not None else (0 if not m else None) for r,m in zip(rows,mask)]
    seconds=sum(r['classical']['prefix_seconds']+(r['llm']['branch_seconds'] if m else r['classical']['branch_seconds'])+(r['llm']['feature_seconds'] if name not in ('never','always','hindsight_NONDEPLOYABLE') else 0) for r,m in zip(rows,mask))
    return {'policy':name,'scope':'exploratory_v3_heldout_smoke_only','n_runs':count,'independent_systems':len(set(groups)),'mean_loss_system_weighted':group_mean(loss,groups),'escalations':int(sum(mask)),'escalation_fraction':float(np.mean(mask)),'selected_branch_requests':sum(r['llm']['requests'] for r,m in zip(rows,mask) if m),'selected_branch_tokens':None if None in tokens else sum(tokens),'estimated_selected_branch_seconds':seconds,'logical_deployment_labels':20*count,'missed_useful_count':miss,'useful_count':int(sum(useful)),'missed_useful_rate':None if not sum(useful) else miss/int(sum(useful)),'harmful_escalations':bad,'harmful_per_escalation':None if not sum(mask) else bad/int(sum(mask))}

def main():
    os.chdir(Path(__file__).resolve().parents[2]);OUT.mkdir(parents=True,exist_ok=True)
    classic=lines('results/v3/classical/runs.jsonl');llm=lines('results/v3/runs.jsonl');requests=lines('results/v3/requests.jsonl');validations=lines('results/v3/validation.jsonl')
    if any(r.get('namespace')!='measured' for r in classic+llm):raise ValueError('synthetic/unknown namespace in research input')
    for r in llm:
        checkpoint=Path(f'results/v3/checkpoints/{r["dataset"]}_{r["seed"]}.json')
        if not r['events'] and checkpoint.exists():
            saved=read(checkpoint)
            assert saved['context']['prefix_hash']==r['prefix_hash']
            r['events']=saved['events']
    lookup={(r['dataset'],r['seed']):r for r in classic if r['method']=='ezr_centroid_adapted'}
    pairs=[]
    for l in llm:
        c=lookup[(l['dataset'],l['seed'])]
        assert c['prefix_hash']==l['prefix_hash'] and c['ids'][:10]==l['ids'][:10]
        if l['status']!='completed':continue
        pairs.append({'dataset':l['dataset'],'seed':l['seed'],'system_group':l['system_group'],'split':l['split'],'features':l['features'],'classical_loss':c['loss'],'llm_loss':l['loss'],'gain':c['loss']-l['loss'],'classical':c,'llm':l})
    csvout('paired_gains.csv',[{k:r[k] for k in ['dataset','seed','system_group','split','classical_loss','llm_loss','gain']} for r in pairs])
    summary=[]
    for dataset in sorted(set(r['dataset'] for r in classic)):
        for method in ['random','ezr_centroid_adapted','local_llm_binary_v3']:
            rr=[r for r in classic+llm if r['dataset']==dataset and r['method']==method]
            good=[r for r in rr if r['status']=='completed']
            summary.append({'dataset':dataset,'method':method,'intended':5,'completed':len(good),'mean_loss':float(np.mean([r['loss'] for r in good])) if good else None,'median_loss':float(np.median([r['loss'] for r in good])) if good else None,'mean_delta_percent':float(np.mean([r['delta_percent'] for r in good])) if good and all(r['delta_percent'] is not None for r in good) else None,'mean_branch_seconds':float(np.mean([r['branch_seconds'] for r in good])) if good else None})
    csvout('method_summary.csv',summary)
    # Actual collection keeps failures and both branches. Distinct union is separate.
    union={}
    for r in classic+llm:union.setdefault((r['dataset'],r['seed']),set()).update(r['ids'])
    costs={'actual_label_accesses':sum(r['actual_new_accesses'] for r in classic+llm),'sum_distinct_rows_per_dataset_seed':sum(len(ids) for ids in union.values()),'logical_classical_labels':sum(r['logical_evaluations'] for r in classic),'logical_llm_labels_including_reused_prefix':sum(r['logical_evaluations'] for r in llm),'intended_classical_runs':30,'intended_paired_runs':15,'completed_classical_runs':sum(r['status']=='completed' for r in classic),'completed_paired_runs':len(pairs),'actual_requests':len(requests),'retries':sum(r['retry']>0 for r in requests),'request_errors':sum(r['status']=='error' for r in requests),'malformed_responses':sum(not v['valid'] for v in validations if next(r for r in requests if r['request_id']==v['request_id'])['status']=='response'),'completed_model_responses':sum(r['status']=='response' for r in requests),'timeout_attempts':sum('TimeoutError' in r.get('error','') for r in requests),'worker_unavailable_attempts':sum('worker unavailable' in r.get('error','') for r in requests),'dispatched_model_requests':sum(r['status']=='response' or 'TimeoutError' in r.get('error','') for r in requests),'observed_input_tokens_lower_bound':sum(r['input_tokens'] or 0 for r in requests),'observed_output_tokens_lower_bound':sum(r['output_tokens'] or 0 for r in requests),'input_tokens':sum(r['input_tokens'] for r in requests) if all(r['input_tokens'] is not None for r in requests) else None,'output_tokens':sum(r['output_tokens'] for r in requests) if all(r['output_tokens'] is not None for r in requests) else None,'request_wall_seconds':sum(r['wall_seconds'] for r in requests),'fallback_acquisitions':sum(e['fallback'] for r in llm for e in r['events']),'projected_proposals':sum(e['projected'] for r in llm for e in r['events']),'duplicate_proposals':sum(e['duplicate'] for r in llm for e in r['events']),'collision_proposals':sum(e['collision'] for r in llm for e in r['events']),'external_experiment_spend_usd':0,'electricity_hardware_cost_usd':None,'loading':read('results/v3/model_runtime.json') if Path('results/v3/model_runtime.json').exists() else None,'resource_ledger':read('artifacts/resource_ledger_v2.json')}
    costs.update({'v3_new_llm_label_accesses':sum(r['actual_new_accesses'] for r in llm),'v3_new_classical_label_accesses':sum(r['actual_new_accesses'] for r in classic),'historical_v1_v2_label_accesses':758,'all_version_actual_label_accesses':758+sum(r['actual_new_accesses'] for r in classic+llm),'feasibility_requests':sum(r.get('stage')=='format_gate' for r in requests),'paired_model_requests':sum(r.get('stage')=='paired' for r in requests),'historical_v1_v2_request_attempts':133,'all_version_request_attempts':133+len(requests),'feasibility_quality_excluded':True})
    write(OUT/'costs.json',costs)
    policies=[];curves=[]
    if len(pairs)==15:
        dev=[r for r in pairs if r['split']=='development'];test=[r for r in pairs if r['split']=='heldout_smoke']
        assert set(r['system_group'] for r in dev).isdisjoint(r['system_group'] for r in test)
        masks={};rng=np.random.default_rng(20260924)
        masks['never']=np.zeros(len(test),bool);masks['always']=np.ones(len(test),bool)
        for name,keys in [('benefit',FEATURES),('benefit_without_uncertainty',[k for k in FEATURES if k!='uncertainty']),('gain_from_uncertainty_only',['uncertainty'])]:
            router=GainRouter(keys).fit(dev);t=time.perf_counter();pred=router.predict(test);overhead=(time.perf_counter()-t)/len(test)
            masks[name]=pred>router.threshold
            write(OUT/f'{name}_router.json',{**router.export(),'prediction_seconds_per_run':overhead,'heldout_predictions':pred.tolist()})
            if name=='benefit':
                masks['random_development_rate']=rng.random(len(test))<router.rate
                matched=np.zeros(len(test),bool);matched[rng.permutation(len(test))[:int(sum(masks[name]))]]=True;masks['random_matched_realized_rate_DIAGNOSTIC']=matched
            for threshold in GRID:
                row=assess(test,pred>threshold,name);row['threshold']=None if np.isinf(threshold) else threshold;curves.append(row)
        u=UncertaintyRouter().fit(dev);pred=u.predict(test);masks['uncertainty']=pred>u.threshold
        write(OUT/'uncertainty_router.json',{'threshold':None if np.isinf(u.threshold) else float(u.threshold),'development_curve':u.curve,'development_rate':u.rate})
        for threshold in u.grid:
            row=assess(test,pred>threshold,'uncertainty');row['threshold']=None if np.isinf(threshold) else float(threshold);curves.append(row)
        masks['hindsight_NONDEPLOYABLE']=np.asarray([r['gain']>0 for r in test])
        policies=[assess(test,m,name) for name,m in masks.items()]
        write(OUT/'policy_choices.json',{k:v.tolist() for k,v in masks.items()})
        csvout('policies_heldout_smoke.csv',policies);csvout('threshold_curves.csv',curves)
    else:
        write(OUT/'router_blocked.json',{'reason':'Incomplete paired denominator; no complete-case-only primary policy comparison','complete_pairs':len(pairs),'intended':15})
        dev=[r for r in pairs if r['split']=='development']
        if len(dev)==10:
            prospective=[]
            for d in read('data/manifest_v3.json')['datasets']:
                if d['split']=='heldout_smoke':
                    for seed in [11,23,37,53,71]:
                        p=read(f'results/v3/classical/prefixes/{d["id"]}_{seed}.json')
                        prospective.append({'dataset':d['id'],'seed':seed,'features':p['features']})
            for name,keys in [('benefit',FEATURES),('benefit_without_uncertainty',[k for k in FEATURES if k!='uncertainty']),('gain_from_uncertainty_only',['uncertainty'])]:
                model=GainRouter(keys).fit(dev)
                write(OUT/f'{name}_router_UNEVALUATED.json',{**model.export(),'prospective_predictions':model.predict(prospective).tolist(),'evaluation_status':'not evaluated: held-out paired denominator incomplete'})
            benefit=GainRouter().fit(dev);uncertainty=UncertaintyRouter().fit(dev)
            rng=np.random.default_rng(20260924)
            bmask=benefit.predict(prospective)>benefit.threshold
            umask=uncertainty.predict(prospective)>uncertainty.threshold
            random_mask=rng.random(len(prospective))<benefit.rate
            matched=np.zeros(len(prospective),bool);matched[rng.permutation(len(prospective))[:int(sum(bmask))]]=True
            write(OUT/'uncertainty_router_UNEVALUATED.json',{'threshold':None if np.isinf(uncertainty.threshold) else float(uncertainty.threshold),'development_curve':uncertainty.curve,'evaluation_status':'not evaluated: missing held-out paired outcomes'})
            csvout('prospective_choices_UNEVALUATED.csv',[{'dataset':r['dataset'],'seed':r['seed'],'never':False,'always':True,'benefit':bool(bmask[i]),'uncertainty':bool(umask[i]),'random_development_rate':bool(random_mask[i]),'random_matched_rate_diagnostic':bool(matched[i]),'hindsight_NONDEPLOYABLE':None,'outcome_evaluation':'blocked; no completed paired held-out denominator'} for i,r in enumerate(prospective)])
    plots(classic,llm,pairs,summary,curves)
    write(OUT/'summary.json',{'methods':summary,'policies':policies,'costs':costs,'paired_gains':[{k:r[k] for k in ['dataset','seed','gain']} for r in pairs]})

def plots(classic,llm,pairs,summary,curves):
    os.environ['MPLCONFIGDIR']=str(Path('.cache/matplotlib').resolve())
    os.environ['XDG_CACHE_HOME']=str(Path('.cache').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150})
    fig,axes=plt.subplots(1,3,figsize=(11,3.5),sharey=True)
    for ax,d in zip(axes,['Apache','SQL','X264']):
        for k,method in enumerate(['random','ezr_centroid_adapted','local_llm_binary_v3']):
            values=[r['loss'] for r in classic+llm if r['dataset']==d and r['method']==method and r['status']=='completed']
            ax.scatter(np.full(len(values),k)+np.linspace(-.07,.07,len(values)),values,s=28)
            if values:ax.plot([k-.2,k+.2],[np.mean(values)]*2,color='black',lw=2)
        if d=='X264' and not any(r['dataset']==d and r['status']=='completed' for r in llm):ax.text(2,.015,'blocked',ha='center',fontsize=8,color='gray')
        ax.set_title(d+(' — held-out smoke' if d=='X264' else ' — development'));ax.set_xticks(range(3),['Random','Centroid','Constrained LLM'])
    axes[0].set_ylim(-.01,max(r['loss'] for r in classic+llm if r['status']=='completed')*1.12+.01)
    axes[0].set_ylabel('Best normalized loss (lower is better)');fig.suptitle('Three systems × five seeds — descriptive pilot, no generalization claim');fig.tight_layout();fig.savefig(OUT/'quality.png');fig.savefig(OUT/'quality.pdf');plt.close(fig)
    if pairs:
        fig,ax=plt.subplots(figsize=(8,3.5));colors={'Apache':'#377eb8','SQL':'#ff7f00','X264':'#4daf4a'}
        for i,r in enumerate(pairs):ax.scatter(i,r['gain'],color=colors[r['dataset']])
        ax.axhline(0,color='black',lw=.8);ax.axhline(.02,color='gray',ls='--');ax.axhline(-.02,color='gray',ls='--');ax.set_xticks(range(len(pairs)),[f'{r["dataset"]}\n{r["seed"]}' for r in pairs],fontsize=8);ax.set_ylabel('Classical loss − LLM loss');ax.set_title('Paired continuation gains; dashed lines = predeclared material margin');fig.tight_layout();fig.savefig(OUT/'paired_gains.png');plt.close(fig)
    request_rows=lines('results/v3/requests.jsonl')
    if request_rows:
        counts=[sum(r['status']=='response' for r in request_rows),sum('TimeoutError' in r.get('error','') for r in request_rows),sum('worker unavailable' in r.get('error','') for r in request_rows)]
        fig,ax=plt.subplots(figsize=(7,3.5));bars=ax.barh(['Response returned','Timed out','Worker unavailable\n(not dispatched)'],counts,color=['#d95f02','#7570b3','#888888'])
        ax.bar_label(bars,padding=3);ax.set_xlim(0,max(counts)*1.2);ax.set_xlabel('Count of request attempts');ax.set_title(f'{len(request_rows)} attempts — exploratory v3');ax.invert_yaxis();fig.tight_layout();fig.savefig(OUT/'reliability.png');plt.close(fig)
    if curves:
        fig,ax=plt.subplots(figsize=(6,3.5))
        for name in ['benefit','uncertainty']:
            rr=[r for r in curves if r['policy']==name];ax.plot([r['escalation_fraction'] for r in rr],[r['mean_loss_system_weighted'] for r in rr],'o-',label=name)
        ax.set_xlabel('Escalation fraction');ax.set_ylabel('Held-out smoke loss');ax.set_title('Fixed threshold grids — one system, five seeds');ax.legend();fig.tight_layout();fig.savefig(OUT/'quality_cost_curve.png');plt.close(fig)
if __name__=='__main__':
    from .resources import Resources
    from .config import load_config
    with Resources(load_config('configs/followup_v3.yaml'),'artifacts/resource_ledger_v2.json') as resource:
        resource.check();main();resource.check()
    costs=read(OUT/'costs.json');costs['resource_ledger']=read('artifacts/resource_ledger_v2.json');write(OUT/'costs.json',costs)
    summary=read(OUT/'summary.json');summary['costs']=costs;write(OUT/'summary.json',summary)
