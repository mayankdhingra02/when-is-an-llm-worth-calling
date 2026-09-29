"""Byte-validated local HTTP workload. No LLM, archived outcomes, or tuning loop."""
import asyncio
import hashlib
import json
import os
import signal
import socket
import subprocess
import time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/study_v105'
OUT=ROOT/'results/v105_nginx'
BINARY=ROOT/'.local-runtime/nginx-v105/nginx-1.28.3/objs/nginx'
PORT=18595
PAYLOAD=bytes(range(256))*128
REFERENCE={'workers':1,'connections':64,'sendfile':'off','multi_accept':'off','tcp_nopush':'off','tcp_nodelay':'on','accept_mutex':'off'}
CONTRAST={'workers':2,'connections':256,'sendfile':'on','multi_accept':'on','tcp_nopush':'on','tcp_nodelay':'on','accept_mutex':'on'}
CASES=['reference','contrast','reference','reference','contrast','reference']
CONCURRENCY=16
PER_CLIENT=512

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def config_text(case,folder):
    c=REFERENCE if case=='reference' else CONTRAST
    return f'''daemon off;
master_process on;
worker_processes {c['workers']};
pid "{folder}/nginx.pid";
error_log "{folder}/error.log" notice;
events {{ worker_connections {c['connections']}; multi_accept {c['multi_accept']}; accept_mutex {c['accept_mutex']}; }}
http {{
 access_log off;
 default_type application/octet-stream;
 sendfile {c['sendfile']};
 tcp_nopush {c['tcp_nopush']};
 tcp_nodelay {c['tcp_nodelay']};
 keepalive_timeout 10s;
 keepalive_requests 10000;
 server {{ listen 127.0.0.1:{PORT}; server_name localhost;
  root "{folder}/www";
  location = /payload.bin {{ }}
 }}
}}
'''

def validate_header(header,expected_length):
    lines=header.decode('ascii').split('\r\n')
    if lines[0]!='HTTP/1.1 200 OK':raise ValueError('Non-200 HTTP response')
    fields={}
    for line in lines[1:]:
        if not line:continue
        name,value=line.split(':',1);name=name.lower()
        if name in fields:raise ValueError('Duplicate response header')
        fields[name]=value.strip()
    if fields.get('content-length')!=str(expected_length):raise ValueError('Incorrect Content-Length')
    if 'transfer-encoding' in fields:raise ValueError('Unexpected Transfer-Encoding')
    if fields.get('content-encoding','identity')!='identity':raise ValueError('Unexpected Content-Encoding')
    if fields.get('connection','').lower()=='close':raise ValueError('Unexpected connection closure')

def validate_body(body,expected=PAYLOAD):
    if body!=expected:raise ValueError('Response bytes differ from fixed workload')

async def client(number,counts):
    reader,writer=await asyncio.open_connection('127.0.0.1',PORT)
    request=b'GET /payload.bin HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\nAccept-Encoding: identity\r\n\r\n'
    try:
        for _ in range(PER_CLIENT):
            counts[number]['sent']+=1
            writer.write(request);await writer.drain()
            header=await reader.readuntil(b'\r\n\r\n');validate_header(header,len(PAYLOAD))
            body=await reader.readexactly(len(PAYLOAD));validate_body(body)
            counts[number]['valid']+=1
    finally:
        writer.close();await writer.wait_closed()

async def workload(counts):
    tasks=[asyncio.create_task(client(i,counts)) for i in range(CONCURRENCY)]
    try:await asyncio.wait_for(asyncio.gather(*tasks),timeout=60)
    finally:
        for task in tasks:
            if not task.done():task.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)

