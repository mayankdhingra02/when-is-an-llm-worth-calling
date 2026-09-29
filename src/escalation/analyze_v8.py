"""Retrospective development-only scoring, isolated from selection."""
import csv,os
from pathlib import Path
import numpy as np
from .io import read,write,lines
from .study_v8 import OUT,manifest,verify,run_config,prefix
from .study_v6 import retrospective_labels
from .finite_v6 import load_candidates
from .evaluator import evaluate
from .resources import Resources


def analyze():
    verify();m=manifest();progress=read(OUT/'progress.json');complete=progress['complete'];records=[]
    columns=['classical','original_llm','excluded_llm','uniform_selection','static_rank']+(['llm_selection'] if complete else [])
    for d in m['datasets']:
        c=load_candidates(d);labels=retrospective_labels(d,c)
        for seed in m['seeds']:
            k=d['id']+'_'+str(seed);p=prefix(d,seed)
            states={'classical':read(f'results/v6/classical/{k}.json')['arms']['centroid_nominal']['state'],
              'original_llm':read(f'results/v6/paired/{k}.json')['state'], 'excluded_llm':read(f'results/v7/llm/{k}.json')['state']}
            for arm in ['uniform_selection','static_rank']:
                path=OUT/arm/(k+'.json')
                if path.exists():states[arm]=read(path)['state']
            if complete:states['llm_selection']=read(OUT/'llm'/(k+'.json'))['state']
            if any(col not in states for col in columns):continue
            loss={name:evaluate(labels,c.directions,s['ids'])['loss'] for name,s in states.items()}
            pool=next(case['pool'] for case in m['cases'] if case['dataset']==d['id'] and case['seed']==seed)
            # Retrospective best attainable loss in frozen shortlist, not an optimizer acquisition or policy.
            upper=evaluate(labels,c.directions,p['state']['ids']+pool['ranked'])['loss']
            records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'split':'development',**loss,'shortlist_hindsight_loss':upper})
    groups=[]
    for g in sorted({r['system_group'] for r in records}):
        rs=[r for r in records if r['system_group']==g]
        groups.append({'system_group':g,'n':len(rs),**{col:float(np.mean([r[col] for r in rs])) for col in columns+['shortlist_hindsight_loss']}})
    req=lines(OUT/'requests.jsonl');reliability=[]
    for arm in ['uniform_selection','static_rank','llm']:
        runs=[read(p) for p in (OUT/arm).glob('*.json')]
        reliability.append({'arm':arm,'completed_or_fallback':len(runs),'intended':15,'fallback_runs':sum(r['status']=='fallback' for r in runs),
           'new_acquisitions':sum(r['actual_new_accesses'] for r in runs)})
    summary={'scope':'post-v7 exploratory development-only candidate selection; no generalization or router claim',
      'complete':complete,'records':records,'systems':groups,'reliability':reliability,'intended':progress['intended'],
      'collection':{'new_objective_accesses':len(lines(OUT/'acquisitions.jsonl')),'model_attempts':len(lines(OUT/'request_starts.jsonl')),
         'input_tokens':sum(r['input_tokens'] for r in req) if all(r['input_tokens'] is not None for r in req) else None,
         'output_tokens':sum(r['output_tokens'] for r in req) if all(r['output_tokens'] is not None for r in req) else None,
         'request_wall_seconds':sum(r['wall_seconds'] for r in req),'external_spend_usd':0},
      'interpretation':'Direct selection guarantees table membership; this alone is not model benefit. Shortlist hindsight uses hidden targets retrospectively and is nondeployable.',
      'deployment_scenario':{'cases':15,'logical_labels':300,'model_requests':15,'status':'hypothetical LLM-only deployment, not actual research cost'}}
    if complete:
        summary['paired_gain_summary']={baseline:{'mean_gain':float(np.mean([r[baseline]-r['llm_selection'] for r in records])),
          'material_help':sum(r[baseline]-r['llm_selection']>.02 for r in records),'material_harm':sum(r[baseline]-r['llm_selection']<-.02 for r in records)} for baseline in columns if baseline!='llm_selection'}
    write(OUT/'summary.json',summary)
    if records:
        with (OUT/'outcomes.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    os.environ['MPLCONFIGDIR']=str(Path('.cache/matplotlib').resolve());os.environ['XDG_CACHE_HOME']=str(Path('.cache').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,4))
    for ax,g in zip(axes,groups):
        ax.bar(range(len(columns)),[g[col] for col in columns],color=['#64748b','#d1a344','#cb7948','#7aaf96','#456c85','#695aa6'][:len(columns)])
        ax.axhline(g['shortlist_hindsight_loss'],color='black',linestyle='--',linewidth=1,label='shortlist hindsight')
        ax.set_xticks(range(len(columns)),[col.replace('_','\n') for col in columns],fontsize=7)
        ax.set_title(g['system_group'].replace('_family',''));ax.set_ylabel('Mean loss (lower better)');ax.legend(fontsize=7)
    fig.suptitle('V8 development-only candidate selection' if complete else 'V8 controls complete; LLM selection untested')
    fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(OUT/('comparison.'+ext),dpi=180)
    plt.close(fig)
    print(__import__('json').dumps({'complete':complete,'systems':groups,'collection':summary['collection']},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:r.check();analyze();r.check()
