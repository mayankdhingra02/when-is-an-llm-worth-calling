"""Synthetic native-client controls, excluded from all measured research aggregates."""
import json,os,socket,subprocess,sys,tempfile,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.redis_v60 import decode,encode
BIN=ROOT/'.local-runtime/redis-v60/redis-d4c381df7a729c06a5207c4f18d804febe956dc4/src/redis-benchmark'
def main():
    out=ROOT/'artifacts/synthetic_v61_reply_guard';out.mkdir(exist_ok=False);rows=[]
    for name,reply,code in [('correct',b'$7\r\nfixture\r\n',0),('wrong_bytes',b'$7\r\ncorrupt\r\n',42),('nil',b'$-1\r\n',42),('wrong_type',b'+fixture\r\n',42)]:
        with tempfile.TemporaryDirectory(prefix='esc-guard-',dir='/private/tmp') as tmp:
            path=Path(tmp)/'fixture.sock';listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);listener.bind(str(path));listener.listen();listener.settimeout(.1)
            stop=threading.Event();clients=[];threads=[]
            def handle(conn):
                stream=conn.makefile('rb')
                try:
                    while not stop.is_set():
                        args=decode(stream)
                        if args[0].upper()==b'CONFIG':response=encode([args[-1],b'no' if args[-1]==b'appendonly' else b''])
                        elif args[0].upper()==b'INFO':response=b'$0\r\n\r\n'
                        elif args[0].upper()==b'HGET':response=reply
                        else:response=b'+OK\r\n'
                        conn.sendall(response)
                except (OSError,ValueError):pass
                finally:stream.close();conn.close()
            def serve():
                while not stop.is_set():
                    try:conn,_=listener.accept()
                    except socket.timeout:continue
                    conn.settimeout(2);clients.append(conn);t=threading.Thread(target=handle,args=(conn,),daemon=True);threads.append(t);t.start()
            worker=threading.Thread(target=serve,daemon=True);worker.start();env=os.environ.copy();env['V60_EXPECT_VALUE']='fixture';start=time.monotonic()
            try:
                with (out/(name+'.log')).open('xb') as log:result=subprocess.run([str(BIN),'-s',str(path),'-n','1','-c','1','-P','1','--csv','HGET','key','field'],stdout=log,stderr=subprocess.STDOUT,env=env,timeout=5)
                row={'namespace':'synthetic','case':name,'expected_exit':code,'actual_exit':result.returncode,'wall_seconds':time.monotonic()-start};rows.append(row)
            finally:
                stop.set();worker.join(timeout=1);listener.close()
                for conn in clients:
                    try:conn.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
                for t in threads:t.join(timeout=1)
            assert result.returncode==code,row
    (out/'summary.json').write_text(json.dumps({'synthetic_only':True,'research_objective_evaluations':0,'model_requests':0,'cases':rows},indent=2)+'\n')
    print('Four native-client synthetic controls passed')
if __name__=='__main__':main()
