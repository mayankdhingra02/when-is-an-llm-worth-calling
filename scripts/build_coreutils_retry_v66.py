"""Generate owner-declared built prerequisites, then build only sort."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
ART=ROOT/'artifacts/study_v66'
if __name__=='__main__':
    previous=json.loads((ART/'build.json').read_text());spent=sum(r['result']['wall_seconds'] for r in previous['steps']);start=time.monotonic();records=[]
    env={**os.environ,**previous['environment']};cwd=ROOT/'.local-runtime/candidates-v66/coreutils-9.7'
    commands=[['make','-j2','-f','Makefile','-f',str(ART/'coreutils_prepare.mk'),'v66-prepare'],['make','-j2','src/sort']]
    for i,cmd in enumerate(commands):
        left=600-spent-(time.monotonic()-start);assert left>0
        r=run(cmd,cwd=cwd,env=env,wall_cap=left,log_path=ART/f'coreutils_prereq_{i}.log');records.append({'command':cmd,'result':r});(ART/'build_coreutils_retry.json').write_text(json.dumps(records,indent=2)+'\n')
        if r['exit_code'] or r['termination_reason']:raise SystemExit(1)
    p=cwd/'src/sort';bins=json.loads((ART/'binaries.json').read_text());bins[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();(ART/'binaries.json').write_text(json.dumps(bins,indent=2)+'\n');print('GNU sort built')
