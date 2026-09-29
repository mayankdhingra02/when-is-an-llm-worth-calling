"""Separate evaluator and independent acquired-only replay for V25."""
import argparse,csv,hashlib,json,math,os,sys
from collections import Counter
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write,lines
from escalation.core import State
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
from escalation.resources import Resources
OUT=Path('results/v25_shortlist')

def reference_choice(features,state,pool):
    def mode(ids):return [min(Counter(features[i][j] for i in ids).items(),key=lambda p:(-p[1],p[0]))[0] for j in range(len(features[0]))]
    best,rest=mode(state.best),mode(state.rest)
    available=[i for i in state.order if i in pool and i not in state.ids]
    def distance(a,b):return math.sqrt(sum(x!=y for x,y in zip(a,b))/len(a))
    return min(available,key=lambda i:distance(features[i],best)-distance(features[i],rest))

def calculate():
    for n,h in read('reports/protocol_v25_shortlist.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,'Changed frozen input: '+n)
    progress=read(OUT/'progress.json');require(progress['complete'],'Incomplete experiment; retain full denominator and suppress efficacy')
    m=read('data/manifest_v8.json');journal=lines(OUT/'acquisitions.jsonl');require(len(journal)==150,'150 acquisitions required')
    records=[];replayed=0
    v22=read('results/v22_larger/summary.json')['records']
    for spec in m['datasets']:
        with Path(spec['path']).open() as stream:source=list(csv.DictReader(stream,delimiter=spec['delimiter']))
        features=[];values=[];source_lines=[];seen=set()
        for line,row in enumerate(source,2):
            if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
            feature=tuple(float(row[k]) for k in spec['feature_names'])
            if feature in seen:continue
            seen.add(feature);features.append(feature);values.append(float(row[spec['primary_objective']]));source_lines.append(line)
        require(len(values)==spec['rows'],'Independent schema count')
        lo,hi=min(values),max(values)
        def loss(ids):return 0. if hi==lo else min((values[i]-lo)/(hi-lo) if spec['direction']=='-' else (hi-values[i])/(hi-lo) for i in ids)
        for case in [c for c in m['cases'] if c['dataset']==spec['id']]:
            key=f"{case['dataset']}_{case['seed']}";p=read(f'results/v6/prefixes/{key}.json')['state'];arm=read(OUT/'arms'/f'{key}.json');state=State(**p).clone();pool=case['pool']['ranked']
            state.order=[i for i in p['order'] if i in set(pool)|set(p['ids'])]
            events=[e for e in journal if e['dataset']==case['dataset'] and e['seed']==case['seed']]
            require(len(events)==arm['actual_new_accesses']==10,'Per-arm accounting')
            for e in events:
                selected=reference_choice(features,state,pool);require(selected==e['row_id'],'Independent sequential choice')
                require(e['source_line']==source_lines[selected] and float(e['raw_target'])==values[selected],'Source label identity')
                state.observe(selected,[values[selected]],[spec['direction']]);replayed+=1
            require(state.record()==arm['state'],'Exact state replay')
            require(len(state.ids)==len(set(state.ids))==20 and state.ids[:10]==p['ids'] and state.labels[:10]==p['labels'],'Paired prefix and budget')
            full=read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
            static=read(f'results/v8/static_rank/{key}.json')['state']
            old=[r for r in v22 if r['dataset']==case['dataset'] and r['seed']==case['seed'] and r['condition']!='assigned_ids_repeat'];require(len(old)==3,'Three LLM presentations')
            llm_losses=[]
            for r in old:
                actual=read(f"results/v22_larger/arms/{r['job_id']:02d}_llm.json")['state']
                measured=loss(actual['ids']);require(math.isclose(measured,r['llm_loss'],abs_tol=1e-12),'LLM metric replay');llm_losses.append(measured)
            restricted=loss(state.ids)
            records.append({'dataset':spec['id'],'system_group':spec['system_group'],'seed':case['seed'],
                'restricted_loss':restricted,'full_classical_loss':loss(full['ids']),'static_rank_loss':loss(static['ids']),
                'llm_mean_loss':mean(llm_losses),'llm_best_presentation_loss':min(llm_losses),'llm_worst_presentation_loss':max(llm_losses),
                'branch_seconds':arm['branch_seconds'],'selected_ids':state.ids[10:]})
    fields=['restricted_loss','full_classical_loss','static_rank_loss','llm_mean_loss']
    groups=[{'system_group':g,**{f:mean(r[f] for r in records if r['system_group']==g) for f in fields}} for g in sorted({r['system_group'] for r in records})]
    comparisons={}
    for baseline in fields[1:]:
        gains=[r[baseline]-r['restricted_loss'] for r in records]
        comparisons[baseline]={'mean_gain_favoring_restricted':mean(g[baseline]-g['restricted_loss'] for g in groups),
            'restricted_wins':sum(x>1e-12 for x in gains),'ties':sum(abs(x)<=1e-12 for x in gains),'restricted_losses':sum(x< -1e-12 for x in gains),
            'material_wins':sum(x>.02 for x in gains),'material_losses':sum(x<-.02 for x in gains)}
    return {'scope':'Exploratory development-only matched-shortlist adaptive classical ablation; not independent confirmation',
       'complete':True,'cases':records,'families':groups,'comparisons':comparisons,'new_objective_acquisitions':150,'new_model_calls':0,
       'strictly_beats_all_three_llm_presentations':sum(r['restricted_loss']<r['llm_best_presentation_loss']-1e-12 for r in records),
       'no_worse_than_all_three_llm_presentations':sum(r['restricted_loss']<=r['llm_best_presentation_loss']+1e-12 for r in records),
       'independent_sequential_choices_verified':replayed}

def render(summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(11,3.7))
    for ax,g in zip(axes,summary['families']):
        fields=['full_classical_loss','static_rank_loss','restricted_loss','llm_mean_loss']
        ax.bar(range(4),[g[f] for f in fields],color=['#9aa8b2','#7b8b96','#176B93','#b55b3d'])
        ax.set_xticks(range(4),['Full-space\nclassical','Static\nshortlist','Adaptive\nshortlist','LLM\n3-presentation mean'],fontsize=7)
        ax.set_title(g['system_group']);ax.set_ylabel('Mean normalized loss (lower is better)')
    fig.suptitle('V25: same shortlist, equal objective budgets, no new LLM calls')
    fig.text(.5,.015,'Three exposed development families × five seeds; sequential classical feedback differs from LLM batch selection.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.045,1,.96])
    for ext in ['png','svg']:fig.savefig(OUT/('comparison.'+ext),dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved summary differs');print('15 arms,150 choices/labels and45 LLM metrics independently replayed.');return
    require(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'));before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check();summary=calculate();write(OUT/'summary.json',summary)
        with (OUT/'cases.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=[k for k in summary['cases'][0] if k!='selected_ids']);w.writeheader();w.writerows({k:v for k,v in r.items() if k!='selected_ids'} for r in summary['cases'])
        render(summary);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v25/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'new_model_calls':0,'new_objective_acquisitions':0,'active_since':after['active_since']})
    print(json.dumps({k:summary[k] for k in ['families','comparisons','strictly_beats_all_three_llm_presentations','no_worse_than_all_three_llm_presentations']},indent=2))

if __name__=='__main__':main()
