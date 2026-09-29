"""Charged evaluation/figure wrapper around independent stdlib reconstruction."""
import csv,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from verify_arithmetic_v36 import calculate
from escalation.io import read,write
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config,require
OUT=Path('results/v36_arithmetic')

def render(r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cases=[(c['dataset'],c['seed']) for c in read('data/arithmetic_v36.json')['cases']]
    rows=[[next(a for a in r['records'] if (a['dataset'],a['seed'],a['arm'])==(d,s,m)) for m in ('joint_shortlist','joint_full')] for d,s in cases]
    positions=[[c['changed_positions'] for c in row] for row in rows];gains=[[c['exact_gain_over_old']*100 for c in row] for row in rows]
    fig,axes=plt.subplots(1,2,figsize=(9,6.6));lim=max(.1,max(abs(v) for row in gains for v in row))
    for ax,values,title,cmap,low,high,fmt in [(axes[0],positions,'Changed continuation positions (of 10)','Blues',0,10,'.0f'),
            (axes[1],gains,'Exact-arithmetic feasible-runtime gain (%)','RdBu',-lim,lim,'.3f')]:
        im=ax.imshow(values,cmap=cmap,vmin=low,vmax=high,aspect='auto');ax.set_xticks([0,1],['Shortlist','Full domain']);ax.set_yticks(range(10),[f'{d} / {s}' for d,s in cases]);ax.set_title(title,fontsize=10)
        for i,row in enumerate(values):
            for j,value in enumerate(row):ax.text(j,i,format(value,fmt),ha='center',va='center',fontsize=9,color='black' if abs(value)<(high-low)*.35 else 'white')
        fig.colorbar(im,ax=ax,shrink=.8)
    fig.suptitle('V36: trajectory and terminal sensitivity to exact arithmetic')
    fig.text(.5,.02,'Same ten prefixes and budgets; two exposed systems. Positive runtime gain favors exact arithmetic.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.05,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'arithmetic_sensitivity.{ext}',dpi=180)
    plt.close(fig)

def main():
    require(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'));before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>60,'Analysis reserve');r=calculate();write(OUT/'summary.json',r)
        for name,rows in [('arms',r['records']),('llm_comparisons',r['llm_comparisons']),('families',r['groups'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v36/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'active_since':after['active_since']})
    print(json.dumps({k:v for k,v in r.items() if k not in ('records','llm_comparisons')},indent=2))
if __name__=='__main__':main()
