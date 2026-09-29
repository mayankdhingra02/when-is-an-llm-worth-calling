"""Postcollection descriptive diagnostics; no new labels or policy selection."""
import os,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib');os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.io import read,write,lines
from escalation.study_v7 import manifest,run_config
from escalation.finite_v6 import load_candidates,parse_symbols
from escalation.resources import Resources

def main():
    summary=read('results/v7/summary.json')
    if not summary['complete']:raise ValueError('diagnosis requires all intended cases')
    m=manifest();old_requests={(r.get('dataset'),r.get('seed')):r for r in lines('results/v6/requests.jsonl') if r.get('split')=='development'}
    new_requests={(r['dataset'],r['seed']):r for r in lines('results/v7/requests.jsonl')}
    rows=[]
    for d in m['datasets']:
        c=load_candidates(d);valid=set(c.x)
        for seed in m['seeds']:
            prefix=read(f'results/v6/prefixes/{d["id"]}_{seed}.json');seen={c.x[i] for i in prefix['state']['ids']}
            row={'dataset':d['id'],'seed':seed,'split':'development'}
            for arm,request in [('original',old_requests[(d['id'],seed)]),('excluded',new_requests[(d['id'],seed)])]:
                if request['status']!='response':
                    row[arm]={'status':request['status'],'proposal_metrics':None};continue
                proposals=[tuple(x) for x in parse_symbols(request['raw_output'],c)]
                row[arm]={'status':'response','count':len(proposals),'prefix_copies':sum(x in seen for x in proposals),
                  'within_batch_repetitions':len(proposals)-len(set(proposals)),
                  'valid_recorded_configurations':sum(x in valid for x in proposals),
                  'valid_unobserved_configurations':sum(x in valid and x not in seen for x in proposals)}
            rows.append(row)
    totals={}
    for arm in ['original','excluded']:
        successful=[r[arm] for r in rows if r[arm]['status']=='response']
        totals[arm]={'responded_cases':len(successful),**{key:sum(r[key] for r in successful) for key in ['count','prefix_copies','within_batch_repetitions','valid_recorded_configurations','valid_unobserved_configurations']}}
    write('results/v7/proposal_diagnostics.json',{'scope':'post-hoc descriptive, development only, matched original cases; no treatment changes','cases':rows,'totals':totals})
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
    groups=[d['system_group'] for d in m['datasets']]
    for ax,base in zip(axes,['original_llm','classical','uniform_excluded']):
        for i,group in enumerate(groups):
            rs=[r for r in summary['records'] if r['system_group']==group]
            ax.scatter(i+np.linspace(-.15,.15,len(rs)),[r[base]-r['llm_excluded'] for r in rs],s=28)
        ax.axhline(0,color='black',linewidth=.7)
        for y in [-.02,.02]:ax.axhline(y,color='gray',linestyle='--',linewidth=.7)
        ax.set_xticks(range(len(groups)),groups,rotation=20);ax.set_title('Versus '+base.replace('_',' '),fontsize=10)
    axes[0].set_ylabel('Baseline loss − new LLM loss\nPositive favors prefix exclusion')
    fig.suptitle('V7: all 15 paired development cases; dashed lines = ±.02 margin',fontsize=11);fig.tight_layout()
    for ext in ['png','svg']:fig.savefig('results/v7/paired_gains.'+ext,dpi=180)
    plt.close(fig);print(__import__('json').dumps(totals,indent=2))
if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:r.check();main();r.check()
