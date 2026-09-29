"""Frozen three-trial diagnosis; expected owner failure remains a charged failure."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from escalation.kanzi_v74 import REFERENCE,parse_header,verify_settings,byte_equal
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss
FAIL={'transform':'LZP+TEXT+BWT+LZP','entropy':'ANS1','block_bytes':262144,'jobs':1}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for n,d in json.loads((ROOT/'reports/protocol_v76.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==d,n
    rss(-1);out=ROOT/'results/v76_kanzi_diagnosis';out.mkdir(exist_ok=False)
    lock=json.loads((ROOT/'configs/runtime_v76.lock.json').read_text());source=ROOT/'data/generated_v74/workload.bin'
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    trials=[];started=time.monotonic();stop=None
    try:
        for i,(version,config) in enumerate([('original',FAIL),('patched',FAIL),('patched',REFERENCE)]):
            if time.monotonic()-started>300:raise TimeoutError('400s stage reserve')
            folder=out/f'trial_{i}';folder.mkdir();row={'trial':i,'version':version,'config':config,'status':'charged'};trials.append(row)
            with (out/'charges.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
            atomic_json(folder/'spec.json',row);compressed=folder/'output.knz';decoded=folder/'decoded.bin'
            def base(jar):return [str(ROOT/lock['java']),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(ROOT/jar)]
            encode=base(lock['original_jar'] if version=='original' else lock['jar'])+['-c','-i',str(source),'-o',str(compressed),'-x','-t',config['transform'],'-e',config['entropy'],'-b',str(config['block_bytes']),'-j','1','-v','3']
            # Original owner decoder must recover patched streams exactly.
            decode=base(lock['original_jar'])+['-d','-i',str(compressed),'-o',str(decoded),'-j','1','-v','3']
            atomic_json(folder/'commands.json',{'compression':encode,'decompression':decode})
            def monitor(pid):
                m=rss(pid);s=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
                return {'rss_bytes':m,'scratch_bytes':s},('rss_cap' if m>2*1024**3 else 'scratch_cap' if s>128*1024**2 else None)
            row['compression']=run(encode,cwd=ROOT,log_path=folder/'compression.log',wall_cap=40,monitor=monitor,env=env)
            log=(folder/'compression.log').read_text()
            if i==0:
                row['status']='application_failure'
                row['expected_failure_reproduced']=row['compression']['exit_code']==13 and row['compression']['termination_reason'] is None and 'Invalid length: 2479880 (must be in [1..2163456])' in log
                atomic_json(folder/'result.json',row);assert row['expected_failure_reproduced'],'Control differs from prior failure'
                continue
            assert row['compression']['exit_code']==0 and row['compression']['termination_reason'] is None
            with compressed.open('rb') as f:header=parse_header(f.read(16))
            verify_settings(header,config,log);row.update(stream_header=header,compressed_bytes=compressed.stat().st_size,compressed_sha256=sha(compressed))
            row['decompression']=run(decode,cwd=ROOT,log_path=folder/'decompression.log',wall_cap=40,monitor=monitor,env=env)
            assert row['decompression']['exit_code']==0 and row['decompression']['termination_reason'] is None
            assert byte_equal(source,decoded);row.update(exact_byte_equality=True,decoded_sha256=sha(decoded),status='valid')
            if i==2:assert row['compressed_sha256']=='290dc8a9522ffed814f88d9fc8bc5edc2a8e3d21c9904b185821464500861dd6','Reference changed'
            atomic_json(folder/'result.json',row)
            print('trial',i,'passed',row['compressed_bytes'],flush=True)
    except Exception as exc:
        stop=repr(exc)
        if trials and trials[-1]['status']=='charged':trials[-1].update(status='unexpected_failure',error=stop);atomic_json(out/f'trial_{trials[-1]["trial"]}'/'result.json',trials[-1])
    finally:atomic_json(out/'summary.json',{'intended_trials':3,'charged_trials':len(trials),'complete_diagnosis':stop is None and len(trials)==3,'stop_reason':stop,'seconds':time.monotonic()-started,'trials':trials,'new_model_requests':0})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
