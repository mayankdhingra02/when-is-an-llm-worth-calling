"""Frozen live classical paired continuations: 200 charged native evaluations."""
import hashlib,json,math,random,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.rocksdb_v69 import grid
from escalation.classical_java_v54 import choose
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss

def main():
    for name,digest in json.loads((ROOT/'reports/protocol_v71.freeze.json').read_text())['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    rss(-1);out=ROOT/'results/v71_rocksdb_classical';out.mkdir(exist_ok=False)
    configs=grid();x=np.array([[math.log2(c['cache_mib'])/7,(math.log2(c['block_size'])-9)/7,math.log2(c['restart_interval'])/7] for c in configs])
    rows=[];cases=[];started=time.monotonic();stopped=False
    def acquire(cid,obs,seed,arm,purpose="search"):
        if purpose not in ('search','confirmation'):raise ValueError('invalid purpose')
        if purpose=='search' and cid in {o['config_id'] for o in obs}:raise ValueError('duplicate acquisition')
        if len(obs)>=20:raise ValueError('arm budget exceeded')
        if time.monotonic()-started>1650:raise TimeoutError('1800s stage reserve reached')
        if len(rows)>=200:raise ValueError('collection cap')
        folder=out/f'eval_{len(rows):03d}';folder.mkdir();spec={'seed':seed,'arm':arm,'ordinal':len(obs)+1,'config_id':int(cid),'config':configs[cid],'purpose':purpose}
        atomic_json(folder/'spec.json',spec)
        # Charge before launch, including failure. Prefix is physically collected once.
        row={**spec,'status':'intended','path':str(folder.relative_to(ROOT))};rows.append(row)
        with (out/'charges.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        def monitor(pid):
            value=rss(pid);return {'rss_bytes':value},('rss_cap' if value>2*1024**3 else None)
        receipt=run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_rocksdb_v71.py'),str(folder/'spec.json')],cwd=ROOT,log_path=folder/'worker.log',wall_cap=120,monitor=monitor)
        atomic_json(folder/'supervision.json',receipt)
        result=json.loads((folder/'result.json').read_text()) if (folder/'result.json').exists() else {'status':'resource_noncompletion'}
        row.update(status=result['status'],supervision=receipt)
        if receipt['exit_code'] or receipt['termination_reason'] or result['status']!='valid':
            row['status']='failed';atomic_json(out/'acquisitions.json',rows);raise RuntimeError('physical evaluation failed; stop')
        value=result['objective_verified_loop_seconds']*1000
        row['value_ms']=value;atomic_json(out/'acquisitions.json',rows)
        return {'config_id':int(cid),'value_ms':value,'physical_receipt':row['path']}
    try:
        for seed in [11,23,37,53,71]:
            prefix=[]
            for cid in random.Random(seed).sample(range(len(configs)),4):prefix.append(acquire(cid,prefix,seed,'prefix'))
            while len(prefix)<10:prefix.append(acquire(choose(x,prefix,'nn',seed),prefix,seed,'prefix'))
            prefixpath=out/f'prefix_{seed}.json';atomic_json(prefixpath,prefix)
            arms={m:[dict(o) for o in prefix] for m in ['random','nn','rf_lcb']}
            case={'seed':seed,'prefix_sha256':hashlib.sha256(prefixpath.read_bytes()).hexdigest(),'arms':arms,'confirmation':{m:[] for m in arms}};cases.append(case)
            rngs={m:random.Random(seed+1000) for m in arms};order_rng=random.Random(seed+71000)
            for step in range(7):
                order=list(arms);order_rng.shuffle(order)
                for method in order:
                    obs=arms[method];cid=choose(x,obs,method,seed,rngs[method]);obs.append(acquire(cid,obs,seed,method))
                    atomic_json(out/f'case_{seed}.json',case)
            selected={m:min(obs,key=lambda o:o['value_ms'])['config_id'] for m,obs in arms.items()}
            case['selected_config_ids']=selected;atomic_json(out/f'case_{seed}.json',case)
            for repetition in range(3):
                order=list(arms);order_rng.shuffle(order)
                for method in order:
                    confirmed=case['confirmation'][method]
                    confirmed.append(acquire(selected[method],arms[method]+confirmed,seed,method,'confirmation'))
                    atomic_json(out/f'case_{seed}.json',case)
            print('seed',seed,'complete',len(rows),'physical evaluations',flush=True)
    except Exception as exc:
        stopped=True;atomic_json(out/'failure.json',{'error':repr(exc),'charged_evaluations':len(rows)})
    finally:
        atomic_json(out/'summary.json',{'intended_physical_evaluations':200,'charged_evaluations':len(rows),'successful_evaluations':sum(r['status']=='valid' for r in rows),'unattempted':200-len(rows),'complete':not stopped and len(rows)==200,'seconds':time.monotonic()-started,'independent_system_families':1,'new_model_requests':0,'cases':cases})
    if stopped:sys.exit(1)

if __name__=='__main__':main()
