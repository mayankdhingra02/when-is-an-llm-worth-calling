"""One-shot V61 480-trial Redis development screen; hard 900-second cap."""
import hashlib,json,random,socket,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss
from escalation.redis_v61 import grid
OUT=ROOT/'results/v61_redis_physical'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    freeze=json.loads((ROOT/'reports/protocol_v61_redis.freeze.json').read_text())
    for name,h in freeze['sha256'].items():assert digest(ROOT/name)==h,name
    rss(-1)
    with tempfile.TemporaryDirectory(prefix='esc-v60-preflight-',dir='/private/tmp') as tmp:
        s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        try:s.bind(str(Path(tmp)/'probe.sock'))
        finally:s.close()
    schedule=[];configs=grid()
    for rep in range(3):
        for query in [0,127]:
            ids=list(range(80));random.Random(61000+rep*1000+query).shuffle(ids)
            for cid in ids:schedule.append({'trial':len(schedule),'round':rep,'family':'redis','workload':'hget_'+str(query),'field_index':query,'config_id':cid,'configuration':configs[cid]})
    OUT.mkdir(exist_ok=False);write(OUT/'schedule.json',schedule);rows=[];stopped=None;start=time.monotonic()
    for item in schedule:
        row=dict(item)
        if stopped or time.monotonic()-start>855:
            row.update(status='unattempted',reason=stopped or 'stage_cap');rows.append(row);continue
        trial=OUT/f"trial_{row['trial']:02d}";trial.mkdir();write(trial/'start.json',row)
        def monitor(pgid):
            size=rss(pgid)
            return {'rss_bytes':size},('rss_watchdog' if size>1024**3 else None)
        row.update(run([sys.executable,str(ROOT/'scripts/redis_worker_v61.py'),str(trial)],cwd=ROOT,log_path=trial/'worker.log',wall_cap=40,monitor=monitor))
        if row['exit_code']==0 and row['termination_reason'] is None:
            m=json.loads((trial/'measurement.json').read_text());assert m['status']=='valid'
            row.update(status='valid',objective_ms=m['objective_ms'],measurement_sha256=digest(trial/'measurement.json'))
        else:
            row.update(status='failed',objective_ms=80000.)
            if row['termination_reason'] not in ['wall_timeout','rss_watchdog']:stopped='unexpected_trial_failure'
        write(trial/'result.json',row);rows.append(row)
        with (OUT/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(row['trial'],row['status'],flush=True)
    write(OUT/'all_cases.json',rows)
    summary={'study':'v61','scope':'generated Redis application workloads; development only',
             'intended':480,'attempted':sum('exit_code' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),
             'unattempted':sum(r['status']=='unattempted' for r in rows),'stopped_reason':stopped,
             'complete_table':stopped is None and all('exit_code' in r for r in rows),
             'stage_seconds':time.monotonic()-start,'stage_cap_seconds':900,'model_requests':0,'external_spend_usd':0,
             'optimization_arms':0,'independent_families':1}
    write(OUT/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
