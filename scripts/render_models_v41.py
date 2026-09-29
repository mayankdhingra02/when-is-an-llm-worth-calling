"""Render all predeclared model contrasts and policy views from real summaries."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
from escalation.io import read,write
from escalation.resources import Resources
from escalation.transfer_v41 import current_config

def main():
    out=Path('results/v41_model_analysis');s=read(out/'summary.json')
    if s['completed_cases']!=60 or s['intended_cases']!=60:raise ValueError('Complete denominator required')
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        modes=[r['reference'] for r in s['contrasts'] if r['model_size']=='0.5']
        fig,ax=plt.subplots(figsize=(10,5.5))
        for size,offset,color in [('0.5',-.13,'#2471a3'),('1.5',.13,'#a04000')]:
            data=[next(r for r in s['contrasts'] if r['model_size']==size and r['reference']==mode) for mode in modes]
            y=np.arange(len(modes))+offset;means=np.asarray([r['family_mean_gain'] for r in data])*100
            lo=np.asarray([r['bootstrap95'][0] for r in data])*100;hi=np.asarray([r['bootstrap95'][1] for r in data])*100
            ax.hlines(y,lo,hi,color=color,linewidth=2);ax.scatter(means,y,color=color,label=f'Qwen2.5 {size}B',zorder=3)
        ax.axvline(0,color='#666666',linewidth=1);ax.set_yticks(range(len(modes)),modes);ax.invert_yaxis()
        ax.set_xlabel('Equal-family relative gain over comparator (%)');ax.legend(loc='lower left')
        ax.set_title('Frozen six-family transfer: all classical comparisons\n30 paired cases/model; family bootstrap95% intervals; exploratory')
        fig.tight_layout();fig.savefig(out/'model_contrasts.png',dpi=170);fig.savefig(out/'model_contrasts.svg');plt.close(fig)
        fig,axes=plt.subplots(1,2,figsize=(11,4.8),sharey=True)
        for ax,reference in zip(axes,['batch_3nn','full_sequential_3nn']):
            rows=[r for r in s['contrasts'] if r['reference']==reference];families=sorted(rows[0]['family_means'])
            for size,offset,color in [('0.5',-.17,'#2471a3'),('1.5',.17,'#a04000')]:
                row=next(r for r in rows if r['model_size']==size)
                ax.bar(np.arange(6)+offset,[row['family_means'][f]*100 for f in families],.34,color=color,label=size+'B')
            ax.axhline(0,color='#666666',linewidth=1);ax.set_xticks(range(6),families,rotation=35,ha='right');ax.set_title('vs '+reference);ax.legend()
        axes[0].set_ylabel('Mean paired relative gain (%)');fig.suptitle('Each family remains visible; five seeds per family')
        fig.tight_layout();fig.savefig(out/'family_gains.png',dpi=170);fig.savefig(out/'family_gains.svg');plt.close(fig)
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/render_accounting.json',{'seconds':after['experiment_seconds']-before['experiment_seconds'],'new_model_calls':0,'new_acquisitions':0})
    print('Saved two PNG/SVG scientific figures.')
if __name__=='__main__':main()
