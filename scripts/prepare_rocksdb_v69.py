"""Create fixed inputs and all nominal feature vectors, before physical outcomes."""
import hashlib,json,struct,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.rocksdb_v69 import RECORDS,READS,WARMUP,grid,payload,trace
if __name__=='__main__':
    start=time.monotonic();out=ROOT/'data/generated_v69';out.mkdir(exist_ok=False)
    with (out/'values.bin').open('wb') as f:
        for i in range(RECORDS):
            if time.monotonic()-start>180:raise TimeoutError('input preparation cap')
            f.write(payload(i))
    requests=trace();(out/'trace.bin').write_bytes(struct.pack('<'+'I'*len(requests),*requests))
    (out/'grid.json').write_text(json.dumps(grid(),indent=2)+'\n')
    manifest={'records':RECORDS,'timed_reads':READS,'warmup_reads':WARMUP,'nominal_configurations':len(grid()),'all_configs_physically_validated':False,
       'request_seed':69001,'seconds':time.monotonic()-start,'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.iterdir())}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
