"""One-shot bounded real planner feasibility. See frozen V55 protocol."""
import hashlib, json, os, re, signal, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from escalation.planning_v55 import Task
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '.local-runtime/planning-v55/downward-1eef26b2cbf599a1894606aa898d9d49e1034cb9'
OUT = ROOT / 'results/v55_planning_feasibility'
DATA = ROOT / 'artifacts/sources/v55'

def rss(pgid):
    lines = subprocess.check_output(['ps','-axo','pid=,pgid=,rss='], text=True, timeout=2).splitlines()
    return sum(int(row[2])*1024 for line in lines if len(row := line.split()) == 3 and int(row[1]) == pgid)

def main():
    seal = json.loads((ROOT/'reports/protocol_v55_planning_feasibility.freeze.json').read_text())
    for name, digest in seal['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    rss(-1)  # permission preflight before any experiment artifacts or invocation
    task = Task((DATA/'domain.pddl').read_text(), (DATA/'p05.pddl').read_text())
    OUT.mkdir(exist_ok=False)
    expressions = ['astar(lmcut())', 'astar(hmax())', 'astar(lmcut())']
    (OUT/'intended.json').write_text(json.dumps(expressions, indent=2)+'\n')
    stage = time.monotonic(); rows = []
    for i, search in enumerate(expressions):
        if time.monotonic()-stage > 100:
            rows.append({'trial':i,'search':search,'status':'unattempted_stage_limit'})
            continue
        trial = OUT/f'trial_{i}'; trial.mkdir()
        command = [sys.executable, str(SRC/'fast-downward.py'), '--build', 'release_no_lp',
                   '--overall-time-limit', '40s', '--plan-file',str(trial/'sas_plan'),
                   str(DATA/'domain.pddl'),str(DATA/'p05.pddl'),'--search',search]
        row = {'trial':i,'search':search,'command':command,'started_at_unix':time.time()}
        (trial/'start.json').write_text(json.dumps(row,indent=2)+'\n')
        start=time.monotonic(); reason=None; peak=0; scratch=0
        with (trial/'planner.log').open('xb') as log:
            proc=subprocess.Popen(command, cwd=trial,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                while proc.poll() is None:
                    peak=max(peak,rss(proc.pid))
                    scratch=max(scratch,sum(p.stat().st_size for p in trial.rglob('*') if p.is_file()))
                    if time.monotonic()-start>45: reason='wall_timeout'
                    elif peak>2*1024**3: reason='rss_watchdog'
                    elif scratch>256*1024**2: reason='scratch_watchdog'
                    if reason:
                        os.killpg(proc.pid,signal.SIGKILL); break
                    time.sleep(.2)
                proc.wait(timeout=5)
            except BaseException:
                if proc.poll() is None:
                    os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                raise
        row.update(exit_code=proc.returncode,wall_seconds=time.monotonic()-start,
                   peak_sampled_rss_bytes=peak,peak_sampled_scratch_bytes=scratch,status=reason or 'failed')
        if proc.returncode == 0 and reason is None:
            try:
                plans=list(trial.glob('sas_plan*'))
                if len(plans)!=1: raise ValueError('Expected one plan')
                plan=plans[0].read_text(); check=task.validate(plan)
                comment=re.findall(r'; cost = (\d+) \(',plan)
                logged=re.findall(r'Plan cost: (\d+)',(trial/'planner.log').read_text())
                if comment != [check['cost']] or logged != [check['cost']]:
                    raise ValueError('Reported/recomputed cost mismatch')
                row.update(status='valid',validation=check,plan_sha256=hashlib.sha256(plans[0].read_bytes()).hexdigest())
            except ValueError as exc:
                row.update(status='invalid',validation_error=str(exc))
        (trial/'result.json').write_text(json.dumps(row,indent=2)+'\n')
        rows.append(row)
        (OUT/'trials.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(i,row['status'],round(row['wall_seconds'],3),flush=True)
    passed=len(rows)==3 and all(r['status']=='valid' for r in rows) and len({r['validation']['cost'] for r in rows})==1
    summary={'study':'v55','passed':passed,'intended':3,'attempted':sum('exit_code' in r for r in rows),
             'valid':sum(r['status']=='valid' for r in rows),'stage_seconds':time.monotonic()-stage,
             'model_requests':0,'external_spend_usd':0,'recorded_objective_accesses':0,'trials':rows}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('Feasibility pass:',passed,flush=True)

if __name__=='__main__': main()
