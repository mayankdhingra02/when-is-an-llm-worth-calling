"""One physical configuration trial with exact payload checking on every read."""
import hashlib,json,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'src'),str(ROOT/'.local-runtime/rocksdb-v69')]
from escalation.rocksdb_v69 import RECORDS,READS,WARMUP,VALUE_LENGTH,options,verify_value,readback
from escalation.rocksdb_binding_v69 import open_configured, active_readback
from escalation.receipts_v70 import atomic_json
from escalation.record_json_v69 import bytes_default

def execute(spec, out):
    start=time.monotonic();source=ROOT/'data/generated_v69'
    blob=(source/'values.bin').read_bytes();assert len(blob)==RECORDS*VALUE_LENGTH
    expected=[blob[i*VALUE_LENGTH:(i+1)*VALUE_LENGTH] for i in range(RECORDS)]
    keys=[('user'+str(i)).encode() for i in range(RECORDS)]
    requests=struct.unpack('<'+'I'*(READS+WARMUP),(source/'trace.bin').read_bytes())
    config=spec['config'];dbpath=out/'db'
    progress={'phase':'starting','config':config}
    def save(phase, **fields):
        progress.update(phase=phase, **fields);atomic_json(out/'progress.json',progress)
        atomic_json(out/(phase+'.json'),progress)
    save('starting')
    db,cache=open_configured(dbpath,config);load_start=time.monotonic()
    creation_applied=active_readback(dbpath,config)
    for k,v in zip(keys,expected):db[k]=v
    db.flush();db.flush_wal(True)
    load_seconds=time.monotonic()-load_start
    save('loaded', records_loaded=RECORDS, load_seconds=load_seconds, creation_applied=creation_applied)
    def verify_all(db):
        h=hashlib.sha256();count=0
        for k,v in db.items():
            assert k.startswith(b'user') and k[4:].isdigit()
            i=int(k[4:]);assert 0<=i<RECORDS and k==keys[i]
            verify_value(v,expected[i]);h.update(k);h.update(v);count+=1
        assert count==RECORDS
        return {'records':count,'sha256_in_engine_key_order':h.hexdigest()}
    before=verify_all(db);save('initial_scan',initial_validation=before);db.close();del db,cache
    # Fresh application block cache, OS page cache deliberately not flushed.
    db,cache=open_configured(dbpath,config)
    applied=active_readback(dbpath,config)
    warm_start=time.monotonic()
    for i in requests[:WARMUP]:verify_value(db[keys[i]],expected[i])
    warm_seconds=time.monotonic()-warm_start
    warm_cache_usage=cache.get_usage()
    assert warm_cache_usage>0, 'supplied cache not attached'
    save('warmup',warmup_reads=WARMUP,warmup_seconds=warm_seconds,cache_usage_bytes=warm_cache_usage,applied=applied)
    read_start=time.perf_counter_ns();native_call_ns=0;digest=hashlib.sha256()
    for i in requests[WARMUP:]:
        before_get=time.perf_counter_ns();value=db[keys[i]];native_call_ns+=time.perf_counter_ns()-before_get
        verify_value(value,expected[i]);digest.update(value)
    elapsed_ns=time.perf_counter_ns()-read_start
    save('timed',successful_timed_reads=READS,verified_timed_reads=READS,objective_verified_loop_seconds=elapsed_ns/1e9,diagnostic_get_call_seconds=native_call_ns/1e9,timed_response_sha256=digest.hexdigest())
    after=verify_all(db);assert before==after
    save('final_scan',final_validation=after)
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
        atomic_json(out/'result.json',result);raise
    atomic_json(out/'result.json',result)
