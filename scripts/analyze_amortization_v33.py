"""Real-outcome request recovery scenarios; no provider or objective oracle."""
import argparse,csv,hashlib,json,math,os,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write,lines,digest
from escalation.amortization_v33 import WORK_SECONDS,recovery_threshold,net_saved,presentation_scenarios
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require,MODEL_ID,REVISION
OUT=Path('results/v33_amortization')
BASES=('sequential_3nn','full_classical','static_rank','centroid_shortlist')

def classical(dataset,seed,base):
    key=f'{dataset}_{seed}'
    if base=='full_classical':return read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
    paths={'sequential_3nn':f'results/v29_neighbors/arms/{key}_sequential_3nn.json',
        'static_rank':f'results/v8/static_rank/{key}.json','centroid_shortlist':f'results/v25_shortlist/arms/{key}.json'}
    return read(paths[base])['state']

def best(state,prefix):
    require(len(state['ids'])==len(set(state['ids']))==20,'Twenty unique evaluations')
    require(state['ids'][:10]==prefix['ids'] and state['labels'][:10]==prefix['labels'],'Shared prefix')
    require(len(state['labels'])==20 and all(len(y)==1 and math.isfinite(y[0]) and y[0]>0 for y in state['labels']),'Positive scalar targets')
    return min(y[0] for y in state['labels'])

def calculate():
    for p,h in read('reports/protocol_v33_amortization.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Changed frozen input: '+p)
    verified=read('artifacts/study_v33/model_provenance_replay.json')
    require(verified['verified'] and verified['request_token_and_provenance_replays']==60,'Real model provenance replay')
    jobs=read('data/larger_probe_v22.json')['jobs'];requests=lines('results/v22_larger/requests.jsonl')
    require(len(jobs)==len(requests)==60,'Complete original request denominator')
    records=[]
    for job,req in zip(jobs,requests):
        require(req['job_id']==job['job_id'] and req['messages']==job['messages'],'Exact prepared request')
        require((req['model_id'],req['revision'],req['provider'])==(MODEL_ID,REVISION,'local_transformers'),'Model provenance')
        require(req['namespace']=='measured_v22' and req['status']=='response' and req['retry']==0,'Measured successful request')
        require(req['input_tokens'] is not None and req['output_tokens'] is not None and math.isfinite(req['wall_seconds']) and req['wall_seconds']>=0,'Observed usage required')
        context={k:v for k,v in job.items() if k!='messages'};context.update(namespace='measured_v22',prompt_version='larger_v22',grammar_mode='candidate_order_v19',retry=0)
        require(req['cache_key']==digest({'messages':job['messages'],'model':MODEL_ID,'revision':REVISION,'parameters':req['parameters'],
            'context':context,'parser_projection':'larger_v22','grammar_domains':None,'grammar_mode':'candidate_order_v19'}),'Response cache identity')
        if job['condition']=='assigned_ids_repeat':continue
        prefix=read(f"results/v6/prefixes/{job['dataset']}_{job['seed']}.json")
        arm=read(f"results/v22_larger/arms/{job['job_id']:02d}_llm.json")
        require(arm['prefix_hash']==job['prefix_hash']==prefix['prefix_hash'],'Prefix binding')
        selected=[job['mapping'][s] for s in req['raw_output'].strip().splitlines()]
        require(selected==arm['selected_rows']==arm['state']['ids'][10:],'Real response-to-outcome mapping')
        llm=best(arm['state'],prefix['state'])
        for base in BASES:
            b=best(classical(job['dataset'],job['seed'],base),prefix['state']);gain=(b-llm)/b
            records.append({'dataset':job['dataset'],'system_group':job['system_group'],'seed':job['seed'],
                'baseline':base,'condition':job['condition'],'job_id':job['job_id'],'request_id':req['request_id'],
                'cache_key':req['cache_key'],'baseline_target':b,'llm_target':llm,'gain':gain,
                'request_seconds':req['wall_seconds'],'input_tokens':req['input_tokens'],'output_tokens':req['output_tokens'],
                'recovery_baseline_work_seconds':recovery_threshold(gain,req['wall_seconds'])})
    require(len(records)==180,'All four baselines and45 unique responses')
    cases=[];curves=[];summaries=[]
    for base in BASES:
        for job in [j for j in jobs if j['condition']=='assigned_ids']:
            rows=[r for r in records if r['baseline']==base and r['dataset']==job['dataset'] and r['seed']==job['seed']]
            cases.append({'dataset':job['dataset'],'system_group':job['system_group'],'seed':job['seed'],'baseline':base,**presentation_scenarios(rows)})
        subset=[c for c in cases if c['baseline']==base];families=sorted({c['system_group'] for c in subset})
        equal=lambda values:mean(mean(v for v,g in values if g==family) for family in families)
        scenarios=[]
        for scenario,prefix in [('assigned_ids','assigned'),('uniform_one_presentation','uniform_presentation_mean')]:
            gain_key=prefix+'_gain';cost_key=prefix+'_request_seconds'
            g=equal([(c[gain_key],c['system_group']) for c in subset]);cost=equal([(c[cost_key],c['system_group']) for c in subset])
            scenarios.append({'scenario':scenario,'equal_family_gain':g,'equal_family_request_seconds':cost,
                'always_call_recovery_baseline_work_seconds_per_case':recovery_threshold(g,cost)})
            for work in WORK_SECONDS:
                rows=[(net_saved(c[gain_key],c[cost_key],work),c['system_group']) for c in subset]
                curves.append({'baseline':base,'scenario':scenario,'baseline_work_seconds_per_case':work,
                    'never_call_mean_net_seconds':0.,'always_call_mean_net_seconds':equal(rows),
                    'hindsight_mean_net_seconds':equal([(max(0.,v),g) for v,g in rows]),
                    'hindsight_calls':sum(v>0 for v,g in rows),'always_calls':15,'never_calls':0})
        summaries.append({'baseline':base,'cases':15,'families':3,
            'assigned_positive':sum(c['assigned_gain']>0 for c in subset),'assigned_ties':sum(c['assigned_gain']==0 for c in subset),
            'assigned_harms':sum(c['assigned_gain']<0 for c in subset),
            'uniform_mean_positive':sum(c['uniform_presentation_mean_gain']>0 for c in subset),
            'positive_under_all_three':sum(c['all_three_positive'] for c in subset),'scenarios':scenarios})
    startup={r['startup_wall_seconds'] for r in requests};load={r['model_load_seconds'] for r in requests}
    require(len(startup)==len(load)==1,'Single original model session metadata')
    return {'scope':'Exploratory hypothetical request-time recovery from real cached responses; not deployment savings or learned routing',
        'records':records,'cases':cases,'summaries':summaries,'curves':curves,'work_grid_seconds':list(WORK_SECONDS),
        'historical_v22_collection':{'actual_requests':len(requests),'unique_presentation_requests':45,'exact_repeat_requests':15,
            'request_wall_seconds':sum(r['wall_seconds'] for r in requests),'input_tokens':sum(r['input_tokens'] for r in requests),
            'output_tokens':sum(r['output_tokens'] for r in requests),'startup_wall_seconds_once':next(iter(startup)),
            'model_load_seconds_component_of_startup':next(iter(load))},
        'new_model_calls':0,'new_objective_acquisitions':0,'new_physical_trials':0,
        'cost_caveat':'Only observed request time is recovered; startup, controller, differing objective-evaluation costs and future retries excluded. Target proportionality and acceptable quality are unvalidated assumptions.'}

