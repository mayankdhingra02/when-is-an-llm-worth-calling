"""One-shot V56 collector; no paid/cloud/model calls."""
import hashlib, json, os, random, re, signal, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.planning_v55 import Task
from escalation.classical_planning_v56 import grid, options
from run_planning_v55 import SRC, DATA, rss
OUT=ROOT/'results/v56_planning_physical'

def write(p,obj): p.write_text(json.dumps(obj,indent=2)+'\n')

def main():
    seal=json.loads((ROOT/'reports/protocol_v56_planning_screen.freeze.json').read_text())
    for name,digest in seal['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    rss(-1)
    task=Task((DATA/'domain.pddl').read_text(),(DATA/'p05.pddl').read_text())
    configurations=grid(); schedule=[]
    for rep in range(3):
        ids=list(range(48));random.Random(56000+rep).shuffle(ids)
        schedule.extend([{'trial':len(schedule)+j,'round':rep,'config_id':cid,'configuration':configurations[cid]} for j,cid in enumerate(ids)])
    OUT.mkdir(exist_ok=False);write(OUT/'schedule.json',schedule)
    stage=time.monotonic(); rows=[]; stopped=None
    for intended in schedule:
        row=dict(intended)
        if stopped or time.monotonic()-stage>1489:
            row.update(status='unattempted',reason=stopped or 'stage_limit');rows.append(row);continue
        trial=OUT/f"trial_{row['trial']:03d}";trial.mkdir()
        command=[sys.executable,str(SRC/'fast-downward.py'),'--build','release_no_lp',
                 '--overall-time-limit','9s','--keep-sas-file','--plan-file',str(trial/'sas_plan'),
                 str(DATA/'domain.pddl'),str(DATA/'p05.pddl'),*options(row['configuration'])]
        row.update(command=command,started_at_unix=time.time());write(trial/'start.json',row)
        start=time.monotonic();reason=None;peak=0;scratch=0
        with (trial/'planner.log').open('xb') as log:
            proc=subprocess.Popen(command,cwd=trial,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                while proc.poll() is None:
                    peak=max(peak,rss(proc.pid))
                    scratch=max(scratch,sum(p.stat().st_size for p in trial.rglob('*') if p.is_file()))
                    if time.monotonic()-start>10:reason='wall_timeout'
                    elif peak>2*1024**3:reason='rss_watchdog'
                    elif scratch>256*1024**2:reason='scratch_watchdog'
                    if reason:os.killpg(proc.pid,signal.SIGKILL);break
                    time.sleep(.2)
                proc.wait(timeout=5)
            except BaseException:
                if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                raise
        wall=time.monotonic()-start
        if wall>10 and reason is None:reason='wall_timeout'
        row.update(exit_code=proc.returncode,wall_seconds=wall,peak_sampled_rss_bytes=peak,
                   peak_sampled_scratch_bytes=scratch,status=reason or 'failed',penalized_ms=20000.)
        if proc.returncode==0 and reason is None:
            try:
                plans=list(trial.glob('sas_plan*'))
                if len(plans)!=1:raise ValueError('Expected exactly one plan')
                plan=plans[0].read_text();check=task.validate(plan)
                log=(trial/'planner.log').read_text()
                if check['cost']!='104' or re.findall(r'; cost = (\d+) \(',plan)!=['104'] or re.findall(r'Plan cost: (\d+)',log)!=['104']:
                    raise ValueError('Unequal/reported cost')
                row.update(status='valid',validation=check,penalized_ms=wall*1000,
                           plan_sha256=hashlib.sha256(plans[0].read_bytes()).hexdigest())
            except ValueError as exc:row.update(status='invalid',validation_error=str(exc));stopped='invalid_plan'
        elif reason is None:
            if proc.returncode in [20,21,22,23,24]:row['status']='resource_or_unsolved'
            else:stopped='unexpected_planner_failure'
        write(trial/'result.json',row);rows.append(row)
        with (OUT/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(row['trial'],row['config_id'],row['status'],round(wall,3),flush=True)
    write(OUT/'all_cases.json',rows)
    summary={'intended':144,'attempted':sum('exit_code' in r for r in rows),
             'valid':sum(r['status']=='valid' for r in rows),'unattempted':sum(r['status']=='unattempted' for r in rows),
             'complete_admissible_table':stopped is None and all('exit_code' in r for r in rows),
             'stopped_reason':stopped,'stage_seconds':time.monotonic()-stage,'model_requests':0,'external_spend_usd':0}
    write(OUT/'summary.json',summary);print(summary,flush=True)
if __name__=='__main__':main()
