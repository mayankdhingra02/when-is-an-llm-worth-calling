"""Independent replay of saved headroom decisions and unchanged collection cost."""
import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines
from escalation.data import sha
from escalation.study_v8 import verify
from escalation.finite_v6 import load_candidates
from escalation.study_v6 import retrospective_labels

verify()
for p,h in read('reports/protocol_v10_headroom.freeze.json')['sha256'].items():assert sha(p)==h,p
s=read('results/v10_headroom/summary.json');m=read('data/manifest_v8.json');old=read('results/v8/summary.json')
for d in m['datasets']:
    c=load_candidates(d);raw=[y[0] for y in retrospective_labels(d,c)];lo=min(raw);span=max(raw)-lo
    for seed in m['seeds']:
        key=d['id']+'_'+str(seed);p=read('results/v6/prefixes/'+key+'.json')
        pool=next(r['pool']['ranked'] for r in m['cases'] if r['dataset']==d['id'] and r['seed']==seed)
        minimum=min(raw[i] for i in p['state']['ids']+pool)
        for r in [r for r in s['cases'] if r['dataset']==d['id'] and r['seed']==seed]:
            target=minimum if r['scope']=='shortlist' else lo
            oracle=(target-lo)/span if span else 0
            assert math.isclose(r['oracle_loss'],oracle,abs_tol=1e-14)
            assert math.isclose(r['headroom'],r['baseline_loss']-oracle,abs_tol=1e-14)
            assert r['material_at_002']==(r['headroom']>.02)
            if r['baseline']!='uniform_expectation':
                assert r['raw_oracle']==target
                assert math.isclose(r['relative_runtime_reduction_bound'],(r['raw_baseline']-target)/r['raw_baseline'],abs_tol=1e-14)
for summary in s['summaries']:
    rs=[r for r in s['cases'] if r['baseline']==summary['baseline'] and r['scope']==summary['scope']]
    assert len(rs)==15
    assert summary['material_cases']==sum(r['headroom']>.02 for r in rs)
    assert summary['families_with_material_cases']==len({r['system_group'] for r in rs if r['headroom']>.02})
    family_means=[sum(r['headroom'] for r in rs if r['system_group']==g)/5 for g in sorted({r['system_group'] for r in rs})]
    assert math.isclose(summary['mean_headroom'],sum(family_means)/3,abs_tol=1e-14)
    for margin,count in summary['margin_sensitivity'].items():assert count==sum(r['headroom']>float(margin) for r in rs)
ledger=read('artifacts/resource_ledger_v2.json');baseline=read('artifacts/study_v10/baseline_ledger.json')
assert ledger['requests']==baseline['requests']==128 and ledger['experiment_seconds']<=1800 and ledger['active_since'] is None
assert len(lines('results/v8/acquisitions.jsonl'))==450 and len(lines('results/v8/requests.jsonl'))==15
write('artifacts/study_v10/verification.json',{'verified':True,'cases':15,'references_checked':len(s['cases']),
    'primary_shortlist_material_cases':next(r['material_cases'] for r in s['summaries'] if r['baseline']=='static_rank' and r['scope']=='shortlist'),
    'new_model_calls':0,'new_optimizer_acquisitions':0,'prior_scientific_freezes_intact':True,'live_requests':ledger['requests'],'experiment_seconds':ledger['experiment_seconds']})
print('Headroom verified:15 cases,120 comparison/bound references; no new calls/acquisitions; prior freezes intact.')
