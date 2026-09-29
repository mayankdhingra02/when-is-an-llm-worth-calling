"""Twenty charged local correctness/noise probes, no LLM or optimization claim."""
import hashlib,json,random,socket,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v152';O=ROOT/'results/v152_native';B=ROOT/'.native-v150'
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(port,data):
 with socket.create_connection(('127.0.0.1',port),timeout=2) as s:
  s.sendall(data);f=s.makefile('rb');out=[]
  while True:
   line=f.readline()
   if not line:raise RuntimeError('Unexpected EOF')
   if line==b'END\r\n':return out
   out.append(line.decode().strip())
def prime(port):
 with socket.create_connection(('127.0.0.1',port),timeout=2) as s:
  s.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1);f=s.makefile('rb')
  for client in range(4):
   value=bytes([65+client])*1024
   for key in range(256):
    s.sendall(f'set k{client}_{key:03d} 0 0 1024\r\n'.encode()+value+b'\r\n')
    if f.readline()!=b'STORED\r\n':raise RuntimeError('Prefill not stored')
def verify_stats(lines):
 d={line.split()[1]:line.split()[2] for line in lines if line.startswith('STAT ')}
 expected={'cmd_get':1024000,'get_hits':1024000,'get_misses':0,'cmd_set':1025024,'evictions':0,'curr_items':1024}
 for k,v in expected.items():
  if int(d[k])!=v:raise ValueError(f'Stat {k} expected{v}, actual{d[k]}')
 return d

def main():
 for n,h in json.loads((A/'preprobe.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==h,n
 O.mkdir(exist_ok=False);start=time.monotonic();records=[];plan=[]
 for block in range(5):
  configs=[(t,r) for t in [1,4] for r in [1,20]];random.Random(152000+block).shuffle(configs)
  plan.extend({'block':block,'threads':t,'requests_per_event':r} for t,r in configs)
 write(O/'plan.json',plan);write(O/'ledger.json',{'charged_probes':0,'cap_probes':20,'stage_cap_seconds':300})
 for i,c in enumerate(plan):
  if time.monotonic()-start>=285:raise TimeoutError('Reserve lifecycle within300second cap')
  record={**c,'index':i,'charged':True,'at_unix':time.time(),'status':'started'};records.append(record);write(O/'ledger.json',{'charged_probes':len(records),'cap_probes':20,'stage_cap_seconds':300})
  p=None;log=None;t0=time.monotonic()
  try:
   # Ask the OS for an unused loopback port; do not kill or reuse unrelated services.
   with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
   argv=[str(B/'memcached-1.6.45/memcached'),'-l','127.0.0.1','-p',str(port),'-U','0','-m','64','-t',str(c['threads']),'-R',str(c['requests_per_event'])]
   record['server_command']=argv;log=(O/f'server_{i:02d}.log').open('wb');p=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT);record['pid']=p.pid
   deadline=time.monotonic()+2
   while True:
    if p.poll() is not None:raise RuntimeError('Server exited before readiness')
    try:
     with socket.create_connection(('127.0.0.1',port),timeout=.1):break
    except OSError:
     if time.monotonic()>deadline:raise TimeoutError('Server startup')
     time.sleep(.02)
   prime(port)
   if time.monotonic()-t0>3:raise TimeoutError('Prefill/startup budget')
   result=subprocess.run([str(B/'memcached_client_v152'),str(port)],capture_output=True,text=True,timeout=min(10,13-(time.monotonic()-t0)))
   record.update(client_stdout=result.stdout,client_stderr=result.stderr,client_exit=result.returncode);result.check_returncode();measurement=json.loads(result.stdout)
   if measurement['checked_operations']!=2048000 or measurement['failed_clients']!=0 or not 0<measurement['seconds']<=10:raise ValueError('Invalid correctness/time')
   record['measurement']=measurement;record['stats']=verify_stats(command(port,b'stats\r\n'));record['status']='correct'
  except Exception as e:record.update(status='failed',error=repr(e))
  finally:
   if p is not None:
    if p.poll() is None:
     p.terminate()
     try:p.wait(timeout=1)
     except subprocess.TimeoutExpired:p.kill();p.wait(timeout=1)
    record['server_exit']=p.returncode;record['server_reaped']=p.poll() is not None
   if log:log.close()
   record['lifecycle_seconds']=time.monotonic()-t0;write(O/f'probe_{i:02d}.json',record)
  print(json.dumps({'probe':i,'status':record['status'],'seconds':record.get('measurement',{}).get('seconds'),'error':record.get('error')}),flush=True)
 write(O/'completion.json',{'intended_probes':20,'charged_probes':len(records),'correct':sum(r['status']=='correct' for r in records),'wall_seconds':time.monotonic()-start,'new_model_requests':0,'new_recorded_table_acquisitions':0,'new_native_feasibility_probes':len(records)})
if __name__=='__main__':main()
