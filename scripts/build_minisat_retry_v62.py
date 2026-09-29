"""Bounded project-local build of inspected owner MiniSat, no system installation."""
import hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
SRC=ROOT/'.local-runtime/minisat-v62/minisat-37dc6c67e2af26379d88ce349eb9c4c6160e8543';OUT=ROOT/'artifacts/study_v62'
if __name__=='__main__':
    OUT.mkdir(exist_ok=True);records=[]
    commands=[['cmake','-S',str(SRC),'-B',str(SRC/'build'),'-DCMAKE_POLICY_VERSION_MINIMUM=3.5','-DCMAKE_BUILD_TYPE=Release','-DCMAKE_CXX_STANDARD=98','-DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk'],['cmake','--build',str(SRC/'build'),'--target','minisat_core','-j','2']]
    for i,c in enumerate(commands):
        r=run(c,cwd=ROOT,log_path=OUT/f'build_retry_{i}.log',wall_cap=120);r['command']=c;records.append(r)
        (OUT/'build_retry.json').write_text(json.dumps(records,indent=2)+'\n')
        if r['exit_code'] or r['termination_reason']:raise SystemExit(1)
    b=SRC/'build/minisat_core';(OUT/'binary.json').write_text(json.dumps({'path':str(b.relative_to(ROOT)),'sha256':hashlib.sha256(b.read_bytes()).hexdigest()},indent=2)+'\n')
    print('MiniSat core built locally')
