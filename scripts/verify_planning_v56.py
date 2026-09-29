"""Read-only replay of V55/V56 hashes, raw plans, budgets and all choices."""
import hashlib, itertools, json, math, random, re, statistics, sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.planning_v55 import Task

def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def equal(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def main():
    for name in ['v55_planning_feasibility','v56_planning_screen']:
        for p,h in read(ROOT/f'reports/protocol_{name}.freeze.json')['sha256'].items():assert digest(ROOT/p)==h,p
    source=ROOT/'artifacts/sources/v55'
    task=Task((source/'domain.pddl').read_text(),(source/'p05.pddl').read_text())
    old=read(ROOT/'results/v55_planning_feasibility/summary.json')
    for row in old['trials']:
        trial=ROOT/f"results/v55_planning_feasibility/trial_{row['trial']}"
        assert task.validate((trial/'sas_plan').read_text())==row['validation']
        assert digest(trial/'sas_plan')==row['plan_sha256']
    physical=ROOT/'results/v56_planning_physical';out=ROOT/'results/v56_planning_screen'
    meta=read(physical/'summary.json');assert meta['complete_admissible_table']
    rows=[json.loads(line) for line in (physical/'trials.jsonl').read_text().splitlines()]
    assert len(rows)==144 and rows==read(physical/'all_cases.json')
    configs=list(itertools.product(['lmcut','hmax'],['null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'],['true','false'],['low_h','low_g','fifo']))
    schedule=[]
    for rep in range(3):
        ids=list(range(48));random.Random(56000+rep).shuffle(ids)
        schedule.extend((rep,cid) for cid in ids)
    valid=0;table=read(out/'table.json')
    for i,row in enumerate(rows):
        assert (row['round'],row['config_id'])==schedule[i] and row['trial']==i
        assert tuple(row['configuration'])==configs[row['config_id']]
        trial=physical/f'trial_{i:03d}'
        assert row==read(trial/'result.json')
        start=read(trial/'start.json');assert all(row[k]==v for k,v in start.items())
        assert (trial/'output.sas').exists()
        log=(trial/'planner.log').read_text()
        if row['status']=='valid':
            valid+=1
            assert row['exit_code']==0 and 0<row['wall_seconds']<=10
            check=task.validate((trial/'sas_plan').read_text())
            assert check==row['validation'] and check['cost']=='104'
            assert digest(trial/'sas_plan')==row['plan_sha256']
            assert re.findall(r'Plan cost: (\d+)',log)==['104']
            equal(row['penalized_ms'],1000*row['wall_seconds'])
        else:
            assert row['status'] in ['wall_timeout','rss_watchdog','scratch_watchdog','resource_or_unsolved']
            assert row['penalized_ms']==20000
    assert valid==meta['valid']
    for cid,t in enumerate(table):
        entries=[r for r in rows if r['config_id']==cid];values=[r['penalized_ms'] for r in entries]
        assert len(entries)==3 and t['repetition_ms']==values
        equal(t['median_ms'],statistics.median(values))
        equal(t['cv'],statistics.stdev(values)/statistics.mean(values))
        assert t['valid_repetitions']==sum(r['status']=='valid' for r in entries)
    seal=read(out/'table_seal.json');assert seal['sha256']==digest(out/'table.json')
    assert seal['physical_trials_sha256']==digest(physical/'trials.jsonl')
    levels=[['lmcut','hmax'],['null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'],['true','false'],['low_h','low_g','fifo']]
    x=np.asarray([[int(val==level) for val,choices in zip(c,levels) for level in choices] for c in configs])
    journal=[json.loads(s) for s in (out/'acquisitions.jsonl').read_text().splitlines()]
    assert len(journal)==200
    seen_events=[];decisions=0
    def check_events(observations,seed,method):
        for i,o in enumerate(observations):
            ev=journal[o['source_event_id']]
            assert ev['case']==seed and ev['arm']==method and ev['inclusive_step']==(i+1 if method=='prefix' else i+11)
            assert ev['config_id']==o['config_id'] and ev['value_ms']==o['value_ms']==table[o['config_id']]['median_ms']
            seen_events.append(ev['event_id'])
    def next_id(obs,method,seed,rng):
        nonlocal decisions
        decisions+=1
        ids=[o['config_id'] for o in obs];remaining=[i for i in range(48) if i not in ids]
        if method=='random':return rng.choice(remaining)
        y=np.array([o['value_ms'] for o in obs])
        if method=='nn':
            score=[]
            for cid in remaining:
                neighbors=sorted(range(len(ids)),key=lambda j:(np.abs(x[cid]-x[ids[j]]).mean(),j))[:3]
                score.append(float(y[neighbors].mean()))
        else:
            forest=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids))
            forest.fit(x[ids],y);p=np.asarray([t.predict(x[remaining]) for t in forest.estimators_])
            score=p.mean(axis=0)-p.std(axis=0)
        return min(zip(score,remaining))[1]
    summary=read(out/'summary.json');opt=min(t['median_ms'] for t in table)
    cv=[t['cv'] for t in table if t['valid_repetitions']==3]
    noise=100*statistics.median(cv);threshold=max(5,2*noise);hits=0
    for case in summary['cases']:
        seed=case['seed'];pfile=out/f'prefix_{seed}.json';prefix=read(pfile)
        assert len(prefix)==10 and len({o['config_id'] for o in prefix})==10
        assert [o['config_id'] for o in prefix[:4]]==random.Random(seed).sample(range(48),4)
        for n in range(4,10):assert next_id(prefix[:n],'nn',seed,None)==prefix[n]['config_id']
        check_events(prefix,seed,'prefix');bests=[]
        for method in ['random','nn','rf_lcb']:
            arm=read(out/f'arm_{seed}_{method}.json');obs=arm['observations']
            assert arm['prefix_sha256']==digest(pfile) and obs[:10]==prefix
            assert len(obs)==20 and len({o['config_id'] for o in obs})==20
            rng=random.Random(seed+1000)
            for n in range(10,20):assert next_id(obs[:n],method,seed,rng)==obs[n]['config_id']
            check_events(obs[10:],seed,method)
            best=min(o['value_ms'] for o in obs);bests.append(best);equal(best,case['best_ms'][method])
        pb=min(o['value_ms'] for o in prefix);equal(pb,case['prefix_best_ms'])
        equal(case['prefix_headroom_percent'],100*(pb-opt)/pb)
        headroom=100*(min(bests)-opt)/min(bests);equal(headroom,case['portfolio_headroom_percent'])
        assert case['gate_met']==(headroom>=threshold);hits+=headroom>=threshold
    assert sorted(seen_events)==list(range(200))
    equal(summary['table_minimum_ms'],opt);equal(summary['median_configuration_cv_percent'],noise)
    equal(summary['gate_threshold_percent'],threshold)
    assert summary['gate_case_count']==hits and summary['gate_passed']==(hits>=2)
    result={'verified':True,'physical_trials':144,'valid_plans':valid,'feasibility_plans':3,
            'recorded_accesses':200,'arms':15,'reconstructed_choices':decisions,'gate_passed':bool(hits>=2)}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
