"""One-shot live classical collection, max200 trials/1800s, no model calls."""
import hashlib,json,os,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid,features,choose,guard,SEEDS,METHODS
from escalation.kanzi_v74 import parse_header,verify_settings,byte_equal
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for name,digest in json.loads((ROOT/'reports/protocol_v75.freeze.json').read_text())['sha256'].items():assert sha(ROOT/name)==digest,name
    rss(-1);out=ROOT/'results/v75_kanzi_classical';out.mkdir(exist_ok=False)
    configs=grid();x=features(configs);lock=json.loads((ROOT/'configs/runtime_v74.lock.json').read_text())
    base=[str(ROOT/lock['java']),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(ROOT/lock['jar'])]
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    source=ROOT/'data/generated_v74/workload.bin';sourcehash=sha(source)
    rows=[];cases=[];started=time.monotonic();stop=None
    def acquire(cid,obs,seed,arm,purpose='search'):
        guard(cid,obs,purpose,len(rows))
        if time.monotonic()-started>1700:raise TimeoutError('1800s stage reserve')
        folder=out/f'eval_{len(rows):03d}';folder.mkdir();config=configs[cid]
        row={'event_id':len(rows),'seed':seed,'arm':arm,'ordinal':len(obs)+1,'config_id':cid,'config':config,'purpose':purpose,'status':'charged','path':str(folder.relative_to(ROOT)),'charged_at_unix':time.time()};rows.append(row)
        atomic_json(folder/'spec.json',row)
        with (out/'charges.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
        compressed=folder/'output.knz';decoded=folder/'decoded.bin'
        commands={'compression':base+['-c','-i',str(source),'-o',str(compressed),'-x','-t',config['transform'],'-e',config['entropy'],'-b',str(config['block_bytes']),'-j','1','-v','3'],
                  'decompression':base+['-d','-i',str(compressed),'-o',str(decoded),'-j','1','-v','3']}
        atomic_json(folder/'commands.json',commands)
        def monitor(pid):
            memory=rss(pid);scratch=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
            return {'rss_bytes':memory,'scratch_bytes':scratch},('rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>128*1024**2 else None)
        try:
            for phase,cmd in commands.items():
                row[phase]=run(cmd,cwd=ROOT,log_path=folder/f'{phase}.log',wall_cap=40,monitor=monitor,env=env)
                atomic_json(folder/'progress.json',row)
                if row[phase]['exit_code'] or row[phase]['termination_reason']:raise RuntimeError(phase+' failed')
                if phase=='compression':
                    with compressed.open('rb') as f:headerbytes=f.read(16)
                    header=parse_header(headerbytes);verify_settings(header,config,(folder/'compression.log').read_text())
                    row.update(header_hex=headerbytes.hex(),stream_header=header,compressed_bytes=compressed.stat().st_size,compressed_sha256=sha(compressed))
            check=time.monotonic();assert byte_equal(source,decoded),'Exact decompression mismatch'
            row.update(input_sha256=sourcehash,decoded_sha256=sha(decoded),decoded_bytes=decoded.stat().st_size,exact_byte_equality=True,verification_seconds=time.monotonic()-check,status='valid')
            atomic_json(folder/'result.json',row)
            # Remove only this trial's validated bulky products; retain hashes, raw header and logs.
            compressed.unlink();decoded.unlink()
            atomic_json(folder/'retention.json',{'removed_after_validation':['output.knz','decoded.bin'],'raw_header_and_sha256_retained':True})
        except Exception as exc:
            row.update(status='failed',error=repr(exc));atomic_json(folder/'result.json',row);raise
        finally:atomic_json(out/'acquisitions.json',rows)
        return {'config_id':cid,'compressed_bytes':row['compressed_bytes'],'event_id':row['event_id']}
    try:
        for seed in SEEDS:
            prefix=[]
            for cid in random.Random(seed).sample(range(len(configs)),4):prefix.append(acquire(cid,prefix,seed,'prefix'))
            while len(prefix)<10:prefix.append(acquire(choose(x,prefix,'nn',seed),prefix,seed,'prefix'))
            path=out/f'prefix_{seed}.json';atomic_json(path,prefix)
            case={'seed':seed,'prefix_sha256':sha(path),'arms':{m:[dict(o) for o in prefix] for m in METHODS},'confirmation':{m:[] for m in METHODS},'decisions':[]};cases.append(case)
            rngs={m:random.Random(seed+1000) for m in METHODS};order_rng=random.Random(seed+75000)
            for step in range(7):
                order=list(METHODS);order_rng.shuffle(order)
                for method in order:
                    obs=case['arms'][method];begin=time.monotonic();cid=choose(x,obs,method,seed,rngs[method])
                    case['decisions'].append({'method':method,'step':step,'config_id':cid,'seconds':time.monotonic()-begin,'observed_events':[o['event_id'] for o in obs]})
                    obs.append(acquire(cid,obs,seed,method));atomic_json(out/f'case_{seed}.json',case)
            selected={m:min(case['arms'][m],key=lambda o:(o['compressed_bytes'],o['config_id']))['config_id'] for m in METHODS};case['selected_config_ids']=selected
            for rep in range(3):
                order=list(METHODS);order_rng.shuffle(order)
                for method in order:
                    confirmation=case['confirmation'][method];confirmation.append(acquire(selected[method],case['arms'][method]+confirmation,seed,method,'confirmation'));atomic_json(out/f'case_{seed}.json',case)
            print('seed',seed,'complete;',len(rows),'physical trials',flush=True)
    except Exception as exc:
        stop=repr(exc);atomic_json(out/'failure.json',{'error':stop,'charged_evaluations':len(rows)})
    finally:
        atomic_json(out/'summary.json',{'intended_physical_evaluations':200,'charged_evaluations':len(rows),'successful_evaluations':sum(r['status']=='valid' for r in rows),'unattempted':200-len(rows),'complete':stop is None and len(rows)==200,'stop_reason':stop,'seconds':time.monotonic()-started,'new_model_requests':0,'independent_families':1,'cases':cases})
    if stop:sys.exit(1)
if __name__=='__main__':main()
