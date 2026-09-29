"""Bounded setup/collection; no model adapter and no implicit EULA grant."""
import argparse,gzip,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.duckdb_v87 import CONFIGS,authorize
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss
from fetch_duckdb_v87 import fetch
ART=ROOT/'artifacts/study_v87';DATA=ROOT/'data/duckdb_v87';RAW=ROOT/'results/v87_duckdb_feasibility'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def permission():
    p=ART/'eula_approval.json';authorize(read(p) if p.exists() else None,(ROOT/'artifacts/sources/v87/DBGEN_LICENSE').read_bytes())
def monitor(pid):
    memory=rss(pid);scratch=sum(p.stat().st_size for d in [DATA,RAW] if d.exists() for p in d.rglob('*') if p.is_file())
    return {'rss_bytes':memory,'scratch_bytes':scratch},'rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>1024**3 else None

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['install-extension','prepare','freeze','run']);a=p.parse_args();permission()
    if a.stage=='install-extension':
        compressed=fetch('https://extensions.duckdb.org/v1.4.4/osx_arm64/tpch.duckdb_extension.gz','tpch.duckdb_extension.gz',32*1024**2)
        dst=ROOT/'.local-runtime/duckdb-v87-tpch.duckdb_extension';assert not dst.exists()
        with gzip.open(compressed,'rb') as r,dst.open('xb') as w:
            total=0
            while True:
                b=r.read(65536)
                if not b:break
                total+=len(b);assert total<=128*1024**2;w.write(b)
        write(ART/'extension.json',{'url':'https://extensions.duckdb.org/v1.4.4/osx_arm64/tpch.duckdb_extension.gz','compressed_sha256':sha(compressed),'binary_sha256':sha(dst),'bytes':total,'signature_validation':'required by DuckDB default at LOAD; not yet executed'});return
    if a.stage=='prepare':
        rss(-1);assert not (ART/'preparation.json').exists()
        cmd=[sys.executable,str(ROOT/'scripts/worker_duckdb_v87.py'),'--prepare'];receipt=run(cmd,cwd=ROOT,log_path=ART/'preparation.log',wall_cap=180,monitor=monitor);write(ART/'preparation.json',{'command':cmd,**receipt,'objective_evaluations':0});assert receipt['exit_code']==0 and receipt['termination_reason'] is None;return
    if a.stage=='freeze':
        assert read(ART/'preparation.json')['exit_code']==0;f=ROOT/'reports/protocol_v87.freeze.json';assert not f.exists()
        names=['reports/protocol_v87_admission.md','scripts/run_duckdb_v87.py','scripts/worker_duckdb_v87.py','scripts/fetch_duckdb_v87.py','scripts/analyze_duckdb_v87.py','src/escalation/duckdb_v87.py','src/escalation/bounded_process_v57.py','scripts/run_planning_v55.py','tests/synthetic/test_duckdb_v87.py','data/duckdb_v87/query_contract.json','data/duckdb_v87/tpch_sf01.duckdb','artifacts/study_v87/data_manifest.json','artifacts/study_v87/extension.json','.local-runtime/duckdb-v87-tpch.duckdb_extension']
        paths=[ROOT/n for n in names];paths.extend(p for p in (ROOT/'.local-runtime/duckdb-v87').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
        write(f,{'scope':'9 native classical feasibility trials; no model or held-out claim','at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}});return
    rss(-1);freeze=read(ROOT/'reports/protocol_v87.freeze.json')
    for n,d in freeze['sha256'].items():assert sha(ROOT/n)==d,n
    RAW.mkdir(exist_ok=False);write(RAW/'authorization.json',read(ART/'eula_approval.json'));start=time.monotonic();rows=[];stop=None
    try:
        for rep in range(3):
            for i in [(rep+j)%3 for j in range(3)]:
                assert len(rows)<9 and time.monotonic()-start<830
                folder=RAW/f'trial_{len(rows):02d}';folder.mkdir();cmd=[sys.executable,str(ROOT/'scripts/worker_duckdb_v87.py'),'--config',str(i),'--out',str(folder)]
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
