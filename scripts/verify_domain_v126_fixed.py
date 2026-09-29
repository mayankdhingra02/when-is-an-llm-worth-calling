"""Independent standard-library replay of acquired coverage and feasibility.

No optimizer imports, requests, or new objective acquisitions. Run after collection.
"""
import csv,hashlib,json,math,statistics
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def verify():
    for n,h in read('reports/protocol_v126.freeze.json')['sha256'].items():assert sha(n)==h,n
    specs={s['id']:s for s in read('data/manifest_v41.json')['datasets']};targets={};source={};parsed=0
    for ds,s in specs.items():
        assert sha(s['path'])==s['sha256'];lines=(ROOT/s['path']).read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=s['delimiter']));source[ds]={};targets[ds]={}
        for i,line in enumerate(s['subset']['source_lines']):
            row=dict(zip(header,next(csv.reader([lines[line-1]],delimiter=s['delimiter']))));raw=row[s['primary_objective']];v=float(raw);assert math.isfinite(v) and v>0
            assert all(row[n]==v for n,v in s['filters'].items())
            assert all(float(row[n])==v for n,v in s['fixed_features'].items())
            source[ds][i]=(line,raw);targets[ds][i]=v;parsed+=1
    assert parsed==4992
    plans=read('artifacts/study_v126/plans.json');jobs=read('artifacts/study_v126/cases.json');prefixes=read('artifacts/study_v126/coverage_prefixes.json')
    events=[json.loads(x) for x in (ROOT/'results/v126_domain_audit/acquisitions.jsonl').read_text().splitlines()];by=defaultdict(list)
    for e in events:by[e['key']].append(e)
    assert len(events)==4932 and len(plans)==497 and set(by)=={j['key'] for j in plans};coverage={ds:set() for ds in specs}
    for j in prefixes:
        p=read(j['prefix'])['state'];coverage[j['dataset']].update(p['ids'])
        for i,y in zip(p['ids'],p['labels']):assert targets[j['dataset']][i]==y[0]
        unseen=[i for i in p['order'] if i not in p['ids']];expected=[unseen[i:i+10] for i in range(0,len(unseen),10)]
        assert expected==[x['selected_rows'] for x in plans if x['base_key']==j['key']]
    for j in plans:
        p=read(j['prefix'])['state'];assert sha(j['prefix'])==j['prefix_sha256'];es=by[j['key']];assert [e['row_id'] for e in es]==j['selected_rows']
        for e in es:
            i=e['row_id'];assert e['dataset']==j['dataset'] and (e['source_line'],e['raw_target'])==source[j['dataset']][i]
            assert i not in coverage[j['dataset']];coverage[j['dataset']].add(i)
        arm=read(f"results/v126_domain_audit/branches/{j['key']}.json");s=arm['state'];assert s['order']==p['order'];assert s['ids']==p['ids']+j['selected_rows'];assert s['labels']==p['labels']+[[float(e['raw_target'])] for e in es];assert len(s['ids'])==len(set(s['ids']))==arm['logical_evaluations']<=20;assert arm['new_acquisitions']==len(es)
    assert all(coverage[ds]==set(t) for ds,t in targets.items())
    result=read('results/v126_domain_audit/comparison.json');receipt=read('results/v126_domain_audit/collection.json');assert receipt['complete'] and receipt['error'] is None and receipt['new_recorded_acquisitions']==4932 and receipt['completed_branches']==receipt['intended_branches']==497 and receipt['seconds']<=180 and receipt['new_model_requests']==0;assert result['collection']==receipt
    old={(c['dataset'],c['seed']):c for c in read('results/v42_selection_reference/summary.json')['cases']};assert len(result['cases'])==len(jobs)==30;controls=0
    for j,r in zip(jobs,result['cases']):
        assert all(r[k]==v for k,v in j.items());s=specs[j['dataset']];direction=s['direction'];opt=min if direction=='-' else max;t=targets[j['dataset']];p=read(j['prefix']);g=opt(t.values());pool=opt([y[0] for y in p['state']['labels']]+[t[i] for i in p['pool']['mapping'].values()]);assert r['direction']==direction and r['domain_best']==g and r['domain_size']==len(t) and r['shortlist_best']==pool
        o=old[j['dataset'],j['seed']];assert Fraction(str(pool))==Fraction(o['shortlist_ceiling']);assert set(p['pool']['mapping'].values())==set(o['candidate_ids']) and len(p['pool']['mapping'])==len(o['candidate_ids'])==20
        for i,v in zip(o['candidate_ids'],o['acquired_candidate_targets']):assert Fraction(str(t[i]))==Fraction(v)
        for i,y in zip(p['state']['ids'],p['state']['labels']):assert t[i]==y[0]
        refs={}
        for m in ['batch_3nn','full_sequential_3nn','random_full','single_portfolio']:
            path=f"results/v115_portfolio/arms/{j['key']}.json" if m=='single_portfolio' else f"results/v41_transfer/arms/{j['key']}_{m}.json"
            if not (ROOT/path).exists():assert m=='single_portfolio';continue
            a=read(path)['state'];assert a['ids'][:10]==p['state']['ids'] and a['labels'][:10]==p['state']['labels'] and len(set(a['ids']))==len(a['ids'])==20
            for i,y in zip(a['ids'],a['labels']):assert t[i]==y[0]
            refs[m]=opt(y[0] for y in a['labels']);controls+=1
        assert r['references']==refs
        gains={m:(Fraction(str(v))-Fraction(str(g)))/Fraction(str(v))*(1 if direction=='-' else -1) for m,v in refs.items()};assert r['hindsight_global_gains']=={m:float(v) for m,v in gains.items()}
        assert r['joint_batch_sequential_5pct_possible']==all(gains[m]>=Fraction('0.05') for m in ['batch_3nn','full_sequential_3nn']);assert r['sequential_5pct_possible']==(gains['full_sequential_3nn']>=Fraction('0.05'))
    for f in result['families']:
        rs=[r for r in result['cases'] if r['system_group']==f['system_group']];assert len(rs)==f['cases']==5
        assert f['mean_global_gain_vs_sequential']==statistics.mean(r['hindsight_global_gains']['full_sequential_3nn'] for r in rs)
        assert f['joint_5pct_possible']==sum(r['joint_batch_sequential_5pct_possible'] for r in rs)
        assert f['sequential_5pct_possible']==sum(r['sequential_5pct_possible'] for r in rs)
        assert f['sequential_attains_global_best']==sum(r['references']['full_sequential_3nn']==r['domain_best'] for r in rs)
    assert result['joint_5pct_possible_cases']==sum(r['joint_batch_sequential_5pct_possible'] for r in result['cases'])
    assert result['sequential_5pct_possible_cases']==sum(r['sequential_5pct_possible'] for r in result['cases'])
    assert result['equal_family_mean_global_gain_vs_sequential']==statistics.mean(f['mean_global_gain_vs_sequential'] for f in result['families'])
    return {'verified':True,'source_values_replayed':parsed,'charged_journal_events':len(events),'coverage_branches':len(plans),'prefixes':30,'independent_exposed_families':6,'control_states':controls,'prior_v42_pool_ceilings_matched':30,'new_model_requests':0,'new_objective_acquisitions':0}
if __name__=='__main__':
    r=verify();(ROOT/'artifacts/study_v126/verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
