"""One charged physical compression trial; parent owns timeout/process group."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.live_compression_v15 import measure
spec=json.loads(sys.stdin.read())
payload=(ROOT/spec['workload_path']).read_bytes()
assert hashlib.sha256(payload).hexdigest()==spec['workload_sha256']
result,compressed=measure(spec['setting'],payload,spec.get('binary'))
output=ROOT/'artifacts/sources/live_v15/outputs'/f"trial_{spec['trial_id']:04d}.bin"
output.parent.mkdir(parents=True,exist_ok=True)
if output.exists():raise FileExistsError('Refusing to overwrite physical evidence')
output.write_bytes(compressed)
result['compressed_path']=str(output.relative_to(ROOT))
print(json.dumps(result))
