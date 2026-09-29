"""Build inspected owner source locally; no installer, service, or download."""
import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
SRC=ROOT/'.local-runtime/redis-v60/redis-d4c381df7a729c06a5207c4f18d804febe956dc4'
OUT=ROOT/'artifacts/study_v60'
command=['make','-j2','MALLOC=libc','BUILD_TLS=no',
         'CC=/usr/bin/clang -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk']
if __name__=='__main__':
    env=os.environ.copy();env['SDKROOT']='/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk'
    result=run(command,cwd=SRC,log_path=OUT/'build.log',wall_cap=600,env=env)
    result['command']=command;result['sdkroot']=env['SDKROOT']
    result['source_commit']='d4c381df7a729c06a5207c4f18d804febe956dc4'
    if result['exit_code']==0:
        result['binary_sha256']={n:hashlib.sha256((SRC/'src'/n).read_bytes()).hexdigest() for n in ['redis-server','redis-benchmark','redis-cli']}
    (OUT/'build.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));sys.exit(result['exit_code'] or bool(result['termination_reason']))
