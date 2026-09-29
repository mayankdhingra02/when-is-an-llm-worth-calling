"""Replay settings, outcomes, budget and every decision without querying a DB."""
import hashlib,json,math,random,struct,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.rocksdb_v69 import grid
from escalation.rocksdb_binding_v69 import active_readback
from escalation.classical_java_v54 import choose

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def verify():
    start=time.monotonic()
    for stage in [70,71]:
        for n,h in read(ROOT/f'reports/protocol_v{stage}.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    out=ROOT/'results/v71_rocksdb_classical';summary=read(out/'summary.json');assert summary['complete']
    configs=grid();x=np.array([[math.log2(c['cache_mib'])/7,(math.log2(c['block_size'])-9)/7,math.log2(c['restart_interval'])/7] for c in configs])
    charges=[json.loads(line) for line in (out/'charges.jsonl').read_text().splitlines()]
    acquisitions=read(out/'acquisitions.json');assert len(charges)==len(acquisitions)==200
    blob=(ROOT/'data/generated_v69/values.bin').read_bytes();trace=list(struct.iter_unpack('<I',(ROOT/'data/generated_v69/trace.bin').read_bytes()))
    digest=hashlib.sha256()
    for (i,) in trace[10000:]:digest.update(blob[1000*i:1000*(i+1)])
    response_hash=digest.hexdigest();h=hashlib.sha256()
    for i in sorted(range(65536),key=lambda i:('user'+str(i)).encode()):
        h.update(('user'+str(i)).encode());h.update(blob[1000*i:1000*(i+1)])
    scan_hash=h.hexdigest();by_event={}
    # Include corrected feasibility, excluding all invalid old V69 timings.
    folders=list((ROOT/'results/v70_rocksdb_feasibility').glob('trial_*'))+[ROOT/r['path'] for r in acquisitions]
    for folder in folders:
        spec=read(folder/'spec.json');result=read(folder/'result.json');supervision=read(folder/'supervision.json')
        assert result['status']=='valid' and supervision['exit_code']==0 and supervision['termination_reason'] is None
        assert supervision['wall_seconds']<=120 and supervision['sampled_maxima']['rss_bytes']<=2*1024**3
        active_readback(folder/'db',spec['config'])
        assert read(folder/'warmup.json')['cache_usage_bytes']>0
        assert result['timed_response_sha256']==response_hash
        assert result['successful_timed_reads']==result['verified_timed_reads']==100000
        for phase in ['initial_validation','final_validation']:
            assert result[phase]=={'records':65536,'sha256_in_engine_key_order':scan_hash}
        timed=read(folder/'timed.json');assert timed['objective_verified_loop_seconds']==result['objective_verified_loop_seconds']
        assert timed['timed_response_sha256']==response_hash
        if folder.name.startswith('eval_'):
            assert result['data_files_retained'] is False
            inventory=read(folder/'database_file_inventory.json')
            for p in (folder/'db').iterdir():assert sha(p)==inventory[p.name]['sha256'],str(p)
    position=0;decisions=0
    def take(seed,arm,ordinal,cid,purpose):
        nonlocal position
        charge=charges[position];row=acquisitions[position];folder=ROOT/row['path'];result=read(folder/'result.json')
        assert charge['seed']==seed and charge['arm']==arm and charge['ordinal']==ordinal and charge['purpose']==purpose
        assert charge['config_id']==int(cid) and charge['config']==configs[cid]
        assert row['value_ms']==result['objective_verified_loop_seconds']*1000
        position+=1
        return {'config_id':int(cid),'value_ms':row['value_ms'],'physical_receipt':row['path']}
    for seed in [11,23,37,53,71]:
        prefix=[]
        for cid in random.Random(seed).sample(range(512),4):prefix.append(take(seed,'prefix',len(prefix)+1,cid,'search'));decisions+=1
        while len(prefix)<10:
            cid=choose(x,prefix,'nn',seed);prefix.append(take(seed,'prefix',len(prefix)+1,cid,'search'));decisions+=1
        assert prefix==read(out/f'prefix_{seed}.json')
        case=read(out/f'case_{seed}.json');assert case['prefix_sha256']==sha(out/f'prefix_{seed}.json')
        arms={m:[dict(o) for o in prefix] for m in ['random','nn','rf_lcb']}
        rngs={m:random.Random(seed+1000) for m in arms};order_rng=random.Random(seed+71000)
        for step in range(7):
            order=list(arms);order_rng.shuffle(order)
            for m in order:
                cid=choose(x,arms[m],m,seed,rngs[m]);arms[m].append(take(seed,m,len(arms[m])+1,cid,'search'));decisions+=1
        assert case['arms']==arms
        selected={m:min(obs,key=lambda o:o['value_ms'])['config_id'] for m,obs in arms.items()}
        assert case['selected_config_ids']==selected
        confirm={m:[] for m in arms}
        for rep in range(3):
            order=list(arms);order_rng.shuffle(order)
            for m in order:confirm[m].append(take(seed,m,18+rep,selected[m],'confirmation'))
        assert confirm==case['confirmation']
        for m in arms:
            assert len(arms[m])==17 and len({o['config_id'] for o in arms[m]})==17
            assert len(arms[m])+len(confirm[m])==20
    assert position==200 and decisions==155
    assert not list((ROOT/'.scratch-v71').iterdir())
    return {'verified':True,'new_physical_trials_verified':203,'classical_charges':200,'search_decisions_replayed':decisions,'confirmation_charges':45,'arms':15,'logical_arm_evaluations':300,'independent_system_families':1,'new_database_queries':0,'new_model_requests':0,'seconds':time.monotonic()-start}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
