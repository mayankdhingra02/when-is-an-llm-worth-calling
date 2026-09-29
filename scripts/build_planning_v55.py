"""Build inspected pinned owner source locally, bounded, without LP/downloads."""
import json, os, signal, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'.local-runtime/planning-v55/downward-1eef26b2cbf599a1894606aa898d9d49e1034cb9'
OUT = ROOT/'artifacts/study_v55'
OUT.mkdir(parents=True, exist_ok=True)
commands = [['cmake','-S',str(SRC/'src'),'-B',str(SRC/'builds/release_no_lp'),
             '-DCMAKE_BUILD_TYPE=Release','-DUSE_LP=NO'],
            ['cmake','--build',str(SRC/'builds/release_no_lp'),'-j','2']]
records=[]; start=time.monotonic()
for i, command in enumerate(commands):
    with (OUT/f'build_{i}.log').open('xb') as log:
        p=subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,start_new_session=True)
        while p.poll() is None:
            if time.monotonic()-start>900:
                os.killpg(p.pid,signal.SIGKILL);p.wait();break
            time.sleep(.5)
    records.append({'command':command,'exit_code':p.returncode,'elapsed_seconds':time.monotonic()-start})
    (OUT/'build.json').write_text(json.dumps(records,indent=2)+'\n')
    if p.returncode: raise SystemExit(p.returncode)
print('Project-local release_no_lp build completed.')
