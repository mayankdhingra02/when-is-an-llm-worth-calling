"""One charged physical trial; parent controls timeout and reaps process group."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.live_compression_v17 import measure
spec=json.loads(sys.stdin.read());payload=(ROOT/spec['workload_path']).read_bytes()
assert hashlib.sha256(payload).hexdigest()==spec['workload_sha256']
result,compressed=measure(spec['setting'],payload,spec.get('binary'))
path=ROOT/'artifacts/sources/live_v32/outputs'/f"trial_{spec['trial_id']:04d}.bin"
path.parent.mkdir(parents=True,exist_ok=True)
with path.open('xb') as stream:stream.write(compressed)
result['compressed_path']=str(path.relative_to(ROOT));print(json.dumps(result))
