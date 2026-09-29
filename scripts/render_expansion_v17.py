"""Render saved V17 outcomes only; no new physical or model observations."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.resources import Resources

def main():
    before=json.loads((ROOT/'artifacts/resource_ledger_v2.json').read_text())
    if before.get('active_since') or 1800-before['experiment_seconds']<5:raise RuntimeError('Insufficient analysis reserve')
    config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    with Resources(config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        out=ROOT/'results/v17_classical'
        rows=json.loads((out/'summary.json').read_text())['cases']
        fig,axes=plt.subplots(1,2,figsize=(9,4))
        for index,family in enumerate(['zstd','lz4','zlib']):
            group=[r for r in rows if r['family']==family]
            for axis,key in zip(axes,['cheap_gain_over_random','hindsight_headroom_over_cheap']):
                axis.scatter([index+(i-2)*.06 for i in range(5)],[100*r[key] for r in group],s=32)
        for axis in axes:
            axis.set_xticks(range(3),['Zstandard\n96 settings','LZ4\n96 settings','zlib\n90 settings'])
            axis.grid(axis='y',alpha=.2)
        axes[0].axhline(0,color='gray',linewidth=1)
        axes[0].set_ylabel('Relative runtime gain (%)');axes[0].set_title('Cheap continuation versus random')
        axes[1].axhline(10,color='darkorange',linestyle='--',linewidth=1,label='10% diagnostic')
        axes[1].set_ylabel('Potential runtime reduction (%)');axes[1].set_title('Full-table hindsight headroom')
        axes[1].legend(fontsize=8)
        fig.suptitle('Expanded development grid: 20 evaluations, checkpoint at 10')
        fig.text(.5,.015,'Five seeds per family; one workload; hindsight is not deployable; no new LLM inference.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.06,1,.93]);fig.savefig(out/'comparison.png',dpi=160);fig.savefig(out/'comparison.svg');plt.close(fig)
        resource.checkpoint()
    print('Saved comparison.png and comparison.svg from recorded outcomes.')

if __name__=='__main__':main()
