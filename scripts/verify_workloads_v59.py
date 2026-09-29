"""Read-only V59 provenance, physical receipts, budgets, decisions and metric replay."""
import hashlib,itertools,json,math,random,re,statistics,sys,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.planning_v55 import Task
from run_java_feasibility_v53 import digest,parse_status

def read(p):return json.loads(p.read_text())
def eq(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)
def main():
    start=time.monotonic();freeze=ROOT/'reports/protocol_v59_workload_screen.freeze.json'
    for name,h in read(freeze)['sha256'].items():assert digest(ROOT/name)==h,name
    approval=read(ROOT/'artifacts/study_v59/approval_receipt.json')
    assert approval['authorized'] and approval['max_physical_trials']==576 and approval['max_stage_seconds']==7200
    assert approval['max_model_requests']==approval['max_external_spend_usd']==0
    assert approval['protocol_freeze_sha256']==digest(freeze)
    physical=ROOT/'results/v59_workload_physical';out=ROOT/'results/v59_workload_screen'
    meta=read(physical/'summary.json');assert meta['complete_table'] and meta['attempted']==576 and meta['unattempted']==0
    rows=read(physical/'all_cases.json');journal=[json.loads(s) for s in (physical/'trials.jsonl').read_text().splitlines()]
    assert len(rows)==576 and rows==journal
    workloads=[('javagc','small'),('fastdownward','p01'),('javagc','large'),('fastdownward','p10')]
    expected=[]
    for rep in range(3):
        for j,(f,w) in enumerate(workloads):
            ids=list(range(48));random.Random(59000+rep*10+j).shuffle(ids)
            expected.extend([{'trial':len(expected)+k,'round':rep,'family':f,'workload':w,'config_id':cid} for k,cid in enumerate(ids)])
    assert expected==read(physical/'schedule.json')
    grids={'javagc':list(itertools.product([1,2,4,8],[1,2,4,8],[2,4,8])),
           'fastdownward':list(itertools.product(['lmcut','hmax'],['null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'],['true','false'],['low_h','low_g','fifo']))}
    expected_java={r['id']:r for r in read(ROOT/'artifacts/study_v57/workload_metadata.json')['workloads'] if r['family']=='javagc'}
    tasks={w:Task((ROOT/'artifacts/sources/v55/domain.pddl').read_text(),(ROOT/f'artifacts/sources/v57/{w}.pddl').read_text()) for w in ['p01','p10']}
    valid=0;plans=0;jvms=0;iterations=0;retained=0
    for row,item in zip(rows,expected):
        assert all(row[k]==v for k,v in item.items())
        assert tuple(row['configuration'])==grids[row['family']][row['config_id']]
        trial=physical/f"trial_{row['trial']:02d}";assert row==read(trial/'result.json')
        receipt=read(trial/'start.json');assert all(row[k]==v for k,v in receipt.items())
        assert digest(trial/'process.log')==row['log_sha256'];log=(trial/'process.log').read_text(errors='replace')
        java=row['family']=='javagc';limit=60 if java else 30
        assert 0<row['wall_seconds']<=row['watchdog_elapsed_seconds']
        if java:
            jvms+=1;parsed=parse_status(log);assert all(row[k]==v for k,v in parsed.items())
            iterations+=int(parsed['warmup_ms'] is not None)+int(parsed['final_ms'] is not None)
        if row['status']=='valid':
            valid+=1;assert row['exit_code']==0 and row['termination_reason'] is None and row['wall_seconds']<=limit
            if java:
                ref=expected_java[row['workload']]
                assert row['reference_output_equal'] and row['success_markers']
                assert row['output_names']==['xalan.out.0']
                assert row['output_bytes']==ref['expected_final_bytes'] and row['output_sha256']==ref['expected_final_sha256']
                assert row['objective_ms']==row['final_ms']
                if row['output_retained']:
                    p=ROOT/row['retained_output_path'];assert digest(p)==row['output_sha256'] and p.stat().st_size==row['output_bytes'];retained+=1
            else:
                plans+=1;p=trial/'sas_plan';v=tasks[row['workload']].validate(p.read_text())
                assert v==row['validation'] and v['cost']=='105' and digest(p)==row['plan_sha256']
                assert re.findall(r'Plan cost: (\d+)',log)==['105'] and re.findall(r'; cost = (\d+) \(',p.read_text())==['105']
                assert (trial/'output.sas').exists();eq(row['objective_ms'],row['wall_seconds']*1000)
        else:
            assert row['status']=='failed'
            assert row['termination_reason'] in ['wall_timeout','rss_watchdog','scratch_watchdog'] or (not java and row['exit_code'] in [20,21,22,23,24])
            assert row['objective_ms']==(120000 if java else 60000)
    assert valid==meta['valid'] and meta['stage_seconds']<=7200
    screen=read(out/'summary.json');assert screen['arms']==60 and screen['recorded_accesses']==800
    decisions=0;charges=0
    for family,workload in workloads:
        folder=out/f'{family}_{workload}';table=read(folder/'table.json')
        selected=[r for r in rows if (r['family'],r['workload'])==(family,workload)]
        assert len(selected)==144 and len(table)==48
        for cid,t in enumerate(table):
            group=[r for r in selected if r['config_id']==cid];values=[r['objective_ms'] for r in group]
            assert len(group)==3 and t['config_id']==cid and tuple(t['configuration'])==grids[family][cid] and t['values_ms']==values
            eq(t['median_ms'],statistics.median(values));eq(t['cv'],statistics.stdev(values)/statistics.mean(values))
            assert t['valid_repetitions']==sum(r['status']=='valid' for r in group)
        events=[json.loads(s) for s in (folder/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==200
        for i,event in enumerate(events):assert event['event_id']==i and event['value_ms']==table[event['config_id']]['median_ms']
        used=[]
        if family=='javagc':x=(np.log2(np.array(grids[family]))-np.array([0.,0.,1.]))/np.array([3.,3.,2.])
        else:
            levels=[['lmcut','hmax'],['null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'],['true','false'],['low_h','low_g','fifo']]
            x=np.array([[int(v==level) for v,choices in zip(c,levels) for level in choices] for c in grids[family]])
        def next_id(obs,method,seed,rng):
            nonlocal decisions
            if time.monotonic()-start>180:raise TimeoutError('Verification180s cap')
            decisions+=1;ids=[o['config_id'] for o in obs];remaining=[i for i in range(48) if i not in ids]
            if method=='random':return rng.choice(remaining)
            y=np.array([o['value_ms'] for o in obs])
            if method=='nn':
                scores=[]
                for cid in remaining:
                    near=sorted(range(len(ids)),key=lambda j:(float(np.abs(x[cid]-x[ids[j]]).mean()),j))[:3]
                    scores.append(float(y[near].mean()))
            else:
                forest=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids))
                forest.fit(x[ids],y);pred=np.array([tree.predict(x[remaining]) for tree in forest.estimators_]);scores=pred.mean(axis=0)-pred.std(axis=0)
            return min(zip(scores,remaining))[1]
        def check_events(obs,seed,arm,offset):
            for i,o in enumerate(obs):
                e=events[o['source_event_id']]
                assert e['case']==seed and e['arm']==arm and e['inclusive_step']==offset+i+1
                assert o['config_id']==e['config_id'] and o['value_ms']==e['value_ms'];used.append(e['event_id'])
        result=next(w for w in screen['workloads'] if (w['family'],w['workload'])==(family,workload))
        assert result['table_sha256']==digest(folder/'table.json')
        minimum=min(t['median_ms'] for t in table);eq(result['minimum_ms'],minimum)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3];threshold=max(5,200*statistics.median(cvs)) if cvs else None
        assert result['threshold_percent']==threshold;hits=0
        for case in result['cases']:
            seed=case['seed'];pf=folder/f'prefix_{seed}.json';prefix=read(pf)
            assert len(prefix)==10 and len({o['config_id'] for o in prefix})==10
            assert [o['config_id'] for o in prefix[:4]]==random.Random(seed).sample(range(48),4)
            check_events(prefix,seed,'prefix',0)
            for n in range(4,10):assert prefix[n]['config_id']==next_id(prefix[:n],'nn',seed,None)
            bests=[]
            for method in ['random','nn','rf_lcb']:
                arm=read(folder/f'arm_{seed}_{method}.json');obs=arm['observations']
                assert arm['prefix_sha256']==digest(pf) and obs[:10]==prefix and len(obs)==20 and len({o['config_id'] for o in obs})==20
                check_events(obs[10:],seed,method,10);rng=random.Random(seed+1000)
                for n in range(10,20):assert obs[n]['config_id']==next_id(obs[:n],method,seed,rng)
                best=min(o['value_ms'] for o in obs);eq(case['best_ms'][method],best);bests.append(best)
            eq(case['prefix_best_ms'],min(o['value_ms'] for o in prefix))
            headroom=100*(min(bests)-minimum)/min(bests);eq(case['portfolio_headroom_percent'],headroom)
            met=threshold is not None and headroom>=threshold;assert case['gate_met']==met;hits+=met
        assert result['gate_case_count']==hits and result['gate_passed']==(hits>=2)
        assert sorted(used)==list(range(200));charges+=len(used)
    print(json.dumps({'verified':True,'physical_trials':576,'valid_trials':valid,'valid_plans':plans,'java_invocations':jvms,'java_completed_iterations':iterations,'retained_java_outputs':retained,'charged_acquisitions':charges,'arms':60,'reconstructed_choices':decisions,'runtime_seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
