"""Project-local owner builds; finite wall cap, no install or network commands."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
ART=ROOT/'artifacts/study_v66'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    started=time.monotonic();records=json.loads((ART/'build.json').read_text())['steps'];prior_seconds=sum(r['result']['wall_seconds'] for r in records);base=ROOT/'.local-runtime/candidates-v66'
    env=dict(os.environ);env.update(CC='/usr/bin/clang',CXX='/usr/bin/clang++',SDKROOT='/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk',LC_ALL='C')
    jpeg=base/'openjpeg-210a8a5690d0da66f02d49420d7176a21ef409dc';core=base/'coreutils-9.7'
    wheel=ROOT/'artifacts/sources/v66/duckdb-1.3.2-cp310-cp310-macosx_12_0_arm64.whl'
    jobs=[('duckdb_install',[str(ROOT/'.venv/bin/python'),'-m','pip','install','--no-index','--no-deps','--no-compile','--target',str(base/'duckdb'),str(wheel)],ROOT),
          ('openjpeg_configure',['cmake','-S',str(jpeg),'-B',str(jpeg/'build'),'-DCMAKE_BUILD_TYPE=Release','-DCMAKE_POLICY_VERSION_MINIMUM=3.5','-DCMAKE_OSX_SYSROOT='+env['SDKROOT'],'-DBUILD_SHARED_LIBS=OFF','-DBUILD_THIRDPARTY=OFF','-DBUILD_TESTING=OFF','-DCMAKE_DISABLE_FIND_PACKAGE_PNG=TRUE','-DCMAKE_DISABLE_FIND_PACKAGE_TIFF=TRUE','-DCMAKE_DISABLE_FIND_PACKAGE_LCMS=TRUE','-DCMAKE_DISABLE_FIND_PACKAGE_LCMS2=TRUE'],ROOT),
          ('openjpeg_build',['cmake','--build',str(jpeg/'build'),'--target','opj_compress','opj_decompress','-j2'],ROOT),
          ('coreutils_configure',['./configure','--disable-nls','--without-libgmp','--disable-dependency-tracking'],core),
          ('coreutils_build',['make','-j2','src/sort'],core)]
    for name,cmd,cwd in jobs:
        if any(r['name']==name and r['result']['exit_code']==0 for r in records):continue
        left=600-prior_seconds-(time.monotonic()-started)
        if left<1:raise TimeoutError('600s build cap')
        record={'name':name,'command':cmd,'cwd':str(cwd),'result':run(cmd,cwd=cwd,env=env,log_path=ART/(name+'_retry.log'),wall_cap=left)};records.append(record)
        (ART/'build.json').write_text(json.dumps({'environment':{k:env[k] for k in ['CC','CXX','SDKROOT','LC_ALL']},'steps':records,'seconds':time.monotonic()-started},indent=2)+'\n')
        print(name,record['result']['exit_code'],flush=True)
        if record['result']['exit_code']!=0 or record['result']['termination_reason']:break
    bins=[jpeg/'build/bin/opj_compress',jpeg/'build/bin/opj_decompress',core/'src/sort']
    bins+=list((base/'duckdb').rglob('*.so'))
    (ART/'binaries.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in bins if p.exists()},indent=2)+'\n')
if __name__=='__main__':main()
