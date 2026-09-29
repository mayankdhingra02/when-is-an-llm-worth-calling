"""Regenerate the V15 presentation figure from saved observations, no new trials."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
from escalation.resources import Resources
ledger=json.loads((ROOT/'artifacts/resource_ledger_v2.json').read_text())
if ledger.get('active_since') is not None or 1800-ledger['experiment_seconds']<5:raise RuntimeError('Insufficient inactive runtime allowance')
config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
with Resources(config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
    saved=json.loads((ROOT/'results/v15_measurements/summary.json').read_text())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axis=plt.subplots(figsize=(7,4))
    for i,family in enumerate(['zstd','lz4','zlib']):
        rows=[r for r in saved['settings'] if r['family']==family and r['complete_three_trials']]
        x=[i+(j-(len(rows)-1)/2)*.012 for j in range(len(rows))]
        axis.scatter(x,[100*r['compression_cv'] for r in rows],s=20,alpha=.75,label=family)
    axis.axhline(10,color='darkorange',linestyle='--',linewidth=1,label='10% diagnostic flag')
    axis.set_xticks(range(3),['Zstandard','LZ4','zlib']);axis.set_ylabel('Within-setting timing CV (%)')
    axis.set_title('Live measurement feasibility: three trials per setting')
    axis.grid(axis='y',alpha=.2);axis.legend(loc='best',fontsize=8)
    fig.text(.5,.015,'One CPython source archive; development only. Timing stacks differ; no LLM inference.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.045,1,1])
    for extension in ('png','svg'):fig.savefig(ROOT/f'results/v15_measurements/timing_variability.{extension}',dpi=160 if extension=='png' else None)
    plt.close(fig);resource.checkpoint()
print('Regenerated V15 figure from saved numerical evidence; no new physical trials or inference.')
