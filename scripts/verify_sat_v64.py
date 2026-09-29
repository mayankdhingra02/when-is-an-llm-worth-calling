"""Independent V64 physical and classical-policy reconstruction from saved records."""
import hashlib,itertools,json,math,random,statistics,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from verify_sat_v62 import check
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)
def main():
    start=time.monotonic();freeze=ROOT/'reports/protocol_v64_sat_screen.freeze.json'
    for name,h in read(freeze)['sha256'].items():assert digest(ROOT/name)==h,name
    a=read(ROOT/'artifacts/study_v64/approval_receipt.json');assert a['authorized_scope_invocation'] and a['protocol_freeze_sha256']==digest(freeze)
    assert a['max_stage_seconds']==7200 and a['max_physical_trials']==288 and a['max_model_requests']==a['max_external_spend_usd']==0
    raw=ROOT/'results/v64_sat_physical';screen=ROOT/'results/v64_sat_screen';summary=read(raw/'summary.json')
    assert summary['complete_table'] and summary['attempted']==288 and summary['stage_seconds']<=7200
    tasks=[read(ROOT/'data/generated_v62/manifest.json')[0],read(ROOT/'data/generated_v63/manifest.json')[0]]
    configs=list(itertools.product([.8,.95],[.9,.999],[25,100,400],[1.2,2],[0,2]));expected=[]
    for rep in range(3):
        for ti,task in enumerate(tasks):
            ids=list(range(48));random.Random(64000+rep*1000+ti).shuffle(ids)
            for cid in ids:expected.append({'trial':len(expected),'round':rep,'task':task,'family':'minisat','workload':task['id'],'config_id':cid,'configuration':list(configs[cid])})
    assert expected==read(raw/'schedule.json')
    rows=read(raw/'all_cases.json');journal=[json.loads(line) for line in (raw/'trials.jsonl').read_text().splitlines()];assert rows==journal and len(rows)==288
    valid=0;failures=0
    for r,spec in zip(rows,expected):
        assert all(r[k]==v for k,v in spec.items())
        folder=raw/f"trial_{r['trial']:02d}";assert read(folder/'result.json')==r
        receipt=read(folder/'start.json');assert all(r[k]==v for k,v in receipt.items())
        assert digest(folder/'solver.log')==r['log_sha256'];cmd=r['command']
        assert '-cpu-lim=18' in cmd and cmd[-2:]==[str(ROOT/r['task']['path']),str(folder/'model.txt')]
        for k,v in zip(['var-decay','cla-decay','rfirst','rinc','phase-saving'],r['configuration']):assert f'-{k}={v}' in cmd
        if r['status']=='valid':
            assert r['exit_code']==10 and r['termination_reason'] is None and r['wall_seconds']<=20
            assert digest(folder/'model.txt')==r['model_sha256']
            assert check((ROOT/r['task']['path']).read_text(),(folder/'model.txt').read_text())==r['validation']
            eq(r['objective_ms'],1000*r['wall_seconds']);valid+=1
        else:
            assert r['status']=='resource_noncompletion' and r['objective_ms']==40000
            log=(folder/'solver.log').read_text()
            assert r['termination_reason'] in ['wall_timeout','rss_watchdog'] or r['exit_code']==-24 or 'INDETERMINATE' in log or 'INTERRUPTED' in log
            failures+=1
    assert summary['valid']==valid
    s=read(screen/'summary.json');assert s['arms']==30 and s['recorded_accesses']==400 and s['primary_comparator']=='rf_lcb'
    x=np.array([[int(a==.95),int(b==.999),{25:0,100:.5,400:1}[c],int(d==2),int(e==2)] for a,b,c,d,e in configs]);decisions=0;charges=0
    for w in s['workloads']:
        folder=screen/('minisat_'+w['workload']);table=read(folder/'table.json');assert len(table)==48 and digest(folder/'table.json')==w['table_sha256']
        for cid,t in enumerate(table):
            rr=[r for r in rows if r['workload']==w['workload'] and r['config_id']==cid];values=[r['objective_ms'] for r in rr]
            assert len(values)==3 and t['config_id']==cid and t['configuration']==list(configs[cid]) and t['values_ms']==values
            eq(t['median_ms'],statistics.median(values));eq(t['cv'],statistics.stdev(values)/statistics.mean(values))
            assert t['valid_repetitions']==sum(r['status']=='valid' for r in rr)
        events=[json.loads(line) for line in (folder/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==200;used=[]
        for i,e in enumerate(events):assert e['event_id']==i and e['value_ms']==table[e['config_id']]['median_ms']
        def check_events(obs,seed,arm,offset):
            for i,o in enumerate(obs):
                e=events[o['source_event_id']];assert e['case']==seed and e['arm']==arm and e['inclusive_step']==offset+i+1
                assert e['config_id']==o['config_id'] and e['value_ms']==o['value_ms'];used.append(e['event_id'])
        def choice(obs,method,seed,rng=None):
            nonlocal decisions
            if time.monotonic()-start>180:raise TimeoutError('Verification cap')
            decisions+=1;ids=[o['config_id'] for o in obs];rem=[j for j in range(48) if j not in ids];y=np.array([o['value_ms'] for o in obs])
            if method=='random':return rng.choice(rem)
            if method=='nn':
                scores=[float(np.mean([y[j] for j in sorted(range(len(ids)),key=lambda j:(float(np.mean(abs(x[k]-x[ids[j]]))),j))[:3]])) for k in rem]
            else:
                model=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids)).fit(x[ids],y)
                pred=np.array([tree.predict(x[rem]) for tree in model.estimators_]);scores=pred.mean(axis=0)-pred.std(axis=0)
            return min(zip(scores,rem))[1]
        minimum=min(t['median_ms'] for t in table);eq(w['minimum_ms'],minimum)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3];threshold=max(5.,200*statistics.median(cvs)) if cvs else None
        assert w['threshold_percent']==threshold;hits=0
        assert [c['seed'] for c in w['cases']]==[11,23,37,53,71]
        for c in w['cases']:
            seed=c['seed'];pf=folder/f'prefix_{seed}.json';p=read(pf);assert len(p)==10 and len({o['config_id'] for o in p})==10
            assert [o['config_id'] for o in p[:4]]==random.Random(seed).sample(range(48),4);check_events(p,seed,'prefix',0)
            for n in range(4,10):assert p[n]['config_id']==choice(p[:n],'nn',seed)
            bests={}
            for method in ['random','nn','rf_lcb']:
                arm=read(folder/f'arm_{seed}_{method}.json');obs=arm['observations'];assert obs[:10]==p and arm['prefix_sha256']==digest(pf)
                assert len(obs)==20 and len({o['config_id'] for o in obs})==20;check_events(obs[10:],seed,method,10);rng=random.Random(seed+1000)
                for n in range(10,20):assert obs[n]['config_id']==choice(obs[:n],method,seed,rng)
                bests[method]=min(o['value_ms'] for o in obs)
            assert c['best_ms']==bests;eq(c['prefix_best_ms'],min(o['value_ms'] for o in p))
            hr=100*(bests['rf_lcb']-minimum)/bests['rf_lcb'];eq(c['primary_rf_headroom_percent'],hr)
            eq(c['portfolio_headroom_percent'],100*(min(bests.values())-minimum)/min(bests.values()))
            met=threshold is not None and hr>=threshold;assert c['gate_met']==met;hits+=met
        assert w['gate_case_count']==hits and w['gate_passed']==(hits>=2) and sorted(used)==list(range(200));charges+=200
    print(json.dumps({'verified':True,'physical_trials':288,'valid_models':valid,'resource_noncompletion':failures,'charged_acquisitions':charges,'reconstructed_choices':decisions,'runtime_seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
