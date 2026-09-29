"""Exploratory group influence and finite-trace routing headroom; no new outcomes."""
import argparse,hashlib,json,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/v117_influence'

def grouped(rows):
    prefixes=defaultdict(list)
    for r in rows:prefixes[(r['family'],r['base_key'])].append(r['gain'])
    groups=defaultdict(list)
    for (family,_),g in prefixes.items():groups[family].append(statistics.mean(g))
    return {f:statistics.mean(g) for f,g in sorted(groups.items())}

def analyze(rows):
    groups=grouped(rows);mean=statistics.mean(groups.values())
    loo={g:statistics.mean(v for f,v in groups.items() if f!=g) for g in groups}
    oracle=grouped([{**r,'gain':max(0,r['gain'])} for r in rows])
    return {'group_means':groups,'mean':mean,'median_group':statistics.median(groups.values()),
      'group_wins':sum(v>0 for v in groups.values()),'group_ties':sum(v==0 for v in groups.values()),'group_losses':sum(v<0 for v in groups.values()),
      'leave_one_group_out':loo,'mean_sign_changes_after_omission':sum((v>0)!=(mean>0) and v!=0 and mean!=0 for v in loo.values()),
      'nondeployable_oracle_headroom_mean':statistics.mean(oracle.values()),
      'nondeployable_oracle_positive_choices':sum(r['gain']>0 for r in rows),
      'observed_practical_win_count':sum(r['gain']>=.05 for r in rows),
      'observed_practical_win_groups':sorted({r['family'] for r in rows if r['gain']>=.05}),
      'n_groups':len(groups),'n_replicas':len(rows)}

def produce():
    freeze=json.loads((ROOT/'reports/protocol_v117.freeze.json').read_text())
    for n,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    a=json.loads((ROOT/'results/v114_analysis/summary.json').read_text())['cases']
    b=json.loads((ROOT/'results/v115_analysis/summary.json').read_text())['cases']
    assert len(a)==len(b)==36 and {r['key'] for r in a}=={r['key'] for r in b}
    controls={c:[{**r,'gain':r['gains'][c]} for r in a] for c in ['batch_3nn','full_sequential_3nn']}
    controls['single_portfolio']=b
    result={'scope':'Exploratory post-outcome diagnostic on six exposed groups; not group-CV of a learned model, not a confidence interval, not independent confirmation.',
      'new_model_requests':0,'new_objective_acquisitions':0,'controls':{c:analyze(rows) for c,rows in controls.items()},
      'oracle_caveat':'Finite saved-trace upper reference choosing classical or that single sampled LLM continuation with hindsight. Not best of three model samples; no cost-free deployable oracle and no population upper bound.'}
    OUT.mkdir(exist_ok=True);(OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# V117: how dependent is the conclusion on individual systems?','','This is a saved-data sensitivity analysis. No model was called and no objective was acquired. All six groups and all 36 observed LLM continuations remain in the primary analysis. Each sampling replica is averaged within its prefix, prefixes within their family, then families equally. Leave-one-family-out calculations diagnose influence; they do not evaluate a learned router or create new independent test data.','','| Comparator | Mean gain | Median group gain | Mean range after omitting one family | Hindsight branch-selection headroom |','|---|---:|---:|---:|---:|']
    for name,d in result['controls'].items():
        v=list(d['leave_one_group_out'].values());lines.append(f"| {name} | {100*d['mean']:.3f}% | {100*d['median_group']:.3f}% | {100*min(v):.3f}% to {100*max(v):.3f}% | {100*d['nondeployable_oracle_headroom_mean']:.3f}% |")
    d=result['controls']['single_portfolio']
    lines+=['',f"Omitting OpenVPN changes the single-portfolio mean from {100*d['mean']:.3f}% to {100*d['leave_one_group_out']['openvpn']:.3f}%. Thus a general claim of average LLM harm is not robust to this family omission. Do not discard OpenVPN or replace the primary result with the favorable subset. The median group gain is {100*d['median_group']:.3f}%; only {d['group_wins']} of six family means are positive.",'','The original practical-margin result is narrower and stable: no saved LLM replica beats the single portfolio by 5%, so dropping a family cannot create such a win. Report small wins too (nine replicas; maximum3.34%). The original batch and sequential comparisons remain separate; their values are shown above rather than hidden behind the blend.','', 'The hindsight column clips each saved gain at zero and then uses the same nested weighting. It selects between that replica and its classical counterfactual after observing both outcomes, so it is explicitly non-deployable. It is not a controller result, a best-of-three model policy, or a bound on future tasks. Both branches and all historical model calls remain charged in the research ledger.','','No p-values or population uncertainty intervals are justified here. These diagnostics refine interpretation of the existing negative-result candidate; they cannot establish Q2 readiness or cross-system routing benefit. Untouched evaluation groups and independent native measurement remain untested.','','Reproduce with `.venv/bin/python scripts/analyze_influence_v117.py`. Machine output: `results/v117_influence/summary.json`; plot: `influence.png`/`influence.svg`.']
    (ROOT/'reports/influence_v117.md').write_text('\n'.join(lines)+'\n')
    import matplotlib
    matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='influence-v117'
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
    for ax,(name,d) in zip(axes,result['controls'].items()):
        labels=list(d['leave_one_group_out']);values=[100*d['leave_one_group_out'][g] for g in labels]
        ax.scatter(values,range(len(labels)),color='#315c91',s=38,label='Omit named family')
        ax.axvline(100*d['mean'],color='#aa4b40',label='All families')
        ax.axvline(0,color='gray',linewidth=.8,linestyle=':');ax.set_yticks(range(len(labels)),labels);ax.set_title(name.replace('_',' '));ax.set_xlabel('Group-first mean gain (%)');ax.grid(axis='x',alpha=.2)
    axes[0].invert_yaxis();axes[2].legend(fontsize=8,loc='best');fig.suptitle('Sensitivity to one-family omission — diagnostic, not confidence intervals')
    fig.tight_layout();fig.savefig(OUT/'influence.png',dpi=170);fig.savefig(OUT/'influence.svg',metadata={'Date':None});plt.close(fig)
    return result

if __name__=='__main__':
    r=produce();print(json.dumps(r,indent=2))
