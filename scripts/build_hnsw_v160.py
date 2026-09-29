"""Scoped compatible toolchain selection; does not change macOS settings."""
import os,subprocess,json,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v160'
def main():
 assert not (A/'build_repair.json').exists();dev='/Applications/Xcode.app/Contents/Developer';sdk=dev+'/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk';cc=dev+'/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang++';assert Path(sdk).is_dir()
 env={k:v for k,v in os.environ.items() if k not in ['CFLAGS','CXXFLAGS','CPPFLAGS','LDFLAGS','SDKROOT','CPATH','LIBRARY_PATH','CMAKE_PREFIX_PATH','CC','CXX']};env.update(DEVELOPER_DIR=dev,SDKROOT=sdk)
 cmd=[cc,'-O2','-std=c++11','-pthread','-isysroot',sdk,'-I','.native-v160/hnswlib-0.8.0','scripts/hnsw_worker_v161.cpp','-o','.native-v160/bin/hnsw_worker_v161'];start=time.monotonic()
 with (A/'build_repair.log').open('wb') as f:r=subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=120)
 p=ROOT/cmd[-1];receipt={'command':cmd,'environment':{'DEVELOPER_DIR':dev,'SDKROOT':sdk},'compiler':subprocess.check_output([cc,'--version'],env=env,text=True),'exit':r.returncode,'seconds':time.monotonic()-start,'cap_seconds':120,'binary_sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,'prior_failure':'Default CommandLineTools SDK27 stubs unsupported by selected linker; build.log retained. First reference-preparation script then failed reading missing binary; no candidate application ran.'};(A/'build_repair.json').write_text(json.dumps(receipt,indent=2)+'\n');r.check_returncode()
if __name__=='__main__':main()
