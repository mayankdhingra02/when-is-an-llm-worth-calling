"""Time-bounded owner source builds exclusively beneath this project."""
import hashlib,json,subprocess,time,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v150';B=ROOT/'.native-v150'
def main():
 assert not (A/'build_repair.json').exists();start=time.monotonic();records=[];error=None;prefix=B/'prefix'
 prior=json.loads((A/'build.json').read_text())['seconds'];env={k:v for k,v in os.environ.items() if k not in ['CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS','SDKROOT','CPATH','LIBRARY_PATH','CMAKE_PREFIX_PATH','CC','CXX']}
 dev='/Applications/Xcode.app/Contents/Developer';sdk=dev+'/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk';cc=dev+'/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang';assert Path(sdk).is_dir()
 env.update(DEVELOPER_DIR=dev,SDKROOT=sdk,CC=cc,CFLAGS='-O2 -isysroot '+sdk,LDFLAGS='-isysroot '+sdk)
 cmds=[(B/'libevent-2.1.13-stable',['./configure','--prefix='+str(prefix),'--disable-shared','--enable-static','--disable-openssl','--disable-samples','--disable-libevent-regress']), (B/'libevent-2.1.13-stable',['make','-j2']), (B/'libevent-2.1.13-stable',['make','install']), (B/'memcached-1.6.45',['./configure','--prefix='+str(prefix),'--with-libevent='+str(prefix),'--disable-docs']), (B/'memcached-1.6.45',['make','-j2'])]
 try:
  for i,(cwd,cmd) in enumerate(cmds):
   remaining=600-prior-(time.monotonic()-start)
   if remaining<=0:raise TimeoutError('Build cap')
   log=A/f'build_repair_{i}.log';before=time.monotonic()
   with log.open('wb') as f:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=remaining)
   records.append({'cwd':str(cwd.relative_to(ROOT)),'command':cmd,'exit':r.returncode,'seconds':time.monotonic()-before,'log':str(log.relative_to(ROOT))})
   r.check_returncode()
 except Exception as e:error=repr(e)
 finally:
  binaries=[B/'memcached-1.6.45/memcached',prefix/'lib/libevent.a']
  (A/'build_repair.json').write_text(json.dumps({'commands':records,'prior_seconds':prior,'toolchain_environment':{k:env[k] for k in ['DEVELOPER_DIR','SDKROOT','CC','CFLAGS','LDFLAGS']},'seconds':time.monotonic()-start,'cap_seconds':600,'error':error,'outputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in binaries if p.exists()}},indent=2)+'\n')
 if error:raise RuntimeError(error)
 print('Built Memcached and static libevent in project only')
if __name__=='__main__':main()
