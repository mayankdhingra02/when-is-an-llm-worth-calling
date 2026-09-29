"""One charged physical compression attempt; parent owns process-group timeout."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
from codec_api_v51 import Codec
from utility_v50 import frame_fields
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.live_compression_v17 import commands
spec=json.loads(sys.stdin.read());payload=(ROOT/spec['workload_path']).read_bytes();assert hashlib.sha256(payload).hexdigest()==spec['workload_sha256']
setting=spec['setting'];family=setting['family'];codec=Codec(family,spec['library']) if spec['mode']=='api' else None
compress,decompress=commands(setting,spec['binary'])
start=time.perf_counter_ns()
if codec:blob=codec.compress(payload,setting)
else:blob=subprocess.run(compress,input=payload,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=2).stdout
elapsed=time.perf_counter_ns()-start
actual=subprocess.run(decompress,input=blob,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=2).stdout
assert actual==payload,'Roundtrip mismatch';fields=frame_fields(family,blob);assert fields['content_checksum']
if family=='lz4':assert fields['independent_blocks']
out=ROOT/'artifacts/sources/live_v51/outputs'/f"trial_{spec['trial_id']:04d}.bin";out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists();out.write_bytes(blob)
print(json.dumps({'compression_ns':elapsed,'compressed_bytes':len(blob),'compressed_sha256':hashlib.sha256(blob).hexdigest(),'compressed_path':str(out.relative_to(ROOT)),'decoded_sha256':hashlib.sha256(actual).hexdigest(),'roundtrip_equal':True,'frame':fields,'timing_scope':'native API allocation, compression and output copy' if codec else 'CLI startup, pipes and compression'}))
