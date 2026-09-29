"""Independent V60/V61 receipt, known-answer, accounting and policy replay."""
import hashlib,itertools,json,math,random,re,statistics,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)
def main():
    start=time.monotonic()
    for version in [60,61]:
        for n,h in read(ROOT/f'reports/protocol_v{version}_redis.freeze.json')['sha256'].items():assert digest(ROOT/n)==h,n
    h=hashlib.sha256()
    for k in range(256):
        h.update(('v60:%012d'%k).encode())
        for f in range(128):h.update(('f%03d'%f).encode());h.update(('field-%03d-'%f+'x'*64).encode()[:64])
    expected={'keys':256,'fields_per_key':128,'total_values':32768,'sha256':h.hexdigest()}
    raw=ROOT/'results/v61_redis_physical';screen=ROOT/'results/v61_redis_screen'
    v60=ROOT/'results/v60_redis_feasibility'
    total=0;queries=0;max_rss=0;encodings={}
    for physical,intended in [(v60,6),(raw,480)]:
        rows=read(physical/'all_cases.json');journal=[json.loads(s) for s in (physical/'trials.jsonl').read_text().splitlines()]
        assert rows==journal and len(rows)==intended
        schedule=read(physical/'schedule.json');summary=read(physical/'summary.json');assert summary['attempted']==intended
        for row,spec in zip(rows,schedule):
            assert all(row[k]==v for k,v in spec.items())
            trial=physical/f"trial_{row['trial']:02d}";assert read(trial/'result.json')==row and read(trial/'start.json')==spec
            max_rss=max(max_rss,row['sampled_maxima'].get('rss_bytes',0))
            if row['status']!='valid':
                assert physical==raw and row['termination_reason'] in ['wall_timeout','rss_watchdog'] and row['objective_ms']==80000
                continue
            m=read(trial/'measurement.json');assert digest(trial/'measurement.json')==row['measurement_sha256']
            assert row['exit_code']==m['server_exit_code']==0 and row['termination_reason'] is None
            assert m['before']==m['after']==expected and m['status']=='valid'
            assert 'redis_version:7.2.11' in m['server_info']
            encodings[m['encoding']]=encodings.get(m['encoding'],0)+1
            command=m['server_command'];assert command[command.index('--port')+1]=='0' and command[command.index('--save')+1]==''
            assert command[command.index('--appendonly')+1]=='no'
            for k,v in spec['configuration'].items():assert command[command.index('--'+k)+1]==str(v)
            assert len(m['phases'])==2
            for phase,number in zip(m['phases'],[10000,100000]):
                logfile=trial/(phase['phase']+'.log');assert digest(logfile)==phase['log_sha256']
                text=logfile.read_text();counts=re.findall(r'V60_VALIDATED_REPLIES=(\d+)',text)
                assert counts==[str(phase['validated_replies'])] and 'V60_REPLY_MISMATCH' not in text
                assert number==phase['requested'] and number<=phase['validated_replies']<=number+800
                cmd=phase['command'];assert cmd[-3:]==['HGET','v60:__rand_int__','f%03d'%spec['field_index']]
                for option,val in [('-n',str(number)),('-c','50'),('-P','16'),('-r','256'),('--seed','60000'),('--threads','1')]:assert cmd[cmd.index(option)+1]==val
                queries+=phase['validated_replies']
            eq(row['objective_ms'],1000*m['phases'][1]['wall_seconds']);total+=1
        assert summary['valid']==sum(r['status']=='valid' for r in rows)
    # Independently reconstruct the configuration grid and randomized physical schedule.
    keys=['hash-max-listpack-entries','hash-max-listpack-value','io-threads','io-threads-do-reads','hz','activerehashing']
    configs=[dict(zip(keys,[a,b,t,r,h,z])) for a,b,(t,r),h,z in itertools.product([64,512],[32,64],[(1,'no'),(2,'no'),(2,'yes'),(4,'no'),(4,'yes')],[10,100],['no','yes'])]
    expected_schedule=[]
    for rep in range(3):
        for q in [0,127]:
            ids=list(range(80));random.Random(61000+rep*1000+q).shuffle(ids)
            for cid in ids:expected_schedule.append({'trial':len(expected_schedule),'round':rep,'family':'redis','workload':f'hget_{q}','field_index':q,'config_id':cid,'configuration':configs[cid]})
    assert expected_schedule==read(raw/'schedule.json')
    rows=read(raw/'all_cases.json');s=read(screen/'summary.json');assert s['arms']==30 and s['recorded_accesses']==400 and s['primary_comparator']=='rf_lcb'
    x=np.array([[(math.log2(c[keys[0]])-6)/3,math.log2(c[keys[1]])-5,math.log2(c[keys[2]])/2,int(c[keys[3]]=='yes'),(c[keys[4]]-10)/90,int(c[keys[5]]=='yes')] for c in configs])
    decisions=0;charges=0
    for w in s['workloads']:
        folder=screen/('redis_'+w['workload']);table=read(folder/'table.json');assert len(table)==80 and digest(folder/'table.json')==w['table_sha256']
        for cid,item in enumerate(table):
            raw_values=[r for r in rows if r['workload']==w['workload'] and r['config_id']==cid]
            vals=[r['objective_ms'] for r in raw_values];assert len(vals)==3
            assert item['configuration']==configs[cid] and item['values_ms']==vals and item['config_id']==cid
            eq(item['median_ms'],statistics.median(vals));eq(item['cv'],statistics.stdev(vals)/statistics.mean(vals))
            assert item['valid_repetitions']==sum(r['status']=='valid' for r in raw_values)
        events=[json.loads(line) for line in (folder/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==200
        for i,e in enumerate(events):assert e['event_id']==i and e['value_ms']==table[e['config_id']]['median_ms']
        used=[]
        def check(obs,seed,arm,offset):
            for i,o in enumerate(obs):
                e=events[o['source_event_id']];assert e['case']==seed and e['arm']==arm and e['inclusive_step']==offset+i+1
                assert e['config_id']==o['config_id'] and e['value_ms']==o['value_ms'];used.append(e['event_id'])
        def choice(obs,method,seed,rng=None):
            nonlocal decisions
            if time.monotonic()-start>180:raise TimeoutError('Verification cap')
            decisions+=1;ids=[o['config_id'] for o in obs];rem=[j for j in range(80) if j not in ids];y=np.array([o['value_ms'] for o in obs])
            if method=='random':return rng.choice(rem)
            if method=='nn':
                scores=[float(np.mean([y[j] for j in sorted(range(len(ids)),key=lambda j:(float(np.mean(abs(x[k]-x[ids[j]]))),j))[:3]])) for k in rem]
            else:
                model=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids)).fit(x[ids],y)
                preds=np.array([tree.predict(x[rem]) for tree in model.estimators_]);scores=preds.mean(axis=0)-preds.std(axis=0)
            return min(zip(scores,rem))[1]
        minimum=min(t['median_ms'] for t in table);eq(w['minimum_ms'],minimum)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3];threshold=max(5.,200*statistics.median(cvs)) if cvs else None
        assert w['threshold_percent']==threshold;hits=0
        assert [c['seed'] for c in w['cases']]==[11,23,37,53,71]
        for c in w['cases']:
            seed=c['seed'];pf=folder/f'prefix_{seed}.json';p=read(pf);assert len(p)==10 and len({o['config_id'] for o in p})==10
            assert [o['config_id'] for o in p[:4]]==random.Random(seed).sample(range(80),4);check(p,seed,'prefix',0)
            for n in range(4,10):assert p[n]['config_id']==choice(p[:n],'nn',seed)
            bests={}
            for method in ['random','nn','rf_lcb']:
                a=read(folder/f'arm_{seed}_{method}.json');obs=a['observations'];assert obs[:10]==p and a['prefix_sha256']==digest(pf)
                assert len(obs)==20 and len({o['config_id'] for o in obs})==20;check(obs[10:],seed,method,10)
                rng=random.Random(seed+1000)
                for n in range(10,20):assert obs[n]['config_id']==choice(obs[:n],method,seed,rng)
                bests[method]=min(o['value_ms'] for o in obs)
            assert c['best_ms']==bests;eq(c['prefix_best_ms'],min(o['value_ms'] for o in p))
            primary=100*(bests['rf_lcb']-minimum)/bests['rf_lcb'];portfolio=100*(min(bests.values())-minimum)/min(bests.values())
            eq(c['primary_rf_headroom_percent'],primary);eq(c['portfolio_headroom_percent'],portfolio)
            met=threshold is not None and primary>=threshold;assert c['gate_met']==met;hits+=met
        assert w['gate_case_count']==hits and w['gate_passed']==(hits>=2)
        assert sorted(used)==list(range(200));charges+=200
    assert read(raw/'summary.json')['stage_seconds']<=900
    print(json.dumps({'verified':True,'valid_physical_trials_v60_v61':total,'validated_benchmark_replies':queries,'max_sampled_rss_bytes':max_rss,'encodings':encodings,'charged_acquisitions':charges,'reconstructed_choices':decisions,'runtime_seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
