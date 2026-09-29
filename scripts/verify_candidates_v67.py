"""Independent physical validation, schedule, classical-choice and gate replay."""
import hashlib,itertools,json,math,random,statistics,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from verify_candidates_v66 import check_row,reference_answers
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def design(family):
    if family=='duckdb':
        levels=[[1,2,4,8],['64MB','128MB','256MB','512MB'],[0,8,12]]
        maps=[{1:0,2:1/3,4:2/3,8:1},{'64MB':0,'128MB':1/3,'256MB':2/3,'512MB':1},{0:0,8:2/3,12:1}]
    elif family=='gnu_sort':
        levels=[[1,2,4,8],['1M','4M','16M','64M'],[2,16,64]]
        maps=[{1:0,2:1/3,4:2/3,8:1},{'1M':0,'4M':1/3,'16M':2/3,'64M':1},{2:0,16:3/5,64:1}]
    else:
        assert family=='openjpeg';levels=[[16,32,64],[3,5],[128,256,512,1024],[1,2]]
        maps=[{16:0,32:.5,64:1},{3:0,5:1},{128:0,256:1/3,512:2/3,1024:1},{1:0,2:1}]
    configs=list(itertools.product(*levels));x=np.array([[m[v] for m,v in zip(maps,c)] for c in configs],dtype=float)
    return configs,x

