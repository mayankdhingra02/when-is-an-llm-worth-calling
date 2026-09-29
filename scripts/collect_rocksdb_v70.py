"""Exactly three bounded physical feasibility attempts; no LLM or optimizer."""
import hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss

if __name__=='__main__':
    freeze=json.loads((ROOT/'reports/protocol_v70.freeze.json').read_text())
    for name,digest in freeze['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    rss(-1)
    out=ROOT/'results/v70_rocksdb_feasibility';out.mkdir(exist_ok=False)
    schedule=[{'cache_mib':8,'block_size':4096,'restart_interval':16},
              {'cache_mib':1,'block_size':65536,'restart_interval':1},
              {'cache_mib':8,'block_size':4096,'restart_interval':16}]
    start=time.monotonic();rows=[];failed=False
    for trial,config in enumerate(schedule):
        if failed or time.monotonic()-start>470:
            rows.append({'trial':trial,'config':config,'status':'unattempted'});continue
        folder=out/f'trial_{trial}';folder.mkdir();spec=folder/'spec.json';spec.write_text(json.dumps({'trial':trial,'config':config},indent=2)+'\n')
        def monitor(pid):
            value=rss(pid);return {'rss_bytes':value},('rss_cap' if value>2*1024**3 else None)
        receipt=run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_rocksdb_v70.py'),str(spec)],cwd=ROOT,log_path=folder/'worker.log',wall_cap=120,monitor=monitor)
        (folder/'supervision.json').write_text(json.dumps(receipt,indent=2)+'\n')
        result=json.loads((folder/'result.json').read_text()) if (folder/'result.json').exists() else {'status':'resource_noncompletion'}
        if receipt['exit_code'] or receipt['termination_reason']:result['status']='failed'
        row={'trial':trial,'config':config,**result,'supervision':receipt};rows.append(row)
        failed=row['status']!='valid'
        with (out/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(trial,row['status'],flush=True)
    summary={'intended':3,'attempted':sum('supervision' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),'seconds':time.monotonic()-start,'cases':rows,'model_requests':0,'optimizer_acquisitions':0}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))
