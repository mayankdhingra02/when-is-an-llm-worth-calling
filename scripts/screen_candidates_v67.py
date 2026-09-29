"""One-shot V67 primary RF-LCB screen, fixed before application grid timings."""
import hashlib,json,random,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.classical_java_v54 import RecordedOracle,choose
from escalation.candidate_screen_v67 import encode as candidate_encode

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    start=time.monotonic()
    for name,h in read(ROOT/'reports/protocol_v67_screen.freeze.json')['sha256'].items():assert digest(ROOT/name)==h,name
    physical=ROOT/'results/v67_candidates_physical';meta=read(physical/'summary.json');assert meta['complete_table'] and meta['attempted']==432
    rows=read(physical/'all_cases.json');out=ROOT/'results/v67_candidates_screen';out.mkdir(exist_ok=False)
    all_cases=[];workloads=[];total_events=0
    for family,workload in [('duckdb','fixed'),('gnu_sort','fixed'),('openjpeg','fixed')]:
        if time.monotonic()-start>175:raise TimeoutError('Offline180s cap')
        selected=[r for r in rows if r['family']==family and r['workload']==workload]
        assert len(selected)==144
        folder=out/f'{family}_{workload}';folder.mkdir();table=[]
        for cid in range(48):
            entries=[r for r in selected if r['config_id']==cid];assert sorted(r['round'] for r in entries)==[0,1,2]
            values=[r['objective_ms'] for r in entries]
            table.append({'config_id':cid,'configuration':entries[0]['configuration'],'median_ms':statistics.median(values),'values_ms':values,'valid_repetitions':sum(r['status']=='valid' for r in entries),'cv':statistics.stdev(values)/statistics.mean(values)})
        write(folder/'table.json',table)
        oracle=RecordedOracle([r['median_ms'] for r in table]);configs=[r['configuration'] for r in table]
        x=candidate_encode(family,configs)
        for seed in [11,23,37,53,71]:
            if time.monotonic()-start>180:raise TimeoutError('Offline180s cap')
            prefix=[]
            for cid in random.Random(seed).sample(range(48),4):prefix.append(oracle.acquire(cid,prefix,seed,'prefix'))
            while len(prefix)<10:prefix.append(oracle.acquire(choose(x,prefix,'nn',seed),prefix,seed,'prefix'))
            pf=folder/f'prefix_{seed}.json';write(pf,prefix);arms={}
            for method in ['random','nn','rf_lcb']:
                obs=[dict(o) for o in prefix];rng=random.Random(seed+1000)
                while len(obs)<20:obs.append(oracle.acquire(choose(x,obs,method,seed,rng),obs,seed,method))
                write(folder/f'arm_{seed}_{method}.json',{'prefix_sha256':digest(pf),'observations':obs});arms[method]=obs
            all_cases.append({'family':family,'workload':workload,'seed':seed,'prefix':prefix,'arms':arms})
        assert len(oracle.events)==200;total_events+=200
        (folder/'acquisitions.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in oracle.events))
        workloads.append({'family':family,'workload':workload,'table':table,'folder':folder.name})
    # Full-table scoring only after every workload's saved decisions.
    results=[]
    for w in workloads:
        valid_cv=[r['cv'] for r in w['table'] if r['valid_repetitions']==3]
        threshold=max(5.,200*statistics.median(valid_cv)) if valid_cv else None
        minimum=min(r['median_ms'] for r in w['table']);cases=[]
        for c in all_cases:
            if (c['family'],c['workload'])!=(w['family'],w['workload']):continue
            bests={m:min(o['value_ms'] for o in obs) for m,obs in c['arms'].items()}
            pb=min(o['value_ms'] for o in c['prefix']);portfolio=min(bests.values());primary=bests['rf_lcb'];hr=100*(primary-minimum)/primary
            cases.append({'seed':c['seed'],'prefix_best_ms':pb,'best_ms':bests,'primary_rf_headroom_percent':hr,'portfolio_headroom_percent':100*(portfolio-minimum)/portfolio,'gate_met':threshold is not None and hr>=threshold})
        results.append({'family':w['family'],'workload':w['workload'],'minimum_ms':minimum,'threshold_percent':threshold,'gate_case_count':sum(c['gate_met'] for c in cases),'gate_passed':sum(c['gate_met'] for c in cases)>=2,'cases':cases,'table_sha256':digest(out/w['folder']/'table.json')})
    assert total_events==600
    write(out/'summary.json',{'workloads':results,'independent_families':3,'primary_comparator':'rf_lcb','arms':45,'recorded_accesses':600,'runtime_seconds':time.monotonic()-start,'model_requests':0})
if __name__=='__main__':main()
