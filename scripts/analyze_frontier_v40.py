"""Post-hoc exhaustive allocation upper bounds for frozen V38 outcomes."""
import argparse,csv,hashlib,json,os,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.frontier_v40 import allocation_frontier
from escalation.io import read,write
from escalation.config import load_config
from escalation.size_prompt_v38 import authorization_config
from escalation.resources import Resources
OUT=Path('results/v40_frontier')
BASES=('runtime_only_llm','exact_joint_shortlist','exact_joint_full','runtime_3nn','static_rank')
CONDITIONS=('assigned_ids','reverse_display','reassigned_ids')
SCENARIOS=CONDITIONS+('uniform_presentation_mean','worst_tested_presentation','best_tested_presentation_hindsight')

def calculate():
    for p,h in read('reports/protocol_v40_frontier.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed: '+p)
    summary=read('results/v38_size_prompt/summary.json');pairs=summary['comparisons'];cases=sorted({(r['dataset'],r['seed']) for r in pairs})
    if len(cases)!=10 or {d for d,s in cases}!={'brotli','lrzip'} or any(sum(d==g for d,s in cases)!=5 for g in ('brotli','lrzip')):raise ValueError('Ten balanced cases required')
    values={}
    for r in pairs:
        key=(r['dataset'],r['seed'],r['condition'],r['baseline'])
        if key in values:raise ValueError('Duplicate comparison')
        b,l=F(r['baseline_runtime']),F(r['size_aware_runtime']);values[key]=(b-l)/b
    if len(values)!=150:raise ValueError('All comparisons required')
    records=[]
    for base in BASES:
        for scenario in SCENARIOS:
            gains=[]
            for d,seed in cases:
                rr=[values[(d,seed,c,base)] for c in CONDITIONS]
                gain=values[(d,seed,scenario,base)] if scenario in CONDITIONS else sum(rr,F(0))/3 if scenario=='uniform_presentation_mean' else min(rr) if scenario=='worst_tested_presentation' else max(rr)
                gains.append(gain)
            result=allocation_frontier(gains)
            # Independent exhaustive allocation check, not another sorted-prefix implementation.
            distributions=[[] for _ in range(11)]
            for mask in range(1024):
                selected=[i for i in range(10) if mask&(1<<i)]
                distributions[len(selected)].append(sum((gains[i] for i in selected),F(0))/10)
            for row,dist in zip(result['curves'],distributions):
                if F(row['oracle_gain_fraction'])!=max(dist) or F(row['random_expected_fraction'])!=sum(dist,F(0))/len(dist) or F(row['worst_gain_fraction'])!=min(dist):raise ValueError('Exhaustive allocation mismatch')
                row['positive_allocation_count']=sum(v>0 for v in dist)
                row['positive_allocation_probability_fraction']=str(F(row['positive_allocation_count'],len(dist)))
                row['oracle_cases']=[{'dataset':cases[i][0],'seed':cases[i][1]} for i in row['oracle_indices']]
            result.update(baseline=base,scenario=scenario,case_gains_fraction=[str(g) for g in gains],enumerated_allocations=1024)
            records.append(result)
    influence=[]
    for excluded in cases:
        family_means=[]
        for family in ('brotli','lrzip'):
            vals=[values[(d,seed,'assigned_ids','exact_joint_shortlist')] for d,seed in cases if d==family and (d,seed)!=excluded]
            family_means.append(sum(vals,F(0))/len(vals))
        g=sum(family_means,F(0))/2
        influence.append({'excluded_dataset':excluded[0],'excluded_seed':excluded[1],'equal_family_mean_fraction':str(g),'equal_family_mean_gain':float(g)})
    return {'scope':'Post-hoc finite recorded-case bounds; no learned policy or population inference','cases':[{'dataset':d,'seed':s} for d,s in cases],
            'families':2,'case_count':10,'scenarios':records,'enumerated_allocations':30720,'curve_rows':330,
            'primary_leave_one_case_out':influence,'new_model_calls':0,'new_acquisitions':0,
            'cost_scope':'Exactly k hypothetical calls over ten cases; 200 logical objective evaluations; actual historical collection remains counted. No monetary or latency utility.'}

def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
    styles=[('assigned_ids','Assigned IDs','#176b93','-'),('reverse_display','Reverse display','#b56143','-'),('reassigned_ids','Reassigned IDs','#668054','-'),('worst_tested_presentation','Worst tested presentation','#292929','--')]
    for ax,base,title in zip(axes,('exact_joint_shortlist','exact_joint_full','runtime_3nn'),('Joint3NN shortlist','Joint3NN full domain','Runtime3NN')):
        for scenario,label,color,style in styles:
            r=next(r for r in result['scenarios'] if (r['baseline'],r['scenario'])==(base,scenario))
            ax.plot(range(11),[100*v['oracle_gain'] for v in r['curves']],label=label,color=color,linestyle=style)
        ax.axhline(0,color='gray',lw=.7);ax.set_title('Versus '+title);ax.set_xlabel('Exactly k calls among ten cases');ax.grid(alpha=.15);ax.set_xticks([0,2,4,6,8,10])
    axes[0].set_ylabel('Hindsight mean feasible-runtime gain (%)');axes[-1].legend(fontsize=7)
    fig.suptitle('Available routing opportunity depends on the cheap comparator')
    fig.text(.5,.015,'Exact recorded-case bounds; two exposed families; oracle uses outcomes and is not deployable.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'frontiers.{ext}',dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        if calculate()!=read(OUT/'summary.json'):raise ValueError('Saved summary mismatch')
        print('Verified 30,720 allocations, 330 curve points, all 30 scenarios.');return
    if OUT.exists():raise FileExistsError('Preserve prior result')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'),read('configs/authorization_v38.json'),hashlib.sha256(Path('reports/protocol_v38_size_prompt.freeze.json').read_bytes()).hexdigest())
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        if resource.remaining()<60:raise ValueError('Analysis reserve')
        r=calculate();OUT.mkdir();write(OUT/'summary.json',r)
        rows=[dict(baseline=s['baseline'],scenario=s['scenario'],**v) for s in r['scenarios'] for v in s['curves']]
        with (OUT/'curves.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json');write('artifacts/study_v40/accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'new_requests':after['requests']-before['requests'],'active_since':after['active_since']})
    print(json.dumps([{k:s[k] for k in ('baseline','scenario','maximum_gain','fewest_calls_at_maximum','positive_cases','ties','negative_cases')} for s in r['scenarios']],indent=2))
if __name__=='__main__':main()
