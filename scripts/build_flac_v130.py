"""Project-local FLAC build; process-local consistent Xcode toolchain only."""
import os, subprocess, time
from collect_smollm_v47 import ROOT, read, write, sha, now

def main():
 a=ROOT/'artifacts/study_v130';start=time.monotonic()
 commands=[['/opt/homebrew/bin/cmake','-S','artifacts/sources/v130/flac-1.5.0','-B','.local-runtime/flac-v130-xcode','-DCMAKE_BUILD_TYPE=Release','-DBUILD_CXXLIBS=OFF','-DBUILD_EXAMPLES=OFF','-DBUILD_TESTING=OFF','-DBUILD_DOCS=OFF','-DWITH_OGG=OFF','-DBUILD_SHARED_LIBS=OFF','-DENABLE_MULTITHREADING=OFF','-DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk','-DCMAKE_C_COMPILER=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang','-DCMAKE_CXX_COMPILER=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang++'],['/opt/homebrew/bin/cmake','--build','.local-runtime/flac-v130-xcode','--target','flacapp','--parallel','2']]
 env={k:v for k,v in os.environ.items() if k not in ['CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS','SDKROOT','CPATH','LIBRARY_PATH','CMAKE_PREFIX_PATH']}
 env['DEVELOPER_DIR']='/Applications/Xcode.app/Contents/Developer'
 receipt={'at':now(),'commands':commands,'status':'started','prior_failure':'build.log: AppleClang17 linked against incompatible CLT27 SDK; no encoding executed','environment_changes':'Process only: remove inherited compiler/linker flags; use Xcode compiler and SDK15.5 together'}
 try:
  with (a/'build_xcode.log').open('x') as f:
   for cmd in commands:subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=max(1,300-(time.monotonic()-start)),check=True)
  binary=ROOT/'.local-runtime/flac-v130-xcode/src/flac/flac'
  receipt.update(status='complete',binary=str(binary.relative_to(ROOT)),sha256=sha(binary),version=subprocess.check_output([str(binary),'--version'],text=True,timeout=5),linked_libraries=subprocess.check_output(['otool','-L',str(binary)],text=True,timeout=5))
 except Exception as e:receipt.update(status='failed',error=repr(e));raise
 finally:receipt['seconds']=time.monotonic()-start;write(a/'build_xcode.json',receipt)
if __name__=='__main__':main()
