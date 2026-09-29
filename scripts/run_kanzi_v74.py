"""Three real local correctness/resource trials; no optimization or model calls."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v74 import REFERENCE,CONTRAST,parse_header,verify_settings,byte_equal
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()

def main():
    for name,digest in json.loads((ROOT/'reports/protocol_v74.freeze.json').read_text())['sha256'].items():
        assert sha(ROOT/name)==digest,name
    rss(-1)
    out=ROOT/'results/v74_kanzi_feasibility';out.mkdir(exist_ok=False)
    lock=json.loads((ROOT/'configs/runtime_v74.lock.json').read_text())
    java=ROOT/lock['java'];jar=ROOT/lock['jar'];source=ROOT/'data/generated_v74/workload.bin'
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    base=[str(java),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(jar)]
    trials=[];started=time.monotonic();stop=None;active=None
    try:
        for index,config in enumerate([REFERENCE,CONTRAST,REFERENCE]):
            active=None
            if time.monotonic()-started>330:raise TimeoutError('600s stage reserve')
            folder=out/f'trial_{index}';folder.mkdir();compressed=folder/'output.knz';decoded=folder/'decoded.bin'
            row={'trial':index,'config':dict(config),'status':'charged_before_launch','compression':None,'decompression':None};trials.append(row)
            active=row
            atomic_json(folder/'spec.json',row)
            with (out/'charges.jsonl').open('a') as f:f.write(json.dumps({'trial':index,'config':config,'at_unix':time.time()})+'\n');f.flush();os.fsync(f.fileno())
            encode=base+['-c','-i',str(source),'-o',str(compressed),'-x','-t',config['transform'],'-e',config['entropy'],'-b',str(config['block_bytes']),'-j',str(config['jobs']),'-v','3']
            decode=base+['-d','-i',str(compressed),'-o',str(decoded),'-j',str(config['jobs']),'-v','3']
            atomic_json(folder/'commands.json',{'compression':encode,'decompression':decode})
            def monitor(pid):
                memory=rss(pid);scratch=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
                reason='rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>128*1024**2 else None
                return {'rss_bytes':memory,'scratch_bytes':scratch},reason
            for phase,command in [('compression',encode),('decompression',decode)]:
                receipt=run(command,cwd=ROOT,log_path=folder/f'{phase}.log',wall_cap=120,monitor=monitor,env=env)
                row[phase]=receipt;atomic_json(folder/'progress.json',row)
                if receipt['exit_code'] or receipt['termination_reason']:raise RuntimeError(phase+' failed; no retry')
                if phase=='compression':
                    with compressed.open('rb') as f:header=parse_header(f.read(16))
                    verify_settings(header,config,(folder/'compression.log').read_text())
                    row['stream_header']=header;row['compressed_bytes']=compressed.stat().st_size
                    row['compressed_sha256']=sha(compressed)
                    atomic_json(folder/'progress.json',row)
            checkstart=time.monotonic();identical=byte_equal(source,decoded)
            row.update(decoded_bytes=decoded.stat().st_size,decoded_sha256=sha(decoded),input_sha256=sha(source),
                       exact_byte_equality=identical,verification_seconds=time.monotonic()-checkstart)
            if not identical:raise ValueError('Decompressed bytes differ')
            row.update(status='valid',compression_process_seconds=row['compression']['wall_seconds'],
                       decompression_process_seconds=row['decompression']['wall_seconds'],
                       compression_ratio=row['compressed_bytes']/source.stat().st_size)
            atomic_json(folder/'result.json',row);atomic_json(out/'trials.json',trials)
            print('trial',index,'valid',row['compression_process_seconds'],row['compressed_bytes'],flush=True)
    except Exception as error:
        stop=repr(error)
        if active is not None and active['status']!='valid':
            active['status']='failed';active['error']=stop
            atomic_json(out/f'trial_{active["trial"]}'/'result.json',active)
    finally:
        atomic_json(out/'summary.json',{'intended_trials':3,'charged_trials':len(trials),'valid_trials':sum(x['status']=='valid' for x in trials),
                    'unattempted':3-len(trials),'complete':stop is None and len(trials)==3,'stop_reason':stop,
                    'seconds':time.monotonic()-started,'new_model_requests':0,'external_spend_usd':0,'trials':trials})
    if stop:raise RuntimeError(stop)

if __name__=='__main__':main()
