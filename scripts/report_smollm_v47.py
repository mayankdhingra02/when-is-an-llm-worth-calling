"""Regenerate V47 figures and the post-hoc no-LLM ordering diagnostic."""
import json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'results/v47_analysis'
def read(p):return json.loads((ROOT/p).read_text())
def main():
    cases=read('results/v47_analysis/cases.json');summary=read('results/v47_analysis/summary.json')
    checks=[]
    for r in cases:
        prefix=read(r['prefix']);old=read(f"results/v41_models/0.5/arms/{r['key']}.json")
        selected=[prefix['pool']['mapping'][i] for i in '0123456789']
        assert old['state']['ids'][10:]==selected
        # Reuse previously acquired outcomes; do not read additional target cells.
        direction=next(d['direction'] for d in read('data/manifest_v41.json')['datasets'] if d['id']==r['dataset'])
        target=(min if direction=='-' else max)(x[0] for x in old['state']['labels'])
        checks.append({'case':r['key'],'first10_ids':list('0123456789'),'rows':selected,
            'first10_target_from_previously_acquired_labels':target,'smollm_target':r['target'],
            'same_target':target==r['target'],'historical_label_source':f"results/v41_models/0.5/arms/{r['key']}.json"})
    diagnostic={'qualification':'Post-hoc explanatory ordering control, not a preregistered baseline or independent test',
        'new_requests':0,'new_acquisitions':0,'same_target_cases':sum(x['same_target'] for x in checks),'cases':checks}
    (OUT/'ordering_diagnostic.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
    refs=['batch_3nn','full_sequential_3nn'];families=sorted(summary['contrasts'][refs[0]]['family_means'])
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    for ax,ref,title in zip(axes,refs,['Matched pool: batch 3NN','Full domain: sequential 3NN']):
        vals=[100*summary['contrasts'][ref]['family_means'][f] for f in families]
        ax.barh(families,vals,color=['#317c59' if v>0 else '#a84c45' for v in vals])
        ax.axvline(0,color='#333333',linewidth=.8)
        ax.set_title(title);ax.set_xlabel('Relative gain (%) — positive favors SmolLM3')
        ax.set_xlim(-20,2)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('SmolLM3-3B Q4_K_M: six exposed software families, five seeds each\nExploratory robustness; seeds are not independent systems',fontsize=12)
    fig.savefig(OUT/'family_gains.png',dpi=180);fig.savefig(OUT/'family_gains.svg');plt.close(fig)
    names=['batch_3nn','full_sequential_3nn','qwen_0.5','qwen_1.5']
    table=['| Reference | Mean relative gain | Descriptive family bootstrap 95% | Wins / ties / harms |','|---|---:|---:|---:|']
    for name in names:
        c=summary['contrasts'][name];lo,hi=c['bootstrap95']
        table.append(f"| {name} | {100*c['family_mean_gain']:+.3f}% | [{100*lo:+.3f}%, {100*hi:+.3f}%] | {c['wins']} / {c['ties']} / {c['harms']} |")
    (OUT/'key_results.md').write_text('\n'.join(table)+'\n')
    print('Ordering diagnostic:',diagnostic['same_target_cases'],'of 30 identical final targets; no new inference or acquisitions')
if __name__=='__main__':main()
