"""Analysis only: exact combinatorial reference plus independent enumeration."""
import sys,itertools,math,csv,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from escalation.io import read,write,now,lines
from escalation.data import sha
from escalation.core import losses
from escalation.finite_v6 import load_candidates
from escalation.study_v6 import retrospective_labels
from escalation.study_v8 import verify,manifest,run_config
from escalation.resources import Resources
from escalation.selection_null_v9 import uniform_minimum_distribution,event_probability,quantile

OUT=Path('results/v9_analysis')

def main(resources):
    verify()
    f=read('reports/protocol_v9_analysis.freeze.json')
    for p,h in f['sha256'].items():assert sha(p)==h,p
    if (OUT/'summary.json').exists():raise RuntimeError('analysis already exists; do not silently overwrite')
    m=manifest();old=read('results/v8/summary.json');diagnostic=read('results/v8/selection_diagnostics.json')
    assert old['complete'] and diagnostic['row_sequence_matches']==15
    combinations=np.asarray(list(itertools.combinations(range(20),10)),dtype=np.int16)
    assert combinations.shape==(184756,10)
    records=[];supports=[];checks=[]
    for d in m['datasets']:
        c=load_candidates(d);ys=retrospective_labels(d,c);scores=losses(ys,c.directions)
        for seed in m['seeds']:
            resources.check();key=d['id']+'_'+str(seed)
            p=read('results/v6/prefixes/'+key+'.json');b=read('results/v8/llm/'+key+'.json')
            case=next(x for x in m['cases'] if x['dataset']==d['id'] and x['seed']==seed)
            outcome=next(x for x in old['records'] if x['dataset']==d['id'] and x['seed']==seed)
            incumbent=float(min(scores[p['state']['ids']]));values=scores[case['pool']['ranked']]
            dist=uniform_minimum_distribution(values,incumbent,10)
            # Independent enumeration does not use the formula or its ranks/counts.
            brute=np.minimum(incumbent,values[combinations].min(axis=1))
            unique,counts=np.unique(brute,return_counts=True)
            assert {float(v):int(n) for v,n in zip(unique,counts)}=={r['loss']:r['subsets'] for r in dist['support']}
            assert math.isclose(float(brute.mean()),dist['expected_loss'],abs_tol=1e-14)
            observed=float(min(scores[b['state']['ids']]))
            first_half=list(case['pool']['mapping'].values())[:10]
            assert b['state']['ids'][10:]==first_half and observed==outcome['llm_selection']
            base=outcome['classical'];expected=dist['expected_loss']
            records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'incumbent_loss':incumbent,
              'classical_loss':base,'observed_llm_loss':observed,'uniform_expected_loss':expected,'observed_static_rank_loss':outcome['static_rank'],
              'observed_uniform_control_loss':outcome['uniform_selection'],'expected_gain_over_classical':base-expected,
              'observed_gain_over_classical':base-observed,'observed_advantage_over_uniform_expectation':expected-observed,
              'probability_random_no_worse_than_observed':event_probability(dist,lambda loss:loss<=observed),
              'probability_random_material_help_vs_classical':event_probability(dist,lambda loss:base-loss>.02),
              'probability_random_material_harm_vs_classical':event_probability(dist,lambda loss:base-loss<-.02),
              'random_loss_q05':quantile(dist,.05),'random_loss_q95':quantile(dist,.95),
              'exact_first_half_sequence_match':True,'subsets_enumerated':len(brute)})
            supports.append({'dataset':d['id'],'seed':seed,**dist})
            checks.append({'dataset':d['id'],'seed':seed,'formula_matches_all_subsets':True,'subsets':len(brute)})
    cols=['classical_loss','observed_llm_loss','uniform_expected_loss','observed_static_rank_loss','observed_uniform_control_loss',
          'expected_gain_over_classical','observed_gain_over_classical','observed_advantage_over_uniform_expectation']
    groups=[{'system_group':g,'cases':5,**{col:math.fsum(r[col] for r in records if r['system_group']==g)/5 for col in cols}}
            for g in sorted({r['system_group'] for r in records})]
    overall={col:math.fsum(g[col] for g in groups)/len(groups) for col in cols}
    result={'at':now(),'namespace':'retrospective_exact_reference_not_measured_arm','post_hoc':True,'records':records,'groups':groups,'equal_group_mean':overall,
      'observed_cases':len(records),'independent_development_groups':len(groups),'subsets_per_case':184756,'verification':checks,
      'all_model_selections_equal_first_displayed_half':True,'new_model_calls':0,'new_optimizer_acquisitions':0,
      'scope':'Conditional finite-pool mathematics; no p-values, unseen-system inference, or claim about unobserved model reorderings'}
    write(OUT/'summary.json',result);write(OUT/'exact_distributions.json',{'namespace':result['namespace'],'distributions':supports})
    with (OUT/'cases.csv').open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    os.environ['MPLCONFIGDIR']=str(Path('.cache/matplotlib').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(11,4))
    for ax,g in zip(axes,groups):
        names=['Adaptive\nclassical','Static\nshortlist','Exact uniform\nexpectation','Observed\nLLM'];fields=cols[:0]+['classical_loss','observed_static_rank_loss','uniform_expected_loss','observed_llm_loss']
        ax.bar(names,[g[k] for k in fields],color=['#657384','#357884','#bd9850','#8171a5'])
        ax.set_title(g['system_group']);ax.set_ylabel('Mean normalized loss (lower better)');ax.tick_params(axis='x',labelsize=8)
    fig.suptitle('Post-hoc reference: all 15 observed LLM outputs select the first displayed half',fontsize=11)
    fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(OUT/('exact_reference.'+ext),dpi=180)
    plt.close(fig);resources.check()
    print(__import__('json').dumps({'groups':groups,'overall':overall,'enumeration_checks':len(checks),'new_model_calls':0,'new_optimizer_acquisitions':0},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as resources:main(resources)