def main():
    start=time.monotonic()
    for name,digest in read(ROOT/'reports/protocol_v67_screen.freeze.json')['sha256'].items():assert sha(ROOT/name)==digest,name
    raw=ROOT/'results/v67_candidates_physical';out=ROOT/'results/v67_candidates_screen';meta=read(raw/'summary.json')
    assert meta['complete_table'] and meta['attempted']==432 and meta['stage_seconds']<=1800
    expected=[]
    for rep in range(3):
        for fi,family in enumerate(['duckdb','gnu_sort','openjpeg']):
            ids=list(range(48));random.Random(67000+1000*rep+fi).shuffle(ids);configs,_=design(family)
            for cid in ids:expected.append({'trial':len(expected),'family':family,'workload':'fixed','round':rep,'config_id':cid,'configuration':list(configs[cid])})
    assert read(raw/'schedule.json')==expected
    rows=read(raw/'all_cases.json');assert len(rows)==432 and rows==[json.loads(x) for x in (raw/'trials.jsonl').read_text().splitlines()]
    answers=reference_answers();sort_hash=hashlib.sha256(b''.join(('%08d\n'%i).encode() for i in range(2**20))).hexdigest();invocations=0;valid=0
    for row,spec in zip(rows,expected):
        assert all(row[k]==v for k,v in spec.items());folder=raw/f"trial_{row['trial']:03d}"
        if row['status']=='valid':invocations+=check_row(row,folder,answers,sort_hash);valid+=1
        else:
            assert row['status']=='resource_noncompletion' and row['objective_ms']==90000
            receipt=read(folder/'supervision.json');assert row['supervision']==receipt
            result=read(folder/'result.json') if (folder/'result.json').exists() else {}
            assert receipt['termination_reason'] in ['wall_timeout','rss_watchdog'] or result.get('error','').startswith(('OutOfMemoryException:','TimeoutError:'))
            invocations+=result.get('program_invocations',0)
        if time.monotonic()-start>180:raise TimeoutError('Verifier cap')
    assert meta['valid']==valid
    summary=read(out/'summary.json');assert summary['arms']==45 and summary['recorded_accesses']==600 and summary['primary_comparator']=='rf_lcb'
    decisions=0;charges=0
    for w in summary['workloads']:
        family=w['family'];configs,x=design(family);folder=out/(family+'_fixed');table=read(folder/'table.json')
        assert len(table)==48 and sha(folder/'table.json')==w['table_sha256']
        for cid,t in enumerate(table):
            records=[r for r in rows if r['family']==family and r['config_id']==cid];values=[r['objective_ms'] for r in records]
            assert sorted(r['round'] for r in records)==[0,1,2] and t['configuration']==list(configs[cid]) and t['values_ms']==values
            eq(t['median_ms'],statistics.median(values));eq(t['cv'],statistics.stdev(values)/statistics.mean(values));assert t['valid_repetitions']==sum(r['status']=='valid' for r in records)
        events=[json.loads(line) for line in (folder/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==200;used=[]
        for i,e in enumerate(events):assert e['event_id']==i and e['value_ms']==table[e['config_id']]['median_ms']
        def check_events(obs,seed,arm,offset):
            for i,o in enumerate(obs):
                e=events[o['source_event_id']];assert e['case']==seed and e['arm']==arm and e['inclusive_step']==offset+i+1
                assert e['config_id']==o['config_id'] and e['value_ms']==o['value_ms'];used.append(e['event_id'])
        def choose(obs,method,seed,rng=None):
            nonlocal decisions
            decisions+=1;ids=[o['config_id'] for o in obs];rem=[j for j in range(48) if j not in ids];y=np.array([o['value_ms'] for o in obs])
            if method=='random':return rng.choice(rem)
            if method=='nn':
                scores=[]
                for candidate in rem:
                    dist=np.abs(x[candidate]-x[ids]).mean(axis=1)
                    neighbors=sorted(range(len(ids)),key=lambda j:(dist[j],j))[:3]
                    scores.append(float(np.mean(y[neighbors])))
            else:
                model=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids)).fit(x[ids],y)
                pred=np.array([tree.predict(x[rem]) for tree in model.estimators_]);scores=pred.mean(axis=0)-pred.std(axis=0)
            return min(zip(scores,rem))[1]
        minimum=min(t['median_ms'] for t in table);eq(w['minimum_ms'],minimum)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3];threshold=max(5.,200*statistics.median(cvs)) if cvs else None
        assert w['threshold_percent']==threshold;hits=0
        assert [c['seed'] for c in w['cases']]==[11,23,37,53,71]
        for c in w['cases']:
            seed=c['seed'];pf=folder/f'prefix_{seed}.json';prefix=read(pf)
            assert len(prefix)==len({o['config_id'] for o in prefix})==10
            assert [o['config_id'] for o in prefix[:4]]==random.Random(seed).sample(range(48),4);check_events(prefix,seed,'prefix',0)
            for n in range(4,10):assert prefix[n]['config_id']==choose(prefix[:n],'nn',seed)
            bests={}
            for method in ['random','nn','rf_lcb']:
                arm=read(folder/f'arm_{seed}_{method}.json');obs=arm['observations']
                assert obs[:10]==prefix and arm['prefix_sha256']==sha(pf) and len(obs)==len({o['config_id'] for o in obs})==20
                check_events(obs[10:],seed,method,10);rng=random.Random(seed+1000)
                for n in range(10,20):assert obs[n]['config_id']==choose(obs[:n],method,seed,rng)
                bests[method]=min(o['value_ms'] for o in obs)
            assert c['best_ms']==bests;eq(c['prefix_best_ms'],min(o['value_ms'] for o in prefix))
            headroom=100*(bests['rf_lcb']-minimum)/bests['rf_lcb'];eq(c['primary_rf_headroom_percent'],headroom)
            eq(c['portfolio_headroom_percent'],100*(min(bests.values())-minimum)/min(bests.values()))
            met=threshold is not None and headroom>=threshold;assert c['gate_met']==met;hits+=met
        assert w['gate_case_count']==hits and w['gate_passed']==(hits>=2) and sorted(used)==list(range(200));charges+=200
    print(json.dumps({'verified':True,'configuration_trials':432,'valid_trials':valid,'application_invocations_with_decoder_validation':invocations,'charged_acquisitions':charges,'reconstructed_choices':decisions,'seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
