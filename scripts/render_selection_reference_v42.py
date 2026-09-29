"""Render the predeclared post-hoc shortlist ceiling and exact random reference."""
import csv,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'));os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
from escalation.io import read,write
from escalation.resources import Resources
from escalation.transfer_v41 import current_config

def main():
    s=read('results/v42_selection_reference/summary.json');v=read('results/v41_model_analysis/summary.json')
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        batch=next(r for r in s['ceiling_summary'] if r['reference']=='batch_3nn')
        ceiling=next(r for r in s['ceiling_summary'] if r['reference']=='full_sequential_3nn')
        counts=[s['model_summary'][0]['model_attains_shortlist_ceiling'],s['model_summary'][1]['model_attains_shortlist_ceiling'],batch['equal']]
        means=[100*next(r['family_mean_gain'] for r in v['contrasts'] if r['model_size']==size and r['reference']=='full_sequential_3nn') for size in ('0.5','1.5')]+[100*ceiling['mean_best_possible_gain']]
        fig,axes=plt.subplots(1,2,figsize=(11,4.8))
        bars=axes[0].bar(['Qwen0.5B','Qwen1.5B','Batch3NN'],counts,color=['#2471a3','#a04000','#527a3d'])
        axes[0].bar_label(bars,labels=[f'{n}/30' for n in counts],padding=4);axes[0].set_ylim(0,34)
        axes[0].set_ylabel('Cases attaining the fixed-shortlist ceiling');axes[0].set_title('Little room beyond the cheap batch control')
        bars=axes[1].bar(['Qwen0.5B','Qwen1.5B','Perfect shortlist\nselector*'],means,color=['#2471a3','#a04000','#777777'])
        axes[1].bar_label(bars,labels=[f'{m:+.3f}%' for m in means],padding=4)
        axes[1].axhline(0,color='#666666',linewidth=1);axes[1].set_ylim(-5.8,.4)
        axes[1].set_ylabel('Equal-family mean gain vs full-domain3NN (%)');axes[1].set_title('Always escalating remains below the strong control')
        fig.suptitle('V42 post-hoc diagnostic: six families × five seeds',fontsize=13)
        fig.text(.5,.01,'*Nondeployable, outcome-informed ceiling. Seven cases still permit selective gains.',ha='center',fontsize=10)
        fig.tight_layout(rect=(0,.055,1,1));out=Path('results/v42_selection_reference')
        fig.savefig(out/'shortlist_ceiling.png',dpi=170);fig.savefig(out/'shortlist_ceiling.svg');plt.close(fig)
        rows=[]
        for r in s['model_comparisons']:rows.append({k:v for k,v in r.items() if k!='exact'})
        with (out/'model_vs_exact_random.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
        with (out/'ceiling_comparisons.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=s['ceiling_comparisons'][0].keys());w.writeheader();w.writerows(s['ceiling_comparisons'])
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v42/render_accounting.json',{'seconds':after['experiment_seconds']-before['experiment_seconds'],'new_model_calls':0,'new_acquisitions':0})
if __name__=='__main__':main()
