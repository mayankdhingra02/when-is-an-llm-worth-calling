"""Display correction only: bound the work axis to nonnegative scenario values."""
import hashlib,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out=Path('results/v33_amortization');receipt=Path('artifacts/study_v33/render_correction.json')
    if receipt.exists():raise RuntimeError('Preserve completed rendering receipt')
    prior={ext:hashlib.sha256((out/f'recovery.{ext}').read_bytes()).hexdigest() for ext in ('png','svg')}
    for ext in ('png','svg'):(out/f'recovery_initial.{ext}').write_bytes((out/f'recovery.{ext}').read_bytes())
    before=read('artifacts/resource_ledger_v2.json');cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check();r=read(out/'summary.json');fig,axes=plt.subplots(1,2,figsize=(10,4.3))
        for ax,base,title in [(axes[0],'full_classical','Original classical comparator'),(axes[1],'sequential_3nn','Stronger sequential 3NN comparator')]:
            rows=[c for c in r['curves'] if c['baseline']==base and c['scenario']=='assigned_ids']
            for key,label,color in [('always_call_mean_net_seconds','Always call','#b56143'),('hindsight_mean_net_seconds','Hindsight only (nondeployable)','#176b93')]:
                ax.plot([c['baseline_work_seconds_per_case'] for c in rows],[c[key] for c in rows],marker='o',markersize=3,label=label,color=color)
            ax.axhline(0,color='#666',linestyle='--',label='Never call');ax.set_xscale('symlog',linthresh=1);ax.set_xlim(0,100000);ax.set_yscale('symlog',linthresh=1)
            ax.set_title(title,fontsize=10);ax.set_xlabel('Assumed future baseline work per case (seconds)');ax.set_ylabel('Mean net seconds after request cost');ax.legend(fontsize=7);ax.grid(alpha=.15)
        fig.suptitle('V33: hypothetical reuse scenario with observed model-request cost')
        fig.text(.5,.015,'Fixed assigned-ID calls; three exposed families. Signed-log axes. No measured deployment or learned policy.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.065,1,.95])
        for ext in ('png','svg'):fig.savefig(out/f'recovery.{ext}',dpi=180)
        plt.close(fig);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write(receipt,{'reason':'Default signed-log autoscale displayed negative work values outside scenario domain; set x limits to0..100000',
        'prior_figure_sha256':prior,'initial_figures_preserved':True,'numerical_outputs_unchanged':True,
        'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],
        'new_model_calls':0,'new_objective_acquisitions':0})

if __name__=='__main__':main()
