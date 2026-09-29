"""Bounded project-local owner-source CMake build; no benchmark run."""
import os,subprocess,time
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
 a=ROOT/'artifacts/study_v140';assert read(a/'downloads.json')['complete'];src=ROOT/'artifacts/sources/v140/xz-5.8.4';out=ROOT/'.local-runtime/xz-v140';out.mkdir(exist_ok=False)
 dev='/Applications/Xcode.app/Contents/Developer';sdk=dev+'/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk';cc=dev+'/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang'
 env={k:v for k,v in os.environ.items() if k not in ['CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS','SDKROOT','CPATH','LIBRARY_PATH','CMAKE_PREFIX_PATH','CC','CXX']};env.update(DEVELOPER_DIR=dev,SDKROOT=sdk,CC=cc,CXX=cc+'++')
 cmds=[['/opt/homebrew/bin/cmake','-S',str(src),'-B',str(out),'-DCMAKE_BUILD_TYPE=Release','-DBUILD_SHARED_LIBS=OFF','-DXZ_NLS=OFF','-DBUILD_TESTING=OFF','-DCMAKE_OSX_SYSROOT='+sdk,'-DCMAKE_C_COMPILER='+cc],['/opt/homebrew/bin/cmake','--build',str(out),'--parallel','2','--target','xz']]
 t=time.monotonic();r={'at':now(),'commands':cmds,'status':'started'}
 try:
  with (a/'build.log').open('x') as f:
   for c in cmds:subprocess.run(c,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=max(1,300-(time.monotonic()-t)),check=True)
  r['status']='complete';r['binaries']={str((out/n).relative_to(ROOT)):sha(out/n) for n in ['xz']}
 except Exception as e:r.update(status='failed',error=repr(e));raise
 finally:r['seconds']=time.monotonic()-t;write(a/'build.json',r)
if __name__=='__main__':main()
