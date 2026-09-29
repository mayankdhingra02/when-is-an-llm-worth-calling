"""One isolated, correctness-checked Redis feasibility trial; parent enforces cap."""
import hashlib,json,os,re,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.redis_v60 import Client,populate,validate,value,field
BIN=ROOT/'.local-runtime/redis-v60/redis-d4c381df7a729c06a5207c4f18d804febe956dc4/src'

def main():
    trial=Path(sys.argv[1]);spec=json.loads((trial/'start.json').read_text())
    config=spec['configuration'];query=spec['field_index'];record={}
    with tempfile.TemporaryDirectory(prefix='esc-v60-',dir='/private/tmp') as tmp:
        sock=Path(tmp)/'redis.sock'
        command=[str(BIN/'redis-server'),'--port','0','--unixsocket',str(sock),'--unixsocketperm','700',
                 '--daemonize','no','--save','','--appendonly','no','--dir',str(trial),
                 '--maxmemory','256mb','--maxmemory-policy','noeviction','--dynamic-hz','no']
        for k,v in config.items():command.extend(['--'+k,str(v)])
        server_log=(trial/'server.log').open('xb');proc=subprocess.Popen(command,stdout=server_log,stderr=subprocess.STDOUT)
        client=None
        try:
            start=time.monotonic()
            while not sock.exists():
                if proc.poll() is not None or time.monotonic()-start>5:raise RuntimeError('Server startup failed')
                time.sleep(.01)
            client=Client(sock);assert client.call('PING')==b'PONG'
            for k,v in config.items():assert client.call('CONFIG','GET',k)==[k.encode(),str(v).encode()]
            record['server_info']=client.call('INFO','server').decode();assert 'redis_version:7.2.11' in record['server_info']
            populate(client);record['before']=validate(client)
            record['encoding']=client.call('OBJECT','ENCODING','v60:000000000000').decode()
            env=os.environ.copy();env['V60_EXPECT_VALUE']=value(query).decode()
            phases=[]
            for phase,requests in [('warmup',10000),('measured',100000)]:
                args=[str(BIN/'redis-benchmark'),'-s',str(sock),'-n',str(requests),'-c','50','-P','16','-r','256',
                      '--seed','60000','--threads','1','--csv','HGET','v60:__rand_int__',field(query).decode()]
                t=time.monotonic()
                with (trial/f'{phase}.log').open('xb') as log:
                    done=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=15)
                elapsed=time.monotonic()-t;raw=(trial/f'{phase}.log').read_text()
                assert done.returncode==0 and 'V60_REPLY_MISMATCH' not in raw
                counts=re.findall(r'V60_VALIDATED_REPLIES=(\d+)',raw);assert len(counts)==1
                assert requests<=int(counts[0])<=requests+50*16
                phases.append({'phase':phase,'command':args,'requested':requests,'validated_replies':int(counts[0]),'wall_seconds':elapsed,
                               'log_sha256':hashlib.sha256((trial/f'{phase}.log').read_bytes()).hexdigest()})
            record['phases']=phases;record['after']=validate(client);assert record['before']==record['after']
            record['objective_ms']=phases[1]['wall_seconds']*1000
            record['server_command']=command;record['status']='valid'
            client.call('SHUTDOWN','NOSAVE')
        except ValueError as exc:
            # SHUTDOWN closes the socket without a reply; only accept after all checks.
            if record.get('status')!='valid' or 'Truncated' not in str(exc):raise
        finally:
            if client:client.close()
            if proc.poll() is None:proc.terminate()
            try:proc.wait(timeout=3)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=3)
            server_log.close();record['server_exit_code']=proc.returncode
        assert record['status']=='valid' and proc.returncode==0
        (trial/'measurement.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':main()