def run_case(index,case):
    folder=OUT/f'{index:02d}_{case}';folder.mkdir();(folder/'www').mkdir();(folder/'logs').mkdir()
    (folder/'www/payload.bin').write_bytes(PAYLOAD)
    config=folder/'nginx.conf';config.write_text(config_text(case,folder))
    counts=[{'sent':0,'valid':0} for _ in range(CONCURRENCY)]
    result={'index':index,'case':case,'status':'started','configuration':REFERENCE if case=='reference' else CONTRAST,
            'config_sha256':sha(config),'payload_sha256':hashlib.sha256(PAYLOAD).hexdigest(),'client_counts':counts,
            'at':datetime.now(timezone.utc).isoformat()}
    proc=None;log=None
    try:
        check=subprocess.run([str(BINARY),'-p',str(folder)+'/', '-c',str(config),'-t'],capture_output=True,text=True,timeout=10)
        (folder/'syntax.log').write_text(check.stdout+check.stderr)
        if check.returncode:raise RuntimeError('NGINX syntax check failed')
        log=(folder/'server.log').open('w')
        proc=subprocess.Popen([str(BINARY),'-p',str(folder)+'/', '-c',str(config)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        result['pid']=proc.pid;deadline=time.monotonic()+10
        while True:
            if proc.poll() is not None:raise RuntimeError('NGINX exited during startup')
            try:
                with socket.create_connection(('127.0.0.1',PORT),timeout=.1):break
            except OSError:
                if time.monotonic()>deadline:raise TimeoutError('NGINX startup timed out')
                time.sleep(.05)
        wall=time.monotonic();cpu=time.process_time()
        try:asyncio.run(workload(counts))
        finally:
            result['workload_seconds']=time.monotonic()-wall
            result['client_cpu_seconds']=time.process_time()-cpu
            result['client_cpu_to_wall']=result['client_cpu_seconds']/result['workload_seconds']
        assert sum(c['valid'] for c in counts)==CONCURRENCY*PER_CLIENT
        result['status']='valid'
    except Exception as e:
        result.update(status='failed',error=repr(e))
    finally:
        if proc:
            try:os.killpg(proc.pid,signal.SIGTERM)
            except ProcessLookupError:pass
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
            result['server_returncode']=proc.returncode
            deadline=time.monotonic()+2
            while True:
                try:os.killpg(proc.pid,0)
                except ProcessLookupError:result['owned_process_group_absent']=True;break
                if time.monotonic()>deadline:
                    result['owned_process_group_absent']=False
                    result['status']='failed';result['cleanup_error']='Process group still present';break
                time.sleep(.05)
        if log:log.close()
        result['requests_sent']=sum(c['sent'] for c in counts)
        result['responses_byte_valid']=sum(c['valid'] for c in counts)
        result['response_body_bytes_validated']=result['responses_byte_valid']*len(PAYLOAD)
        (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    freeze=json.loads((ROOT/'reports/protocol_v105.execution_freeze.json').read_text())
    for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
    assert not OUT.exists();OUT.mkdir(parents=True)
    # Refuse to attach to an existing unrelated loopback listener.
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',PORT))
    start=time.monotonic();rows=[]
    def alarm(_s,_f):raise TimeoutError('V105 1800-second lifecycle limit')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(1800)
    try:
        for i,case in enumerate(CASES):
            if rows and rows[-1]['status']!='valid':
                rows.append({'index':i,'case':case,'status':'unattempted'});continue
            # Persist the charged attempt before starting a workload.
            with (OUT/'attempts.jsonl').open('a') as f:f.write(json.dumps({'index':i,'case':case,'charged_native_configuration_attempt':True})+'\n')
            result=run_case(i,case);rows.append(result)
            print(json.dumps(result),flush=True)
    finally:
        signal.alarm(0)
        (OUT/'summary.json').write_text(json.dumps({'stage':'v105_native_feasibility','cases':rows,'lifecycle_seconds':time.monotonic()-start,
            'new_model_requests':0,'charged_native_configuration_attempts':sum(r['status']!='unattempted' for r in rows)},indent=2)+'\n')

if __name__=='__main__':main()
