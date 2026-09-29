"""Reproduce exposed-system diagnostic tables/figure from measured records only."""
import csv,json,os,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines
from escalation.resources import Resources
from escalation.config import load_config
out=ROOT/'results/v4_projection_diagnostic/analysis';out.mkdir(exist_ok=True)
with Resources(load_config('configs/followup_v3.yaml'),'artifacts/resource_ledger_v2.json'):
    projection=lines('results/v4_projection_diagnostic/runs.jsonl')
    classical=lines('results/v3/classical/runs.jsonl');llm=lines('results/v3/runs.jsonl')
    assert all(r['namespace']=='measured_non_llm_projection_diagnostic' for r in projection)
    if len(projection)!=15 or any(r['status']!='completed' for r in projection):raise RuntimeError('incomplete denominator; retain statuses, no complete-case primary comparison')
    pairs=[];summary=[]
    for p in projection:
        c=next(r for r in classical if r['dataset']==p['dataset'] and r['seed']==p['seed'] and r['method']=='ezr_centroid_adapted')
        l=next(r for r in llm if r['dataset']==p['dataset'] and r['seed']==p['seed'])
        assert c['prefix_hash']==l['prefix_hash']==p['prefix_hash']
        pairs.append({'dataset':p['dataset'],'seed':p['seed'],'classical_loss':c['loss'],'llm_loss':l['loss'],
                      'projection_loss':p['loss'],'projection_gain_over_classical':c['loss']-p['loss'],
                      'llm_gain_over_projection':p['loss']-l['loss']})
    for name in ['Apache','SQL','X264']:
        pp=[r for r in pairs if r['dataset']==name]
        rr=[r for r in classical if r['dataset']==name and r['method']=='random']
        summary.append({'dataset':name,'n':len(pp),'random_mean_loss':float(np.mean([r['loss'] for r in rr])),
                        **{key:float(np.mean([r[key] for r in pp])) for key in ['classical_loss','llm_loss','projection_loss','projection_gain_over_classical','llm_gain_over_projection']}})
    for name,rows in [('paired_comparison.csv',pairs),('method_summary.csv',summary)]:
        with (out/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    costs={'new_label_accesses':sum(r['actual_new_accesses'] for r in projection),'new_model_requests':0,
           'new_input_tokens':0,'new_output_tokens':0,'measured_branch_seconds':sum(r['branch_seconds'] for r in projection),
           'all_version_label_accesses':1508+sum(r['actual_new_accesses'] for r in projection),
           'projected':sum(e['projected'] for r in projection for e in r['events']),
           'duplicates':sum(e['duplicate'] for r in projection for e in r['events']),
           'collisions':sum(e['collision'] for r in projection for e in r['events']),
           'external_experiment_spend_usd':0,'scope':'projection diagnostic only; historical inference remains charged'}
    write(out/'summary.json',{'scope':'exploratory, exposed three-system diagnostic','systems':summary,'costs':costs,
        'llm_materially_better_than_projection':sum(p['llm_gain_over_projection']>.02 for p in pairs),
        'projection_materially_better_than_llm':sum(p['llm_gain_over_projection']<-.02 for p in pairs)})
    os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,3.8))
    colors={'Apache':'#0072B2','SQL':'#D55E00','X264':'#009E73'}
    for j,p in enumerate(pairs):ax.scatter(j,p['llm_gain_over_projection'],color=colors[p['dataset']])
    ax.axhline(0,color='black',lw=.8)
    for delta in [-.02,.02]:ax.axhline(delta,color='gray',ls='--',lw=.8)
    ax.set_xticks(range(15),[f'{p["dataset"]}\n{p["seed"]}' for p in pairs],fontsize=8)
    ax.set_ylabel('Projection loss − LLM loss\n(positive favors LLM)')
    ax.set_title('Uniform projection control versus real LLM — exposed pilot systems')
    fig.tight_layout();fig.savefig(out/'llm_vs_projection.png',dpi=170);fig.savefig(out/'llm_vs_projection.pdf');plt.close(fig)
print(json.dumps(read(out/'summary.json'),indent=2))
