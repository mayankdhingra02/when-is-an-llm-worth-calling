"""Presentation-only regeneration from the frozen completed numerical analysis."""
import sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read
from escalation.study_v8 import run_config
from escalation.resources import Resources

def render():
    s=read('results/v9_analysis/summary.json')
    os.environ['MPLCONFIGDIR']=str(Path('.cache/matplotlib').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,4.5))
    for ax,g in zip(axes,s['groups']):
        fields=['classical_loss','observed_static_rank_loss','uniform_expected_loss','observed_llm_loss']
        names=['Adaptive\nclassical','Static\nshortlist','Uniform\nexpectation','LLM\nobserved']
        ax.bar(names,[g[k] for k in fields],color=['#657384','#357884','#bd9850','#8171a5'],width=.65)
        ax.set_title(g['system_group'].replace('_family',''));ax.set_ylabel('Mean normalized loss (lower better)');ax.tick_params(axis='x',labelsize=9)
    fig.suptitle('All 15 observed LLM selections equal the first displayed half',fontsize=13)
    fig.text(.5,.015,'Uniform expectation: exact retrospective calculation, not a new measured arm. Development data only.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,1])
    for ext in ['png','svg']:fig.savefig(Path('results/v9_analysis')/('exact_reference.'+ext),dpi=180)
    plt.close(fig)
if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:r.check();render();r.check()
