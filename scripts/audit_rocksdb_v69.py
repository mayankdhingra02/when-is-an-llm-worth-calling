"""Post-collection validity audit; source receipts remain immutable."""
import hashlib,json,struct,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.rocksdb_binding_v69 import active_readback

def compute():
    start=time.monotonic();data=ROOT/'data/generated_v69'
    blob=(data/'values.bin').read_bytes();trace=struct.iter_unpack('<I',(data/'trace.bin').read_bytes())
    digest=hashlib.sha256()
    for offset,(i,) in enumerate(trace):
        if offset>=10000:digest.update(blob[i*1000:(i+1)*1000])
    expected=digest.hexdigest()
    h=hashlib.sha256()
    for i in sorted(range(65536),key=lambda i:('user'+str(i)).encode()):
        h.update(('user'+str(i)).encode());h.update(blob[i*1000:(i+1)*1000])
    scan_digest=h.hexdigest();cases=[]
    for folder in sorted((ROOT/'results/v69_1_rocksdb_feasibility').glob('trial_*')):
        result=json.loads((folder/'result.json').read_text())
        assert result['timed_response_sha256']==expected
        for phase in ['initial_validation','final_validation']:
            assert result[phase]=={'records':65536,'sha256_in_engine_key_order':scan_digest}
        assert result['successful_timed_reads']==result['verified_timed_reads']==100000
        try:
            applied=active_readback(folder/'db',result['config']);status='settings_match'
        except ValueError as exc:applied={'error':str(exc)};status='invalid_configuration'
        cases.append({'trial':folder.name,'data_integrity_verified':True,'configuration_status':status,
            'active_readback':applied,'requested':result['config'],'timing_seconds_as_collected':result['objective_verified_loop_seconds']})
    old=json.loads((ROOT/'results/v69_rocksdb_feasibility/summary.json').read_text())
    assert old['attempted']==1 and old['valid']==0
    return {'cases':cases,'physical_attempts_total':4,'serialized_complete_receipts':3,
        'data_correct_completed_receipts':3,'configuration_valid_completed_receipts':sum(c['configuration_status']=='settings_match' for c in cases),
        'contrast_admitted':False,'optimization_admitted':False,
        'supersedes_raw_valid_flags':True,'failed_serialization_objective_timing':None,
        'expected_timed_response_sha256':expected,'expected_full_scan_sha256':scan_digest,
        'no_new_database_queries':True,'no_new_model_requests':True,'seconds':time.monotonic()-start}

if __name__=='__main__':
    out=ROOT/'results/v69_validity_audit';out.mkdir(exist_ok=False)
    result=compute();(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
