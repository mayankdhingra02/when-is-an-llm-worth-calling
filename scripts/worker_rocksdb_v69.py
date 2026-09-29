"""One physical configuration trial with exact payload checking on every read."""
import hashlib,json,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'.local-runtime/rocksdb-v69')]
from escalation.rocksdb_v69 import RECORDS,READS,WARMUP,VALUE_LENGTH,options,verify_value,readback
from rocksdict import Rdict

def execute(spec, out):
    start=time.monotonic();source=ROOT/'data/generated_v69'
    blob=(source/'values.bin').read_bytes();assert len(blob)==RECORDS*VALUE_LENGTH
    expected=[blob[i*VALUE_LENGTH:(i+1)*VALUE_LENGTH] for i in range(RECORDS)]
    keys=[('user'+str(i)).encode() for i in range(RECORDS)]
    requests=struct.unpack('<'+'I'*(READS+WARMUP),(source/'trace.bin').read_bytes())
    config=spec['config'];opt,cache=options(config);dbpath=out/'db'
    db=Rdict(str(dbpath),opt);load_start=time.monotonic()
    for k,v in zip(keys,expected):db[k]=v
    db.flush();db.flush_wal(True)
    load_seconds=time.monotonic()-load_start
    def verify_all(db):
        h=hashlib.sha256();count=0
        for k,v in db.items():
            assert k.startswith(b'user') and k[4:].isdigit()
            i=int(k[4:]);assert 0<=i<RECORDS and k==keys[i]
            verify_value(v,expected[i]);h.update(k);h.update(v);count+=1
        assert count==RECORDS
        return {'records':count,'sha256_in_engine_key_order':h.hexdigest()}
    before=verify_all(db);db.close();del db, opt, cache
    # Fresh application block cache, OS page cache deliberately not flushed.
    opt,cache=options(config);db=Rdict(str(dbpath),opt)
    applied=readback(dbpath,config)
    warm_start=time.monotonic()
    for i in requests[:WARMUP]:verify_value(db[keys[i]],expected[i])
    warm_seconds=time.monotonic()-warm_start
    read_start=time.perf_counter_ns();native_call_ns=0;digest=hashlib.sha256()
    for i in requests[WARMUP:]:
        before_get=time.perf_counter_ns();value=db[keys[i]];native_call_ns+=time.perf_counter_ns()-before_get
        verify_value(value,expected[i]);digest.update(value)
    elapsed_ns=time.perf_counter_ns()-read_start
    after=verify_all(db);assert before==after
    usage=cache.get_usage();files=db.live_files();db.close()
    return {'status':'valid','config':config,'applied':applied,'records_loaded':RECORDS,
        'initial_validation':before,'final_validation':after,'warmup_reads':WARMUP,
        'successful_timed_reads':READS,'verified_timed_reads':READS,
        'timed_response_sha256':digest.hexdigest(),'load_seconds':load_seconds,
        'warmup_seconds':warm_seconds,'objective_verified_loop_seconds':elapsed_ns/1e9,
        'diagnostic_get_call_seconds':native_call_ns/1e9,'total_worker_seconds':time.monotonic()-start,
        'cache_usage_bytes':usage,'live_sst_files':files,'model_requests':0}

if __name__=='__main__':
    specpath=Path(sys.argv[1]);out=specpath.parent;spec=json.loads(specpath.read_text())
    try:result=execute(spec,out)
    except Exception as exc:
        result={'status':'failed','error':repr(exc),'traceback':traceback.format_exc()}
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');raise
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
