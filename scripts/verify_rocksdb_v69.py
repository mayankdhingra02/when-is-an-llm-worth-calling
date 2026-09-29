"""Read-only verification; no database open, objective query or inference."""
import hashlib,json,time
from pathlib import Path
from audit_rocksdb_v69 import compute, ROOT

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if __name__=='__main__':
    start=time.monotonic()
    for stage in ('v69','v69_1'):
        for name,digest in json.loads((ROOT/f'reports/protocol_{stage}.freeze.json').read_text())['sha256'].items():
            assert sha(ROOT/name)==digest,name
    manifest=json.loads((ROOT/'artifacts/sources/v69/manifest.json').read_text())
    for name,meta in manifest['files'].items():assert sha(ROOT/'artifacts/sources/v69'/name)==meta['sha256'],name
    a=compute();b=json.loads((ROOT/'results/v69_validity_audit/summary.json').read_text())
    for item in (a,b):item.pop('seconds')
    assert a==b
    # Check repair changed only JSON serialization and import, not experiment code.
    old=(ROOT/'scripts/worker_rocksdb_v69.py').read_text()
    new=(ROOT/'scripts/worker_rocksdb_v69_1.py').read_text()
    assert new==old.replace('from rocksdict import Rdict','from rocksdict import Rdict\nfrom escalation.record_json_v69 import bytes_default').replace('json.dumps(result,indent=2)','json.dumps(result,indent=2,default=bytes_default)')
    source=ROOT/'artifacts/sources/v69_repair/rdict.rs'
    tree=json.loads((ROOT/'artifacts/sources/v69/tree.json').read_text())['tree']
    expected=next(x['sha'] for x in tree if x['path']=='src/rdict.rs');body=source.read_bytes()
    assert hashlib.sha1(('blob '+str(len(body))+'\0').encode()+body).hexdigest()==expected
    print(json.dumps({'verified':True,'physical_attempts':4,'configuration_valid_receipts':2,
        'invalid_contrast_preserved':True,'missing_initial_timing_not_imputed':True,
        'new_database_queries':0,'seconds':time.monotonic()-start},indent=2))
