"""Verify acquisition lineage/budgets; score only saved complete V58 choices."""
import hashlib,json,random,statistics,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/v58_order_sensitivity'

def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    start=time.monotonic();collection=read(OUT/'collection_summary.json');assert collection['complete']
    for name,h in read(ROOT/'reports/protocol_v58_order_sensitivity.freeze.json')['sha256'].items():assert digest(ROOT/name)==h,name
    assert collection['recorded_accesses']==8000 and collection['completed_cases']==200
    schedule=read(OUT/'schedule.json');assert len(schedule)==40
    global_events=[json.loads(s) for s in (OUT/'acquisitions.jsonl').read_text().splitlines()]
    assert len(global_events)==8000
    sources={f:ROOT/f'results/{folder}' for f,folder in [('javagc','v54_java_screen'),('fastdownward','v56_planning_screen')]}
    cases=[];seen=[];global_offset=0
    for block in schedule:
        f=block['family'];i=block['permutation'];order=block['new_to_source']
        expected=list(range(48));random.Random(58000+i).shuffle(expected);assert order==expected
        table=read(sources[f]/'table.json');old=read(sources[f]/'summary.json')
        minimum=min(r['median_ms'] for r in table);threshold=old['gate_threshold_percent']
        folder=OUT/f'{f}_perm_{i:02d}';events=[json.loads(s) for s in (folder/'acquisitions.jsonl').read_text().splitlines()]
        assert len(events)==200
        for k,e in enumerate(events):
            assert e['event_id']==k and e['value_ms']==table[order[e['config_id']]]['median_ms']
            global_e=global_events[global_offset+k]
            assert global_e=={**e,'event_id':global_offset+k,'block_event_id':k,'family':f,'permutation':i,'source_config_id':order[e['config_id']]}
        used=[]
        def verify_obs(obs,seed,method,offset):
            for n,o in enumerate(obs):
                e=events[o['source_event_id']]
                assert e['config_id']==o['config_id'] and e['value_ms']==o['value_ms']
                assert e['case']==seed and e['arm']==method and e['inclusive_step']==n+offset+1
                used.append(o['source_event_id'])
        for seed in [11,23,37,53,71]:
            pf=folder/f'prefix_{seed}.json';prefix=read(pf)
            assert len(prefix)==10 and len({o['config_id'] for o in prefix})==10
            assert [order[o['config_id']] for o in prefix[:4]]==random.Random(seed).sample(range(48),4)
            verify_obs(prefix,seed,'prefix',0)
            bests={}
            for m in ['random','nn','rf_lcb']:
                arm=read(folder/f'arm_{seed}_{m}.json');obs=arm['observations']
                assert arm['prefix_sha256']==digest(pf) and obs[:10]==prefix
                assert len(obs)==20 and len({o['config_id'] for o in obs})==20
                verify_obs(obs[10:],seed,m,10);bests[m]=min(o['value_ms'] for o in obs)
            bests['prefix']=min(o['value_ms'] for o in prefix)
            headroom={m:100*(v-minimum)/v for m,v in bests.items()}
            portfolio=min(headroom[m] for m in ['random','nn','rf_lcb'])
            cases.append({'family':f,'permutation':i,'seed':seed,'best_ms':bests,'headroom_percent':headroom,'portfolio_headroom_percent':portfolio,'portfolio_gate_met':portfolio>=threshold,'threshold_percent':threshold,'table_minimum_ms':minimum})
        assert sorted(used)==list(range(200));seen.extend(used);global_offset+=200
    families=[]
    for f in sources:
        subset=[c for c in cases if c['family']==f]
        methods={m:{'exact_minimum_count':sum(c['headroom_percent'][m]==0 for c in subset),'median_headroom_percent':statistics.median(c['headroom_percent'][m] for c in subset),'max_headroom_percent':max(c['headroom_percent'][m] for c in subset),'threshold_crossings':sum(c['headroom_percent'][m]>=c['threshold_percent'] for c in subset)} for m in ['prefix','random','nn','rf_lcb']}
        per_permutation=[{'permutation':i,'gate_case_count':sum(c['portfolio_gate_met'] for c in subset if c['permutation']==i)} for i in range(20)]
        families.append({'family':f,'cases':100,'threshold_percent':subset[0]['threshold_percent'],'methods':methods,
                         'permutations_passing_gate':sum(p['gate_case_count']>=2 for p in per_permutation),'permutation_gates':per_permutation,'portfolio_max_headroom_percent':max(c['portfolio_headroom_percent'] for c in subset)})
    result={'scope':'Retrospective exposed-table ID-order sensitivity; not independent-system inference','families':families,'cases':200,'arms':600,'verified_acquisitions':8000,'all_initial_physical_draws_preserved':True,'analysis_seconds':time.monotonic()-start,'collection':collection}
    for name,data in [('cases.json',cases),('summary.json',result)]:
        with (OUT/name).open('x') as fp:json.dump(data,fp,indent=2);fp.write('\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
