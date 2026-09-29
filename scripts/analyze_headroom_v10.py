"""No-call headroom decision from all saved development cases."""
import sys,math,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from escalation.io import read,write,now
from escalation.data import sha
from escalation.core import losses
from escalation.headroom_v10 import bounds,material,relative_improvement
from escalation.finite_v6 import load_candidates
from escalation.study_v6 import retrospective_labels
from escalation.study_v8 import manifest,run_config,verify
from escalation.resources import Resources
OUT=Path('results/v10_headroom')


def main(resources):
    verify()
    for p,h in read('reports/protocol_v10_headroom.freeze.json')['sha256'].items():assert sha(p)==h,p
    if (OUT/'summary.json').exists():raise RuntimeError('refuse overwrite of completed analysis')
    m=manifest();old=read('results/v8/summary.json');null=read('results/v9_analysis/exact_distributions.json');records=[];tables=[]
    for d in m['datasets']:
        c=load_candidates(d);ys=retrospective_labels(d,c);scores=losses(ys,c.directions);raw=[y[0] for y in ys]
        assert d['direction']=='-' and min(raw)>0,'primary raw-relative diagnostic requires positive minimized runtime'
        tables.append({'dataset':d['id'],'system_group':d['system_group'],'meaning':d['meaning'],'rows':len(raw),'minimum':min(raw),
            'median':float(np.median(raw)),'maximum':max(raw),'material_margin_in_source_units':.02*(max(raw)-min(raw))})
        for seed in m['seeds']:
            resources.check();key=d['id']+'_'+str(seed);p=read('results/v6/prefixes/'+key+'.json')
            case=next(case for case in m['cases'] if case['dataset']==d['id'] and case['seed']==seed)
            prior=next(row for row in old['records'] if row['dataset']==d['id'] and row['seed']==seed)
            dist=next(row for row in null['distributions'] if row['dataset']==d['id'] and row['seed']==seed)
            best=bounds(scores,p['state']['ids'],case['pool']['ranked'])
            assert best['shortlist']==prior['shortlist_hindsight_loss']==min(r['loss'] for r in dist['support'])
            raw_best={'shortlist':min(raw[i] for i in p['state']['ids']+case['pool']['ranked']),'full_table':min(raw)}
            states={'static_rank':read('results/v8/static_rank/'+key+'.json')['state'],
                'adaptive_classical':read('results/v6/classical/'+key+'.json')['arms']['centroid_nominal']['state'],
                'observed_llm':read('results/v8/llm/'+key+'.json')['state']}
            for arm,state in states.items():
                assert state['labels']==[ys[i] for i in state['ids']]
                base=float(min(scores[state['ids']]));raw_base=min(raw[i] for i in state['ids'])
                span=max(raw)-min(raw)
                assert math.isclose(base,(raw_base-min(raw))/span if span else 0,abs_tol=1e-14)
                for scope in ['shortlist','full_table']:
                    h=base-best[scope]
                    records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'baseline':arm,'scope':scope,
                        'baseline_loss':base,'oracle_loss':best[scope],'headroom':h,'material_at_002':material(h),
                        'raw_baseline':raw_base,'raw_oracle':raw_best[scope],'relative_runtime_reduction_bound':relative_improvement(raw_base,raw_best[scope],d['direction'])})
            for scope in ['shortlist','full_table']:
                h=dist['expected_loss']-best[scope]
                records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'baseline':'uniform_expectation','scope':scope,
                    'baseline_loss':dist['expected_loss'],'oracle_loss':best[scope],'headroom':h,'material_at_002':material(h),
                    'raw_baseline':None,'raw_oracle':None,'relative_runtime_reduction_bound':None})
    groups=[];summaries=[]
    for arm in ['static_rank','adaptive_classical','observed_llm','uniform_expectation']:
        for scope in ['shortlist','full_table']:
            rs=[r for r in records if r['baseline']==arm and r['scope']==scope]
            local=[]
            for g in sorted({r['system_group'] for r in rs}):
                subset=[r for r in rs if r['system_group']==g]
                item={'baseline':arm,'scope':scope,'system_group':g,'cases':len(subset),
                    'mean_headroom':math.fsum(r['headroom'] for r in subset)/len(subset),'material_cases':sum(r['material_at_002'] for r in subset)}
                groups.append(item);local.append(item)
            summaries.append({'baseline':arm,'scope':scope,'cases':len(rs),'mean_headroom':math.fsum(r['mean_headroom'] for r in local)/len(local),
                'material_cases':sum(r['material_at_002'] for r in rs),'families_with_material_cases':sum(r['material_cases']>0 for r in local),
                'families_with_material_mean':sum(material(r['mean_headroom']) for r in local),
                'margin_sensitivity':{str(margin):sum(material(r['headroom'],margin) for r in rs) for margin in [.005,.01,.02,.05]}})
    write(OUT/'summary.json',{'at':now(),'namespace':'post_hoc_headroom_not_measured_policy','primary_baseline':'static_rank','margin':.02,
      'scope':'all15 V8 development cases; no test reuse or changed outcome criterion','summaries':summaries,'groups':groups,'cases':records,'table_scales':tables,
      'new_model_calls':0,'new_optimizer_acquisitions':0,'oracle_is_nondeployable':True,'saved_bounds_crosschecked':15})
    with (OUT/'cases.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    resources.check();print(json.dumps({'summaries':summaries,'table_scales':tables},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:main(r)
