"""Development-only descriptive comparison; no controller fit or test access."""
import os,csv
from pathlib import Path
import numpy as np
from .io import read,write,lines
from .study_v7 import OUT,manifest,verify,run_config
from .study_v6 import retrospective_labels
from .finite_v6 import load_candidates
from .evaluator import evaluate
from .resources import Resources

def analyze():
    verify();m=manifest();progress=read(OUT/'progress.json');complete=progress['complete'];records=[]
    for d in m['datasets']:
        c=load_candidates(d);labels=retrospective_labels(d,c)
        for seed in m['seeds']:
            k=d['id']+'_'+str(seed);control=OUT/'uniform_excluded'/f'{k}.json'
            if not control.exists():continue
            a=read(f'results/v6/classical/{k}.json');b=read(f'results/v6/paired/{k}.json');u=read(control)
            states={'classical':a['arms']['centroid_nominal']['state'],'original_llm':b['state'],
              'uniform_original':a['arms']['uniform_projection']['state'],'uniform_excluded':u['state']}
            if complete:states['llm_excluded']=read(OUT/'llm'/f'{k}.json')['state']
            loss={name:evaluate(labels,c.directions,s['ids'])['loss'] for name,s in states.items()}
            records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'split':'development',**loss})
    columns=['classical','original_llm','uniform_original','uniform_excluded']+(['llm_excluded'] if complete else [])
    groups=[]
    for g in sorted({r['system_group'] for r in records}):
        rs=[r for r in records if r['system_group']==g]
        groups.append({'system_group':g,'n':len(rs),**{col:float(np.mean([r[col] for r in rs])) for col in columns}})
    req=lines(OUT/'requests.jsonl');reliability=[]
    for arm in ['uniform_excluded','llm']:
        runs=[read(p) for p in (OUT/arm).glob('*.json')];events=[e for r in runs for e in r['events']]
        reliability.append({'arm':arm,'completed_or_fallback':len(runs),'intended':15,'events':len(events),
          **{name:sum(e.get(name,False) for e in events) for name in ['projected','duplicate','collision','fallback']}})
    summary={'scope':'post-v6 exploratory development-only mechanism ablation; no generalization claims','complete':complete,'records':records,'systems':groups,
      'reliability':reliability,'intended':progress['intended'],'collection':{'new_objective_accesses':len(lines(OUT/'acquisitions.jsonl')),
      'model_attempts':len(lines(OUT/'request_starts.jsonl')),'input_tokens':sum(r['input_tokens'] for r in req) if all(r['input_tokens'] is not None for r in req) else None,
      'output_tokens':sum(r['output_tokens'] for r in req) if all(r['output_tokens'] is not None for r in req) else None,
      'request_wall_seconds':sum(r['wall_seconds'] for r in req),'external_spend_usd':0},
      'historical_comparisons':'Original prefixes/classical/uniform/LLM are v6 development records; do not count prior costs as free or reacquired',
      'interpretation':'Zero original-prefix copies is enforced, not proof of model benefit. Compare quality against both original LLM and uniform exclusion control.'}
    if complete:
        summary['paired_gain_summary']={baseline:{'mean_gain':float(np.mean([r[baseline]-r['llm_excluded'] for r in records])),
          'material_help':sum(r[baseline]-r['llm_excluded']>.02 for r in records),'material_harm':sum(r[baseline]-r['llm_excluded']<-.02 for r in records)}
          for baseline in ['original_llm','classical','uniform_excluded']}
    write(OUT/'summary.json',summary)
    if records:
        with (OUT/'outcomes.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    os.environ['MPLCONFIGDIR']=str(Path('.cache/matplotlib').resolve());os.environ['XDG_CACHE_HOME']=str(Path('.cache').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.6));x=np.arange(len(groups));width=.8/len(columns)
    for j,col in enumerate(columns):ax.bar(x-.4+width/2+j*width,[g[col] for g in groups],width,label=col.replace('_',' '))
    ax.set_xticks(x,[g['system_group'] for g in groups]);ax.set_ylabel('Mean normalized loss (lower better)');ax.legend(fontsize=8)
    ax.set_title('V7 development-only ablation' if complete else 'V7 control stage only: new LLM arm not evaluated',fontsize=11);fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(OUT/('comparison.'+ext),dpi=180)
    plt.close(fig);print(__import__('json').dumps({'complete':complete,'systems':groups,'collection':summary['collection']},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:r.check();analyze();r.check()
