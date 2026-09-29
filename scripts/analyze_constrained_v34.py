"""Independent source, decision, budget and Decimal scoring replay."""
import argparse,csv,hashlib,math,os,sys
from collections import Counter
from decimal import Decimal
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write,lines,digest
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
from analyze_verify_classical_v17 import manual_choice
from prepare_constrained_v34 import prepare
OUT=Path('results/v34_constrained')
MODES=('joint_shortlist','joint_full','static_rank','runtime_3nn','cached_llm_assigned_ids','cached_llm_reverse_display','cached_llm_reassigned_ids')
BASES=MODES[:4]

def calculate():
    for p,h in read('reports/protocol_v34_constrained.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Changed frozen input: '+p)
    m=read('data/constrained_v34.json');require(m==prepare(),'Prepared action provenance differs')
    tables={}
    for d in m['datasets']:
        xs=[];ys=[];raw=[];source=[];seen=set()
        with Path(d['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
                if any(row[k]!=str(v) for k,v in d['filters'].items()):continue
                x=tuple(float(row[n]) for n in d['feature_names'])
                if x in seen:continue
                seen.add(x);xs.append(x);ys.append([float(row[n]) for n in ('performance','size')]);source.append(line)
                raw.append([row[n] for n in ('performance','size')])
        require(len(xs)==d['rows'],'Independent candidate reconstruction');tables[d['id']]=(xs,ys,raw,source)
    expected=[];records=[];pairs=[];decimal_checks=0
    for case in m['cases']:
        dataset=case['dataset'];seed=case['seed'];key=f'{dataset}_{seed}'
        xs,ys,raw,source=tables[dataset];original=read(case['prefix_path'])['state']
        saved=read(OUT/'prefixes'/f'{key}.json');prefix=saved['prefix'];ph=digest(prefix)
        require(ph==saved['prefix_hash'] and prefix['ids']==original['ids'] and prefix['order']==original['order'],'Saved prefix identity')
        require(prefix['labels']==[ys[i] for i in original['ids']],'Source prefix vectors')
        anchor=min(prefix['ids'],key=lambda i:ys[i][0]);cap=ys[anchor][1]
        require(prefix['anchor_row']==anchor and prefix['size_cap']==cap,'Acquired-only fixed cap')
        for i in prefix['ids']:expected.append((dataset,seed,'prefix',i,source[i],*raw[i]))
        arms={}
        for mode in MODES:
            arm=read(OUT/'arms'/f'{key}_{mode}.json');ids=list(prefix['ids']);labels=[list(v) for v in prefix['labels']]
            require(arm['status']=='completed' and arm['prefix_hash']==ph and arm['size_cap']==cap,'Completed shared-prefix branch')
            require(arm['logical_evaluations']==20 and arm['actual_new_accesses']==10,'Inclusive budget')
            order=prefix['order'] if mode=='joint_full' else [i for i in prefix['order'] if i in set(case['pool'])|set(ids)]
            for j,event in enumerate(arm['events']):
                selected=manual_choice(xs,order,ids,labels,cap,'joint_3nn') if mode.startswith('joint_') else case['selected'][mode][j]
                require(event['row_id']==selected and selected not in ids,'Independent acquired-only decision replay')
                ids.append(selected);labels.append(ys[selected]);expected.append((dataset,seed,mode,selected,source[selected],*raw[selected]))
            require(len(ids)==len(set(ids))==20 and arm['ids']==ids and arm['labels']==labels,'Twenty source-bound acquisitions')
            feasible=min((i for i in ids if ys[i][1]<=cap),key=lambda i:ys[i][0]);unconstrained=min(ids,key=lambda i:ys[i][0])
            metrics={'best_row':feasible,'best_runtime':ys[feasible][0],'best_size':ys[feasible][1],
                'runtime_only_best_row':unconstrained,'runtime_only_best_runtime':ys[unconstrained][0],'runtime_only_best_size':ys[unconstrained][1],
                'runtime_only_best_violates_cap':ys[unconstrained][1]>cap,'infeasible_new_acquisitions':sum(ys[i][1]>cap for i in ids[10:])}
            require(all(arm[k]==v for k,v in metrics.items()),'Independent terminal feasibility/runtime check')
            require(arm['cached_request']==case['provenance'].get(mode),'Historical request binding')
            if mode=='joint_full':
                old=read(f'results/v12_controls/joint_3nn/{key}.json')
                require(old['ids']==ids and old['labels']==labels,'Unchanged full-domain V12 control')
            records.append({'dataset':dataset,'seed':seed,'arm':mode,'size_cap':cap,**metrics});arms[mode]=arm
        for mode in MODES[4:]:
            for base in BASES:
                l=arms[mode];b=arms[base];gain=(b['best_runtime']-l['best_runtime'])/b['best_runtime']
                unconstrained=(b['runtime_only_best_runtime']-l['runtime_only_best_runtime'])/b['runtime_only_best_runtime']
                db=Decimal(raw[b['best_row']][0]);dl=Decimal(raw[l['best_row']][0]);dg=(db-dl)/db
                rb=Decimal(raw[b['runtime_only_best_row']][0]);rl=Decimal(raw[l['runtime_only_best_row']][0]);dr=(rb-rl)/rb
                require(math.isclose(gain,float(dg),abs_tol=1e-14) and math.isclose(unconstrained,float(dr),abs_tol=1e-14),'Independent Decimal source score')
                decimal_checks+=2
                pairs.append({'dataset':dataset,'seed':seed,'condition':mode.removeprefix('cached_llm_'),'baseline':base,
                    'classical_feasible_runtime':b['best_runtime'],'llm_feasible_runtime':l['best_runtime'],
                    'constrained_relative_gain':gain,'unconstrained_relative_gain':unconstrained,
                    'decimal_constrained_gain':str(dg),'decimal_unconstrained_gain':str(dr)})
    journal=lines(OUT/'acquisitions.jsonl')
    actual=[(r['dataset'],r['seed'],r['arm'],r['row_id'],r['source_line'],r['raw_runtime'],r['raw_size']) for r in journal]
    require(actual==expected and len(actual)==800 and all(r['vector_charge']==1 for r in journal),'Complete ordered 800-charge journal')
    require(read(OUT/'progress.json')['complete'] and len(records)==70 and len(pairs)==120,'Full intended denominator')
    summaries=[]
    for mode in MODES[4:]:
        condition=mode.removeprefix('cached_llm_')
        for base in BASES:
            rows=[r for r in pairs if r['condition']==condition and r['baseline']==base];groups=[]
            for dataset in ('brotli','lrzip'):
                group=[r for r in rows if r['dataset']==dataset]
                groups.append({'dataset':dataset,'cases':len(group),'mean_constrained_gain':mean(r['constrained_relative_gain'] for r in group),
                    'mean_unconstrained_gain':mean(r['unconstrained_relative_gain'] for r in group)})
            summaries.append({'condition':condition,'baseline':base,'cases':len(rows),'groups':groups,
                'equal_family_constrained_gain':mean(g['mean_constrained_gain'] for g in groups),
                'equal_family_unconstrained_gain':mean(g['mean_unconstrained_gain'] for g in groups),
                'wins':sum(r['constrained_relative_gain']>0 for r in rows),'ties':sum(r['constrained_relative_gain']==0 for r in rows),
                'harms':sum(r['constrained_relative_gain']<0 for r in rows)})
    reliability=[{'arm':mode,'cases':10,'runtime_only_best_violations':sum(r['runtime_only_best_violates_cap'] for r in records if r['arm']==mode),
        'infeasible_continuation_vectors':sum(r['infeasible_new_acquisitions'] for r in records if r['arm']==mode)} for mode in MODES]
    return {'scope':m['scope'],'records':records,'pairs':pairs,'summaries':summaries,'reliability':reliability,
        'verification':{'independent_source_and_decision_replay':True,'decimal_gain_checks':decimal_checks,'joint_vectors':800,
            'intended_arms':70,'completed_arms':70,'prefixes':10,'pairwise_comparisons':120,'new_model_calls':0,'new_physical_trials':0},
        'caveat':'Two exposed families; runtime-only LLM prompts; acquired-prefix research cap, not an application-approved quality requirement. No learned-router or held-out claim.'}

def render(r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),sharey=True)
    labels=['Joint 3NN\nshortlist','Joint 3NN\nfull domain','Static\nrank','Runtime\n3NN']
    for ax,dataset in zip(axes,('brotli','lrzip')):
        for offset,condition,color in [(-.24,'assigned_ids','#176b93'),(0,'reverse_display','#b56143'),(.24,'reassigned_ids','#668054')]:
            values=[next(g['mean_constrained_gain'] for g in s['groups'] if g['dataset']==dataset)*100 for base in BASES for s in r['summaries'] if s['condition']==condition and s['baseline']==base]
            ax.bar([i+offset for i in range(4)],values,width=.24,label=condition.replace('_',' '),color=color)
        ax.axhline(0,color='#444',linewidth=.8);ax.set_xticks(range(4),labels);ax.set_title(dataset+' (five seeds)');ax.grid(axis='y',alpha=.2)
    axes[0].set_ylabel('Mean feasible-runtime gain over comparator (%)\nPositive favors cached LLM selections')
    axes[1].legend(fontsize=8)
    fig.suptitle('V34: recorded LLM selections evaluated under an output-size cap')
    fig.text(.5,.02,'Two exposed families; LLM prompts were runtime-only. No new inference or physical execution.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.055,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'constrained_gains.{ext}',dpi=180)
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    if a.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved analysis differs');print('Verified 800 vectors,70 arms,120 comparisons,240 Decimal gains.');return
    require(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    before=read('artifacts/resource_ledger_v2.json');cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>60,'Analysis reserve');r=calculate();write(OUT/'summary.json',r)
        for name,rows in [('arms',r['records']),('comparisons',r['pairs']),('reliability',r['reliability'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v34/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'active_since':after['active_since']})
    write('artifacts/study_v34/verification.json',r['verification'])
    print(__import__('json').dumps({'summaries':r['summaries'],'reliability':r['reliability']},indent=2))

if __name__=='__main__':main()
