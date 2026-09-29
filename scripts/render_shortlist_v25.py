"""Post-collection presentation correction; measured results remain unchanged."""
import os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
from escalation.resources import Resources

def main():
    out=Path('results/v25_shortlist');require(not (out/'comparison_readable.png').exists(),'Preserve completed presentation')
    before=read('artifacts/resource_ledger_v2.json')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        summary=read(out/'summary.json');fig,axes=plt.subplots(1,3,figsize=(11,4))
        for ax,g in zip(axes,summary['families']):
            fields=['full_classical_loss','static_rank_loss','restricted_loss','llm_mean_loss']
            ax.bar(range(4),[g[f] for f in fields],color=['#9aa8b2','#7b8b96','#176B93','#b55b3d'])
            ax.set_xticks(range(4),['Full\nclassical','Static\nrank','Adaptive\nshortlist','LLM\nmean'],fontsize=8)
            ax.set_title(g['system_group']);ax.set_ylabel('Mean normalized loss (lower is better)')
        fig.suptitle('V25: equal objective budgets and the same candidate shortlist')
        fig.text(.5,.015,'Three development families × five seeds. LLM: mean of three presentations. Panels use separate scales.\nClassical sequential feedback differs from LLM batch selection; no generalization claim.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.075,1,.96])
        for ext in ['png','svg']:fig.savefig(out/('comparison_readable.'+ext),dpi=180)
        plt.close(fig);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v25/presentation_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'new_model_calls':0,'new_objective_acquisitions':0})

if __name__=='__main__':main()
