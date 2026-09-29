"""Post-hoc descriptive diversity/figure audit; no policy fitting or new labels."""
import os,sys,collections,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib');os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.io import read,write,lines
from escalation.resources import Resources
from escalation.config import load_config
from escalation.finite_v6 import load_candidates,parse_symbols

def main():
    out=ROOT/'results/v6';s=read(out/'summary.json');rows=read(out/'outcomes.json');req=lines(out/'requests.jsonl')
    diversity=[];manifest=read(ROOT/'data/manifest_v6.json');candidates={d['id']:load_candidates(d) for d in manifest['datasets'] if d['selected']}
    for r in req:
        if r['namespace']!='measured_v6' or r['status']!='response':continue
        proposed=r['raw_output'].splitlines();c=candidates[r['dataset']]
        p=read(out/'prefixes'/(r['dataset']+'_'+str(r['seed'])+'.json'));prefix={tuple(c.x[i]) for i in p['state']['ids']}
        copied=sum(tuple(x) in prefix for x in parse_symbols(r['raw_output'],c))
        diversity.append({'dataset':r['dataset'],'seed':r['seed'],'split':r['split'],'request_id':r['request_id'],
          'unique_proposal_strings':len(set(proposed)),'proposal_count':len(proposed),'exact_original_prefix_copies':copied})
    d={'label':'post-hoc descriptive diagnostic, no refitting','requests':diversity,
      'unique_strings_per_batch_histogram':dict(collections.Counter(r['unique_proposal_strings'] for r in diversity)),
      'exact_original_prefix_copies':sum(r['exact_original_prefix_copies'] for r in diversity),
      'batch_count':len(diversity),'total_unique_within_batch':sum(r['unique_proposal_strings'] for r in diversity),
      'total_proposals':sum(r['proposal_count'] for r in diversity)}
    write(out/'proposal_diversity.json',d)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(1,2,figsize=(11,4.6));held=[r for r in s['systems'] if r['split']=='test'];x=np.arange(len(held))
    for offset,field,label in [(-.27,'random_loss','Random'),(-.09,'classical_loss','Classical'),(.09,'llm_loss','Local LLM'),(.27,'projection_loss','Uniform projection')]:
        axes[0].bar(x+offset,[r[field] for r in held],.18,label=label)
    axes[0].set_xticks(x,[r['system_group'] for r in held],rotation=12);axes[0].set_ylabel('Mean normalized loss (lower better)');axes[0].legend(fontsize=8)
    points=collections.defaultdict(list)
    labels={'never':'Never','always':'Always','benefit':'Benefit','uncertainty':'Uncertainty','random_development_rate':'Random rate',
      'random_matched_realized_rate_diagnostic':'Matched random*','hindsight_oracle_diagnostic':'Oracle*'}
    for r in s['held_out_policies']:points[(r['escalation_rate'],r['group_mean_loss'])].append(labels[r['policy']])
    for (rate,loss),names in points.items():
        axes[1].scatter(rate,loss,s=45)
        text=' / '.join(names)
        if len(names)>2:text='\n'.join(['Never / Benefit / Uncertainty','Random rate / Matched random*'])
        axes[1].annotate(text,(rate,loss),xytext=(6,9),textcoords='offset points',fontsize=8)
    axes[1].set_xlim(-.07,1.2);axes[1].margins(y=.17);axes[1].set_xlabel('Fraction escalated');axes[1].set_ylabel('Held-out group mean loss')
    fig.suptitle('V6: three held-out families × five seeds; * retrospective diagnostic',fontsize=11);fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(out/('quality_cost_review.'+ext),dpi=180)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4));groups=sorted({r['system_group'] for r in rows})
    for i,g in enumerate(groups):
        rs=[r for r in rows if r['system_group']==g];offset=np.linspace(-.16,.16,len(rs))
        ax.scatter(i+offset,[r['gain'] for r in rs],color='#176b87' if rs[0]['split']=='test' else '#888888',s=34)
    ax.axhline(0,color='black',linewidth=.6);ax.axhline(.02,color='gray',linestyle='--',linewidth=.7);ax.axhline(-.02,color='gray',linestyle='--',linewidth=.7)
    ax.set_xticks(range(len(groups)),groups,rotation=15);ax.set_ylabel('Classical loss − LLM loss (positive helps)')
    ax.set_title('All 30 paired gains; blue = held-out, gray = development\nDashed lines: predeclared ±.02 material margin',fontsize=10)
    fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(out/('paired_gains.'+ext),dpi=180)
    plt.close(fig)
    print(json.dumps({k:v for k,v in d.items() if k!='requests'},indent=2))
if __name__=='__main__':
    with Resources(load_config('configs/followup_v3.yaml'),'artifacts/resource_ledger_v2.json') as r:r.check();main();r.check()