def render(r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4.3))
    for ax,base,title in [(axes[0],'full_classical','Original classical comparator'),(axes[1],'sequential_3nn','Stronger sequential 3NN comparator')]:
        rows=[c for c in r['curves'] if c['baseline']==base and c['scenario']=='assigned_ids']
        for key,label,color in [('always_call_mean_net_seconds','Always call','#b56143'),('hindsight_mean_net_seconds','Hindsight only (nondeployable)','#176b93')]:
            ax.plot([c['baseline_work_seconds_per_case'] for c in rows],[c[key] for c in rows],marker='o',markersize=3,label=label,color=color)
        ax.axhline(0,color='#666',linestyle='--',label='Never call');ax.set_xscale('symlog',linthresh=1);ax.set_yscale('symlog',linthresh=1)
        ax.set_title(title,fontsize=10);ax.set_xlabel('Assumed future baseline work per case (seconds)');ax.set_ylabel('Mean net seconds after request cost');ax.legend(fontsize=7);ax.grid(alpha=.15)
    fig.suptitle('V33: hypothetical reuse scenario with observed model-request cost')
    fig.text(.5,.015,'Fixed assigned-ID calls; three exposed families. Signed-log axes. No measured deployment or learned policy.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.065,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'recovery.{ext}',dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved scenario differs');print('180 real-response comparisons,60 case scenarios,56 work-grid rows replayed.');return
    require(not OUT.exists(),'Preserve completed analysis')
    before=read('artifacts/resource_ledger_v2.json');cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>30,'Thirty-second analysis reserve');r=calculate();write(OUT/'summary.json',r)
        for name,rows in [('comparisons',r['records']),('cases',r['cases']),('curves',r['curves'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v33/accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],
        'new_model_calls':0,'new_objective_acquisitions':0,'new_physical_trials':0,'active_since':after['active_since']})
    print(json.dumps(r['summaries'],indent=2))

if __name__=='__main__':main()
