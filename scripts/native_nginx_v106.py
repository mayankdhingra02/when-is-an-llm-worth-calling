"""Bounded real native-client feasibility, retaining all intended conditions."""
import json,os,signal,socket,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
import native_nginx_v105 as old
ROOT=old.ROOT;OUT=ROOT/'results/v106_nginx';CLIENT=ROOT/'.local-runtime/http-client-v106/client';COUNT=65536
old.PORT=18596

def run_case(i,case):
 d=OUT/f'{i:02d}_{case}';d.mkdir();(d/'www').mkdir();(d/'logs').mkdir()
 (d/'www/payload.bin').write_bytes(old.PAYLOAD)
 cfg=d/'nginx.conf';cfg.write_text(old.config_text(case,d).replace('keepalive_requests 10000','keepalive_requests 2000000'))
 r={'index':i,'case':case,'status':'started','at':datetime.now(timezone.utc).isoformat(),'configuration':old.REFERENCE if case=='reference' else old.CONTRAST,'config_sha256':old.sha(cfg),'payload_sha256':old.sha(d/'www/payload.bin')}
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
  client=subprocess.run([str(CLIENT),str(COUNT)],capture_output=True,text=True,timeout=70)
  (d/'client.stdout').write_text(client.stdout);(d/'client.stderr').write_text(client.stderr)
  r['client_returncode']=client.returncode;r['measurement']=json.loads(client.stdout)
  if client.returncode or not r['measurement']['valid']:raise RuntimeError('native client failed')
  assert r['measurement']['requests_sent']==r['measurement']['responses_byte_valid']==16*COUNT
  assert r['measurement']['per_connection_valid']==[COUNT]*16
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

def main():
 freeze=json.loads((ROOT/'reports/protocol_v106.freeze.json').read_text())
 for n,h in freeze['sha256'].items():assert old.sha(ROOT/n)==h,n
 assert not OUT.exists();OUT.mkdir()
 with socket.socket() as s:s.bind(('127.0.0.1',18596))
 rows=[{'index':i,'case':c,'status':'unattempted'} for i,c in enumerate(old.CASES)]
 start=time.monotonic()
 def alarm(_s,_f):raise TimeoutError('stage limit')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(1800)
 try:
  for i,case in enumerate(old.CASES):
   if i and rows[i-1]['status']!='valid':break
   with (OUT/'attempts.jsonl').open('a') as f:f.write(json.dumps({'index':i,'case':case,'charged_native_configuration_attempt':True})+'\n')
   rows[i]=run_case(i,case);print(json.dumps(rows[i]),flush=True)
 finally:
  signal.alarm(0)
  attempts=(OUT/'attempts.jsonl').read_text().splitlines() if (OUT/'attempts.jsonl').exists() else []
  (OUT/'summary.json').write_text(json.dumps({'stage':'v106_native_client_feasibility','cases':rows,'lifecycle_seconds':time.monotonic()-start,'new_model_requests':0,'charged_native_configuration_attempts':len(attempts)},indent=2)+'\n')
if __name__=='__main__':main()
