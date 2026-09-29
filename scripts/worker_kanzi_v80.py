"""One charged trial worker, launched only by the bounded paired runner."""
import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid
from escalation.kanzi_v74 import parse_header,verify_settings,byte_equal
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def collect(specpath, abort_reason=lambda:None):
    specpath=Path(specpath).resolve();folder=specpath.parent
    assert folder.parent==ROOT/'results/v80_kanzi_paired'
    spec=json.loads(specpath.read_text());c=spec['config'];assert c==grid()[spec['config_id']]
    lock=json.loads((ROOT/'configs/runtime_v76.lock.json').read_text());workloads={w['name']:w for w in json.loads((ROOT/'artifacts/study_v79/workloads.json').read_text())['files']}
    source=ROOT/workloads[spec['workload']]['path'];assert sha(source)==workloads[spec['workload']]['sha256']
    base=[str(ROOT/lock['java']),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(ROOT/lock['jar'])]
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    compressed=folder/'output.knz';decoded=folder/'decoded.bin';result={'status':'started','config':c}
    commands={'compression':base+['-c','-i',str(source),'-o',str(compressed),'-x','-t',c['transform'],'-e',c['entropy'],'-b',str(c['block_bytes']),'-j','1','-v','3'],
              'decompression':base+['-d','-i',str(compressed),'-o',str(decoded),'-j','1','-v','3']}
    atomic_json(folder/'commands.json',commands)
    def monitor(pid):
        m=rss(pid);s=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
        return {'rss_bytes':m,'scratch_bytes':s},(abort_reason() or ('rss_cap' if m>2*1024**3 else 'scratch_cap' if s>128*1024**2 else None))
    try:
        for phase,command in commands.items():
            result[phase]=run(command,cwd=ROOT,log_path=folder/f'{phase}.log',wall_cap=40,monitor=monitor,env=env)
            atomic_json(folder/'progress.json',result)
            assert result[phase]['exit_code']==0 and result[phase]['termination_reason'] is None
            if phase=='compression':
                with compressed.open('rb') as f:b=f.read(16)
                header=parse_header(b);verify_settings(header,c,(folder/'compression.log').read_text())
                result.update(header_hex=b.hex(),stream_header=header,compressed_bytes=compressed.stat().st_size,compressed_sha256=sha(compressed))
        assert byte_equal(source,decoded)
        result.update(status='valid',exact_byte_equality=True,input_sha256=sha(source),decoded_sha256=sha(decoded),decoded_bytes=decoded.stat().st_size)
        atomic_json(folder/'result.json',result);compressed.unlink();decoded.unlink()
        atomic_json(folder/'retention.json',{'removed_after_validation':['output.knz','decoded.bin']})
    except Exception as error:
        result.update(status='failed',error=repr(error));atomic_json(folder/'result.json',result)
    return result
if __name__=='__main__':
    sys.exit(0 if collect(sys.argv[1])['status']=='valid' else 1)
