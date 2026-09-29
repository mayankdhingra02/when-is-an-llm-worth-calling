"""One-shot hidden-label-isolated replay of exposed tables under fixed ID permutations."""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.classical_java_v54 import RecordedOracle,choose,encode as java_encode
from escalation.classical_planning_v56 import encode as planning_encode
OUT=ROOT/'results/v58_order_sensitivity'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    seal=json.loads((ROOT/'reports/protocol_v58_order_sensitivity.freeze.json').read_text())
    for name,h in seal['sha256'].items():assert digest(ROOT/name)==h,name
    tables={f:json.loads((ROOT/f'results/{folder}/table.json').read_text()) for f,folder in [('javagc','v54_java_screen'),('fastdownward','v56_planning_screen')]}
    OUT.mkdir(exist_ok=False)
    schedule=[]
    for i in range(20):
        order=list(range(48));random.Random(58000+i).shuffle(order)
        for family in ['javagc','fastdownward']:schedule.append({'permutation':i,'family':family,'new_to_source':order})
    write(OUT/'schedule.json',schedule)
    start=time.monotonic();global_events=[];case_count=0;stopped=False
    for block in schedule:
        if time.monotonic()-start>175:stopped=True;break
        family=block['family'];order=block['new_to_source'];inv={source:new for new,source in enumerate(order)}
        table=tables[family]
        configs=[r['configuration'] for r in table]
        x=(java_encode(configs) if family=='javagc' else planning_encode(configs))[order]
        oracle=RecordedOracle([table[i]['median_ms'] for i in order])
        folder=OUT/f"{family}_perm_{block['permutation']:02d}";folder.mkdir()
        for seed in [11,23,37,53,71]:
            if time.monotonic()-start>180:stopped=True;break
            prefix=[]
            for source_id in random.Random(seed).sample(range(48),4):
                prefix.append(oracle.acquire(inv[source_id],prefix,seed,'prefix'))
            while len(prefix)<10:prefix.append(oracle.acquire(choose(x,prefix,'nn',seed),prefix,seed,'prefix'))
            pfile=folder/f'prefix_{seed}.json';write(pfile,prefix)
            for method in ['random','nn','rf_lcb']:
                obs=[dict(o) for o in prefix];rng=random.Random(seed+1000)
                while len(obs)<20:obs.append(oracle.acquire(choose(x,obs,method,seed,rng),obs,seed,method))
                write(folder/f'arm_{seed}_{method}.json',{'prefix_sha256':digest(pfile),'observations':obs})
            case_count+=1
        for event in oracle.events:
            assert len(global_events)<8000
            global_events.append({**event,'event_id':len(global_events),'block_event_id':event['event_id'],'family':family,'permutation':block['permutation'],'source_config_id':order[event['config_id']]})
        (folder/'acquisitions.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in oracle.events))
        print(family,block['permutation'],len(oracle.events),flush=True)
        if stopped:break
    (OUT/'acquisitions.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in global_events))
    write(OUT/'collection_summary.json',{'intended_cases':200,'completed_cases':case_count,'arms':case_count*3,'recorded_accesses':len(global_events),'runtime_seconds':time.monotonic()-start,'complete':not stopped and case_count==200,'model_requests':0,'new_physical_trials':0,'external_spend_usd':0})
if __name__=='__main__':main()
