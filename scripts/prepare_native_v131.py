"""Fixed workload conversion and worker compile; no performance measurement."""
import subprocess,struct
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
 a=ROOT/'artifacts/study_v131';out=ROOT/'data/native_v131';out.mkdir(exist_ok=False);rows=[];signals=[]
 for w in read(ROOT/'artifacts/study_v130/workloads.json')['workloads']:
  assert sha(ROOT/w['raw_path'])==w['raw_sha256']
  raw=(ROOT/w['raw_path']).read_bytes();assert len(raw)>=8192*2
  x=np.frombuffer(raw[:8192*2],dtype='<i2').astype('<f8')/32768.;signals.append(x)
  rows.append({**w,'fftw_samples':8192,'fftw_sample_rule':'First8192signed samples scaled by32768, no target-dependent selection'})
 np.asarray(signals,dtype='<f8').tofile(out/'signals.f64')
 reference=np.fft.fft(np.asarray(signals),axis=1).astype('<c16');reference.tofile(out/'reference.c128')
 write(a/'workloads.json',{'at':now(),'workloads':rows,'fftw_input':{'path':str((out/'signals.f64').relative_to(ROOT)),'sha256':sha(out/'signals.f64')},'fftw_reference':{'path':str((out/'reference.c128').relative_to(ROOT)),'sha256':sha(out/'reference.c128'),'implementation':'NumPy pocketfft '+np.__version__,'criterion':'max abs complex error <= 1e-10*max(1,max abs reference), finite all samples'},'wavpack':'Whole three original licensed raw clips; same source sample hashes as V130'})
 runtime=ROOT/'.local-runtime/native-v131';dev='/Applications/Xcode.app/Contents/Developer';sdk=dev+'/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk';cc=dev+'/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang'
 cmd=[cc,'-O3','-std=c11','-isysroot',sdk,'-I',str(ROOT/'artifacts/sources/v131/fftw-3.3.11/api'),str(ROOT/'scripts/fftw_worker_v131.c'),str(runtime/'fftw/threads/.libs/libfftw3_threads.a'),str(runtime/'fftw/.libs/libfftw3.a'),'-lm','-lpthread','-o',str(runtime/'fftw_worker')]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);write(a/'worker_build.json',{'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr
 paths=[runtime/'fftw_worker',runtime/'wavpack/wavpack',runtime/'wavpack/wvunpack'];write(a/'binaries.json',{str(p.relative_to(ROOT)):sha(p) for p in paths})
 print('Prepared two task contracts; zero encoder or FFT worker executions')
if __name__=='__main__':main()
