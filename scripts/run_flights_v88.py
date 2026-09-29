"""Bounded CC0 real-data setup/collection; no model calls or TPC components."""
import argparse,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.flights_v88 import CONFIGS
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss
ART=ROOT/'artifacts/study_v88';DATA=ROOT/'data/flights_v88';RAW=ROOT/'results/v88_flights_feasibility'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def monitor(pid):
    memory=rss(pid);scratch=sum(p.stat().st_size for d in [DATA,RAW] if d.exists() for p in d.rglob('*') if p.is_file())
    return {'rss_bytes':memory,'scratch_bytes':scratch},'rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>1024**3 else None

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','freeze','run']);a=p.parse_args()
    if a.stage=='prepare':
        rss(-1);assert not (ART/'preparation.json').exists()
        cmd=[sys.executable,str(ROOT/'scripts/worker_flights_v88.py'),'--prepare'];receipt=run(cmd,cwd=ROOT,log_path=ART/'preparation.log',wall_cap=180,monitor=monitor);write(ART/'preparation.json',{'command':cmd,**receipt,'objective_evaluations':0});assert receipt['exit_code']==0 and receipt['termination_reason'] is None;return
    if a.stage=='freeze':
        assert read(ART/'preparation.json')['exit_code']==0;f=ROOT/'reports/protocol_v88.freeze.json';assert not f.exists()
        names=['reports/protocol_v88.md','scripts/run_flights_v88.py','scripts/worker_flights_v88.py','scripts/fetch_flights_v88.py','scripts/extract_flights_v88.py','scripts/analyze_flights_v88.py','src/escalation/flights_v88.py','src/escalation/bounded_process_v57.py','scripts/run_planning_v55.py','tests/synthetic/test_flights_v88.py','data/flights_v88/query_contract.json','data/flights_v88/flights.duckdb','artifacts/study_v88/data_manifest.json']
        paths=[ROOT/n for n in names];paths.extend(p for p in DATA.rglob('*.csv'));paths.append(ART/'data_extraction.json');paths.extend(p for p in (ROOT/'.local-runtime/duckdb-v87').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
        write(f,{'scope':'9 native classical feasibility trials; no model or held-out claim','at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}});return
    rss(-1);freeze=read(ROOT/'reports/protocol_v88.freeze.json')
    for n,d in freeze['sha256'].items():assert sha(ROOT/n)==d,n
    RAW.mkdir(exist_ok=False);start=time.monotonic();rows=[];stop=None
    try:
        for rep in range(3):
            for i in [(rep+j)%3 for j in range(3)]:
                assert len(rows)<9 and time.monotonic()-start<830
                folder=RAW/f'trial_{len(rows):02d}';folder.mkdir();cmd=[sys.executable,str(ROOT/'scripts/worker_flights_v88.py'),'--config',str(i),'--out',str(folder)]
                row={'trial':len(rows),'repetition':rep,'configuration_index':i,'configuration':CONFIGS[i],'status':'charged','command':cmd,'at_unix':time.time()};rows.append(row);write(folder/'charge.json',row);write(RAW/'acquisitions.json',rows)
                receipt=run(cmd,cwd=ROOT,log_path=folder/'process.log',wall_cap=60,monitor=monitor);row['process']=receipt;write(folder/'process_receipt.json',receipt)
                assert receipt['exit_code']==0 and receipt['termination_reason'] is None
                row['result']=read(folder/'result.json');assert row['result']['configuration']==CONFIGS[i] and row['result']['checked_queries']==57 and row['result']['scored_queries']==48
                row['status']='valid';write(RAW/'acquisitions.json',rows);print('validated',row['trial'],CONFIGS[i]['name'],flush=True)
    except Exception as e:
        stop=repr(e)
        if rows and rows[-1]['status']=='charged':rows[-1].update(status='failed',error=stop)
        write(RAW/'failure.json',{'error':stop})
    finally:
        write(RAW/'acquisitions.json',rows);write(RAW/'summary.json',{'intended_trials':9,'charged_trials':len(rows),'valid_trials':sum(r['status']=='valid' for r in rows),'failed_trials':sum(r['status']=='failed' for r in rows),'unattempted_trials':9-len(rows),'seconds':time.monotonic()-start,'stop_reason':stop,'complete':stop is None and len(rows)==9,'new_model_calls':0})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
