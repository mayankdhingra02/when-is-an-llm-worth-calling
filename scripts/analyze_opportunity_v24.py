"""Bounded post-hoc routing opportunity and retrospective usage scenarios."""
import argparse,csv,hashlib,json,math,os,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write,lines
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
from escalation.resources import Resources
from escalation.opportunity_v24 import frontier
OUT=Path('results/v24_opportunity')

def calculate():
    for name,h in read('reports/protocol_v24_opportunity.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,'Changed frozen input: '+name)
    cases=read('results/v23_robustness/summary.json')['cases'];requests=lines('results/v22_larger/requests.jsonl')
    require(len(cases)==15 and len({(c['dataset'],c['seed']) for c in cases})==15,'Case denominator')
    groups={c['system_group'] for c in cases}
    require(len(groups)==3 and all(sum(c['system_group']==g for c in cases)==5 for g in groups),'Equal family weights')
    require(len(requests)==60,'Request denominator')
    cost=[]
    for c in cases:
        rows=[r for r in requests if r['dataset']==c['dataset'] and r['seed']==c['seed'] and r['condition']!='assigned_ids_repeat']
        require(len(rows)==3 and {r['condition'] for r in rows}=={'assigned_ids','reverse_display','reassigned_ids'},'Unique cost presentations')
        require(all(r['status']=='response' and r['input_tokens'] is not None and r['output_tokens'] is not None for r in rows),'Usage completeness')
        cost.append({k:mean(r[k] for r in rows) for k in ['wall_seconds','input_tokens','output_tokens']})
    scenarios=[]
    for baseline in ['classical_loss','uniform_expected_loss','first_display_loss','lowest_ids_loss']:
        for scenario in ['mean','minimum']:
            result=frontier([c[baseline][scenario] for c in cases])
            for row in result['curves']:
                selected=row.pop('oracle_selected_indices')
                row['selected_cases']=[{'dataset':cases[i]['dataset'],'seed':cases[i]['seed']} for i in selected]
                row['oracle_selected_observed_usage_mean_scenario']={k:math.fsum(cost[i][k] for i in selected) for k in cost[0]}
                row['random_expected_usage_mean_scenario']={k:row['calls']/15*math.fsum(c[k] for c in cost) for k in cost[0]}
            scenarios.append({'baseline':baseline,'scenario':scenario,**result})
    return {'scope':'Post-hoc hindsight and exact random allocation diagnostics; not learned/deployed routing',
            'cases':15,'families':3,'logical_deployment_evaluations':300,'scenarios':scenarios,
            'enumerated_allocations':sum(s['enumerated_subsets'] for s in scenarios),
            'usage_caveat':'Retrospective mean across three observed presentations; excludes startup, controller/training and historical collection; not predicted cost. Minimum-quality scenario does not identify the latency of the minimizing presentation.'}

def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,baseline,title in zip(axes,['classical_loss','first_display_loss'],['Versus classical','Versus first displayed ten']):
        for scenario,style in [('mean','-'),('minimum','--')]:
            s=next(x for x in result['scenarios'] if x['baseline']==baseline and x['scenario']==scenario)
            for field,color,label in [('oracle_gain','#176B93','Hindsight'),('random_expected_gain','#b55b3d','Random expectation')]:
                ax.plot([r['calls'] for r in s['curves']],[r[field] for r in s['curves']],style,color=color,label=label+' / '+scenario)
        ax.axhline(0,color='black',linewidth=.7);ax.set_title(title);ax.set_xlabel('Exactly k calls across 15 cases');ax.set_ylabel('Mean gain in normalized loss');ax.legend(fontsize=7);ax.grid(alpha=.15)
    fig.suptitle('V24: available routing opportunity in saved development runs')
    fig.text(.5,.012,'Mean/minimum refer to three observed presentations. Hindsight is non-deployable; no new model calls.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.04,1,.95])
    for ext in ['png','svg']:fig.savefig(OUT/('frontiers.'+ext),dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved result differs');print('All eight exact frontiers replayed.');return
    require(not OUT.exists(),'Preserve completed V24 result')
    before=read('artifacts/resource_ledger_v2.json')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>30,'Analysis reserve');result=calculate();resource.check()
        write(OUT/'summary.json',result)
        rows=[{'baseline':s['baseline'],'scenario':s['scenario'],**{k:r[k] for k in ['calls','oracle_gain','random_expected_gain','random_min_gain','random_max_gain','enumerated_subsets']}} for s in result['scenarios'] for r in s['curves']]
        with (OUT/'frontiers.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(result);resource.check()
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No calls allowed')
    write('artifacts/study_v24/accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'new_model_calls':0,'new_objective_acquisitions':0,'external_spend_usd':0,'active_since':after['active_since']})
    print(json.dumps([{k:s[k] for k in ['baseline','scenario','maximum_oracle_gain','fewest_calls_at_maximum']} for s in result['scenarios']],indent=2))

if __name__=='__main__':main()
