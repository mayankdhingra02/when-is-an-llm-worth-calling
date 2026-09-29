"""Independent source-row replay of the retrospective quality constraint."""
import sys,csv,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines
from escalation.data import sha
from escalation.finite_v6 import load_candidates
from escalation.study_v8 import verify
verify()
for p,h in read('reports/protocol_v11_quality.freeze.json')['sha256'].items():assert sha(p)==h,p
s=read('results/v11_quality/summary.json');m=read('data/manifest_v8.json');checked=0
assert len(s['cases'])==10 and len(s['comparisons'])==60
for d in m['datasets']:
    if d['id'] not in ['brotli','lrzip']:continue
    c=load_candidates(d)
    with Path(d['path']).open(newline='') as f:rows={n:r for n,r in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2)}
    times={i:float(rows[line]['performance']) for i,line in enumerate(c.source_ids)}
    sizes={i:float(rows[line]['size']) for i,line in enumerate(c.source_ids)}
    for seed in m['seeds']:
        key=d['id']+'_'+str(seed);prefix=read('results/v6/prefixes/'+key+'.json')['state']['ids']
        pool=next(r['pool']['ranked'] for r in m['cases'] if r['dataset']==d['id'] and r['seed']==seed)
        anchor=min(prefix,key=lambda i:times[i]);cap=sizes[anchor]
        r=next(r for r in s['cases'] if r['dataset']==d['id'] and r['seed']==seed)
        assert r['anchor']==anchor and r['size_cap']==cap
        sets={'static_rank':read('results/v8/static_rank/'+key+'.json')['state']['ids'],
            'observed_llm':read('results/v8/llm/'+key+'.json')['state']['ids'],
            'adaptive_classical':read('results/v6/classical/'+key+'.json')['arms']['centroid_nominal']['state']['ids']}
        for name,ids in sets.items():
            eligible=[i for i in ids if sizes[i]<=cap];chosen=min(eligible,key=lambda i:times[i]);v=r['arms'][name]
            assert v['row_id']==chosen and v['runtime']==times[chosen] and v['size']==sizes[chosen] and v['feasible_rows']==len(eligible)
        for scope,ids in [('shortlist',prefix+pool),('full_table',list(times))]:
            eligible=[i for i in ids if sizes[i]<=cap];chosen=min(eligible,key=lambda i:times[i]);v=r['bounds'][scope]
            assert v['row_id']==chosen and v['runtime']==times[chosen] and v['size']==sizes[chosen] and v['feasible_rows']==len(eligible)
        checked+=1
for r in s['comparisons']:
    assert math.isclose(r['relative_runtime_headroom'],(r['baseline_runtime']-r['oracle_runtime'])/r['baseline_runtime'],abs_tol=1e-14)
    assert r['baseline_size']<=r['size_cap'] and r['oracle_size']<=r['size_cap']
for row in s['summaries']:
    rs=[r for r in s['comparisons'] if r['baseline']==row['baseline'] and r['scope']==row['scope'] and (row['group']=='all_two_groups' or r['system_group']==row['group'])]
    assert row['cases']==len(rs)
    assert math.isclose(row['mean_relative_headroom'],sum(r['relative_runtime_headroom'] for r in rs)/len(rs),abs_tol=1e-14)
    for threshold,n in row['sensitivity_counts'].items():assert n==sum(r['relative_runtime_headroom']>float(threshold) for r in rs)
ledger=read('artifacts/resource_ledger_v2.json');before=read('artifacts/study_v11/baseline_ledger.json')
assert ledger['requests']==before['requests']==128 and ledger['active_since'] is None and ledger['experiment_seconds']<1800
assert len(lines('results/v8/acquisitions.jsonl'))==450
write('artifacts/study_v11/verification.json',{'verified':True,'cases_replayed':checked,'references_checked':len(s['comparisons']),
    'source_runtime_and_size_verified':True,'old_scientific_freezes_intact':True,'new_model_calls':0,'new_optimizer_acquisitions':0,
    'requests_used':ledger['requests'],'experiment_seconds':ledger['experiment_seconds']})
print('Verified10 constrained cases and60 bound comparisons; no new inference/acquisitions; prior freezes intact.')
