"""Presentation-only spacing correction; original figure and analyzer retained."""
import os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config,require

def main():
    out=Path('results/v28_consensus');require(not (out/'comparison_readable.png').exists(),'Preserve rendered figure')
    before=read('artifacts/resource_ledger_v2.json')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        result=read(out/'summary.json');fig,axes=plt.subplots(1,3,figsize=(11,4))
        for ax,family in zip(axes,result['families']):
            fields=['static_rank_loss','single_assigned_loss','single_presentation_mean_loss','ensemble_loss']
            ax.bar(range(4),[family[f] for f in fields],color=['#7b8b96','#be9871','#b55b3d','#176b93'])
            ax.set_xticks(range(4),['Static\nrank','Single\nassigned','Single\nmean','3-call\nvote'],fontsize=9)
            ax.set_title(family['system_group']);ax.set_ylabel('Normalized loss (lower is better)')
        fig.suptitle('V28: voting over three saved real LLM presentations')
        fig.text(.5,.015,'20 objective evaluations per arm. Voting costs 3 calls and uses classical rank for ties. Separate panel scales.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.05,1,.95])
        for ext in ('png','svg'):fig.savefig(out/('comparison_readable.'+ext),dpi=180)
        plt.close(fig);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v28/presentation_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'new_model_calls':0,'new_objective_acquisitions':0,'active_since':after['active_since']})

if __name__=='__main__':main()
