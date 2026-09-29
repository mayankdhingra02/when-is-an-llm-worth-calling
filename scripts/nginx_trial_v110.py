"""Bounded real native-client feasibility, retaining all intended conditions."""
import json,os,signal,socket,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
import native_nginx_v105 as old
ROOT=old.ROOT;CLIENT=ROOT/'.local-runtime/http-client-v110/client';COUNT=65536
old.PORT=18596

def run_clients(d):
 children=[];receipts=[];start=time.monotonic();deadline=start+70
 try:
  for i in range(4):
   out=(d/f'client_{i}.stdout').open('w');err=(d/f'client_{i}.stderr').open('w')
   try:p=subprocess.Popen([str(CLIENT),str(COUNT)],stdout=out,stderr=err,start_new_session=True)
   except BaseException:out.close();err.close();raise
   children.append((p,out,err));receipts.append({'index':i,'pid':p.pid,'launch_offset_seconds':time.monotonic()-start})
  for p,_,_ in children:p.wait(timeout=max(.001,deadline-time.monotonic()))
 finally:
  elapsed=time.monotonic()-start
  for i,(p,out,err) in enumerate(children):
   if p.poll() is None:
    try:os.killpg(p.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    p.wait(timeout=5)
   out.close();err.close();rec=receipts[i];rec['returncode']=p.returncode
   try:os.killpg(p.pid,0);rec['owned_process_group_absent']=False
   except ProcessLookupError:rec['owned_process_group_absent']=True
   try:rec['measurement']=json.loads((d/f'client_{i}.stdout').read_text())
   except (ValueError,OSError):rec['measurement']=None
  raw={'clients':receipts,'workload_seconds':elapsed}
  (d/'clients.json').write_text(json.dumps(raw,indent=2)+'\n')
 good=len(receipts)==4 and all(x['returncode']==0 and x['owned_process_group_absent'] and x['measurement'] and x['measurement']['valid'] and x['measurement']['requests_sent']==x['measurement']['responses_byte_valid']==4*COUNT and x['measurement']['per_connection_valid']==[COUNT]*4 for x in receipts)
 cpu=sum(x['measurement']['client_cpu_seconds'] for x in receipts if x['measurement'])
 return dict(raw,valid=good,client_cpu_seconds=cpu,client_cpu_to_wall=cpu/elapsed,requests_sent=sum(x['measurement']['requests_sent'] for x in receipts if x['measurement']),responses_byte_valid=sum(x['measurement']['responses_byte_valid'] for x in receipts if x['measurement']))

from nginx_domain_v108 import config
def run_trial(d,row):
 d.mkdir(parents=True);(d/'www').mkdir();(d/'logs').mkdir()
 (d/'www/payload.bin').write_bytes(old.PAYLOAD)
 cfg=d/'nginx.conf';cfg.write_text(config(row,d))
 r={'status':'started','at':datetime.now(timezone.utc).isoformat(),'configuration':row,'config_sha256':old.sha(cfg),'payload_sha256':old.sha(d/'www/payload.bin')}
 p=None;log=None
 try:
  check=subprocess.run([str(old.BINARY),'-p',str(d)+'/', '-c',str(cfg),'-t'],capture_output=True,text=True,timeout=10)
  (d/'syntax.log').write_text(check.stdout+check.stderr)
  if check.returncode:raise RuntimeError('syntax')
  log=(d/'server.log').open('w');p=subprocess.Popen([str(old.BINARY),'-p',str(d)+'/', '-c',str(cfg)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True);r['pid']=p.pid
  deadline=time.monotonic()+10
  while True:
   if p.poll() is not None:raise RuntimeError('server startup exit')
   try:
    with socket.create_connection(('127.0.0.1',18596),timeout=.1):break
   except OSError:
    if time.monotonic()>deadline:raise TimeoutError('startup')
    time.sleep(.05)
  r['measurement']=run_clients(d)
  if not r['measurement']['valid']:raise RuntimeError('native clients failed')
  r['status']='valid'
 except Exception as e:r.update(status='failed',error=repr(e))
 finally:
  if p:
   try:os.killpg(p.pid,signal.SIGTERM)
   except ProcessLookupError:pass
   try:p.wait(timeout=10)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
   r['server_returncode']=p.returncode;deadline=time.monotonic()+2
   while True:
    try:os.killpg(p.pid,0)
    except ProcessLookupError:r['owned_process_group_absent']=True;break
    if time.monotonic()>deadline:
     r.update(status='failed',owned_process_group_absent=False,cleanup_error='group remains');break
    time.sleep(.05)
  if log:log.close()
  (d/'result.json').write_text(json.dumps(r,indent=2)+'\n')
 return r
