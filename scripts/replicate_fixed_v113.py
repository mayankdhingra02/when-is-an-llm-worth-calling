"""Portable bounded executor for a fixed incumbent-validation packet."""
import argparse,hashlib,json,os,platform,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rss(pid):
 lines=subprocess.check_output(['ps','-axo','pid=,pgid=,rss='],text=True,timeout=2).splitlines()
 return sum(int(x[2])*1024 for line in lines if len(x:=line.split())==3 and int(x[1])==pid)
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--check-only',action='store_true');g.add_argument('--execute',action='store_true');args=ap.parse_args()
 for name,h in json.loads((ROOT/'manifest.json').read_text())['sha256'].items():assert digest(ROOT/name)==h,name
 assert sys.version_info[:2]==(3,10) and platform.system() in ['Darwin','Linux']
 import numpy,scipy,highspy,scipy.sparse.linalg._dsolve._superlu as slu
 assert (numpy.__version__,scipy.__version__,highspy.Highs().version())==('2.2.6','1.13.1','1.7.2')
 machine=hashlib.sha256(platform.node().encode()).hexdigest();source=(ROOT/'source_host_sha256.txt').read_text().strip()
 env=dict(python=sys.version,platform=platform.platform(),machine=platform.machine(),host_name_sha256=machine,same_host_name=machine==source,numpy=numpy.__version__,scipy=scipy.__version__,highs=highspy.Highs().version(),native_superlu_sha256=digest(Path(slu.__file__)),highspy_binaries={p.name:digest(p) for p in Path(highspy.__file__).parent.glob('*.so')},worker_ru_maxrss_unit='bytes' if platform.system()=='Darwin' else 'KiB',parent_rss_unit='bytes')
 if args.check_only:print(json.dumps(dict(verified=True,environment=env,new_objectives=0,collection_executed=False)));return
 assert machine!=source,'Independent-host execution required; do not bypass by renaming'
 rss(-1);out=ROOT/'results';out.mkdir(exist_ok=False);write(out/'environment.json',env)
 cfg=json.loads((ROOT/'configs/validation_v113.json').read_text());records=[];start=time.monotonic()
 assert len(cfg['schedule'])==90
 process_env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','MKL_NUM_THREADS':'1'}
 for job in cfg['schedule']:
  if time.monotonic()-start>1765:break
  d=out/job['request_key'];d.mkdir();write(d/'request.json',job);record=dict(key=job['request_key'],charged=True,at_unix=time.time(),status='started');records.append(record);write(out/'ledger.json',records)
  p=None;t=time.monotonic();peak=0;reason=None
  try:
   with (d/'stdout.txt').open('x') as stdout,(d/'stderr.txt').open('x') as stderr:
    p=subprocess.Popen([sys.executable,str(ROOT/'scripts/worker_numerical_v94.py'),str(d/'request.json'),str(d/'measurement.json')],env=process_env,stdout=stdout,stderr=stderr,start_new_session=True,cwd=ROOT)
    while p.poll() is None:
     peak=max(peak,rss(p.pid))
     if peak>2*1024**3:reason='rss_cap'
     if time.monotonic()-t>30:reason='worker_time_cap'
     if time.monotonic()-start>1795:reason='stage_cap'
     if reason:os.killpg(p.pid,signal.SIGKILL);break
     time.sleep(.05)
    p.wait(timeout=3)
   if reason or p.returncode:raise RuntimeError(str((reason,p.returncode)))
   m=json.loads((d/'measurement.json').read_text());record.update(status='valid' if m['valid'] else 'failed_certificate',label=m['objective_seconds'])
  except Exception as e:record.update(status='failed',label=30.,error=repr(e))
  finally:
   if p is not None and p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
   absent=True
   if p is not None:
    try:os.killpg(p.pid,0);absent=False
    except ProcessLookupError:pass
   record.update(returncode=None if p is None else p.returncode,peak_sampled_rss_bytes=peak,wall_seconds=time.monotonic()-t,owned_process_group_absent=absent)
   write(d/'receipt.json',record);write(out/'ledger.json',records)
  if not absent:break
 write(out/'summary.json',dict(intended=90,acquisitions=len(records),unattempted=90-len(records),stage_seconds=time.monotonic()-start,new_model_requests=0,download_bytes=0,records=records))
 print(f'Collected{len(records)}/90; independent analysis still required')
if __name__=='__main__':main()
