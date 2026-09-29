"""Post-hoc paired quality feasibility; no optimizer or model requests."""
import sys,csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,now
from escalation.data import sha
from escalation.finite_v6 import load_candidates
from escalation.study_v8 import manifest,verify,run_config
from escalation.resources import Resources
from escalation.quality_v11 import constrained_case
OUT=Path('results/v11_quality')


def main(resources):
    verify()
    for p,h in read('reports/protocol_v11_quality.freeze.json')['sha256'].items():assert sha(p)==h,p
    if (OUT/'summary.json').exists():raise RuntimeError('refuse overwrite')
    m=manifest();ds=[d for d in m['datasets'] if d['id'] in ['brotli','lrzip']]
    assert len(ds)==2 and all(d['split']=='development' and 'size' in d['objective_columns'] for d in ds)
    cases=[];records=[]
    for d in ds:
        c=load_candidates(d);wanted=set(c.source_ids);values={}
        for p,h in d['evidence'].items():assert sha(p)==h
        with Path(d['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
                if line in wanted:values[line]=(float(row['performance']),float(row['size']))
        runtime=[values[i][0] for i in c.source_ids];size=[values[i][1] for i in c.source_ids]
        assert all(math.isfinite(x) and x>0 for x in runtime+size)
        for seed in m['seeds']:
            resources.check();key=d['id']+'_'+str(seed)
            p=read('results/v6/prefixes/'+key+'.json')
            inputs={'static_rank':read('results/v8/static_rank/'+key+'.json')['state'],
                'adaptive_classical':read('results/v6/classical/'+key+'.json')['arms']['centroid_nominal']['state'],
                'observed_llm':read('results/v8/llm/'+key+'.json')['state']}
            for state in inputs.values():assert state['labels']==[[runtime[i]] for i in state['ids']]
            pool=next(r['pool']['ranked'] for r in m['cases'] if r['dataset']==d['id'] and r['seed']==seed)
            result=constrained_case(p['state']['ids'],pool,{name:s['ids'] for name,s in inputs.items()},runtime,size)
            cases.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'source_sha256':d['sha256'],**result})
            for arm,base in result['arms'].items():
                for scope,bound in result['bounds'].items():
                    records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'baseline':arm,'scope':scope,
                        'anchor_row':result['anchor'],'size_cap':result['size_cap'],'baseline_row':base['row_id'],
                        'baseline_runtime':base['runtime'],'baseline_size':base['size'],'oracle_row':bound['row_id'],
                        'oracle_runtime':bound['runtime'],'oracle_size':bound['size'],'baseline_feasible_rows':base['feasible_rows'],
                        'bound_feasible_rows':bound['feasible_rows'],'relative_runtime_headroom':(base['runtime']-bound['runtime'])/base['runtime'],
                        'absolute_runtime_headroom':base['runtime']-bound['runtime'],'oracle_size_ratio_to_cap':bound['size']/result['size_cap']})
    summaries=[]
    for arm in ['static_rank','adaptive_classical','observed_llm']:
        for scope in ['shortlist','full_table']:
            for group in ['brotli','lrzip','all_two_groups']:
                rs=[r for r in records if r['baseline']==arm and r['scope']==scope and (group=='all_two_groups' or r['system_group']==group)]
                summaries.append({'baseline':arm,'scope':scope,'group':group,'cases':len(rs),
                    'mean_relative_headroom':math.fsum(r['relative_runtime_headroom'] for r in rs)/len(rs),
                    'sensitivity_counts':{str(t):sum(r['relative_runtime_headroom']>t for r in rs) for t in [0,.05,.1,.2]}})
    write(OUT/'summary.json',{'at':now(),'namespace':'post_hoc_runtime_size_feasibility_not_measured_policy','independent_groups':2,
        'cases':cases,'comparisons':records,'summaries':summaries,'new_model_calls':0,'new_optimizer_acquisitions':0,
        'limitations':['size only retrospectively read, unavailable to old optimizer','bound uses hidden targets and is not deployable',
        'output size is not a correctness/quality validation','source repeated-measurement uncertainty not available here','no learned LLM or router benefit established']})
    with (OUT/'cases.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    resources.check();print(json.dumps({'primary_static_baseline':[r for r in summaries if r['baseline']=='static_rank'],'complete_cases':len(cases)},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:main(r)
