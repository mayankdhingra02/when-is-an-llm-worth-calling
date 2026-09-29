"""Two source-owner builds, local directories, bounded subprocesses, no install."""
import os,subprocess,time
from collect_smollm_v47 import ROOT,write,sha,now

def main():
 a=ROOT/'artifacts/study_v131';src=ROOT/'artifacts/sources/v131';runtime=ROOT/'.local-runtime/native-v131';runtime.mkdir(exist_ok=False)
 env={k:v for k,v in os.environ.items() if k not in ['CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS','SDKROOT','CPATH','LIBRARY_PATH','CMAKE_PREFIX_PATH','CC','CXX']}
 dev='/Applications/Xcode.app/Contents/Developer';sdk=dev+'/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk';cc=dev+'/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang'
 env.update(DEVELOPER_DIR=dev,SDKROOT=sdk,CC=cc,CXX=cc+'++',CFLAGS='-O3 -isysroot '+sdk,LDFLAGS='-isysroot '+sdk)
 jobs=[('wavpack',runtime/'wavpack',[
 ['/opt/homebrew/bin/cmake','-S',str(src/'wavpack-5.9.0'),'-B',str(runtime/'wavpack'),'-DCMAKE_BUILD_TYPE=Release','-DBUILD_SHARED_LIBS=OFF','-DWAVPACK_BUILD_PROGRAMS=ON','-DWAVPACK_ENABLE_THREADS=OFF','-DBUILD_TESTING=OFF','-DWAVPACK_INSTALL_DOCS=OFF','-DCMAKE_OSX_SYSROOT='+sdk,'-DCMAKE_C_COMPILER='+cc],
 ['/opt/homebrew/bin/cmake','--build',str(runtime/'wavpack'),'--parallel','2']]),
 ('fftw',runtime/'fftw',[[str(src/'fftw-3.3.11/configure'),'--enable-neon','--enable-threads','--disable-fortran','--disable-shared','--enable-static'],['make','-j2']])]
 for name,cwd,commands in jobs:
  cwd.mkdir(exist_ok=True);start=time.monotonic();receipt={'at':now(),'commands':commands,'status':'started','cwd':str(cwd),'process_environment':{k:env[k] for k in ['SDKROOT','CC','CXX','CFLAGS','LDFLAGS','DEVELOPER_DIR']}}
  try:
   with (a/f'build_{name}.log').open('x') as f:
    for cmd in commands:subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=max(1,300-(time.monotonic()-start)),check=True)
   receipt['status']='complete';receipt['artifacts']={str(p.relative_to(ROOT)):sha(p) for p in cwd.rglob('*') if p.is_file() and (p.suffix=='.a' or p.name in ['wavpack','wvunpack','config.h','CMakeCache.txt'])}
  except Exception as e:receipt.update(status='failed',error=repr(e));raise
  finally:receipt['seconds']=time.monotonic()-start;write(a/f'build_{name}.json',receipt)
if __name__=='__main__':main()
