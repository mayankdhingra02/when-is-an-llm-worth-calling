"""V70 measurement, ephemeral DB data; retain every receipt and engine log."""
import hashlib,json,shutil,sys,tempfile,time,traceback
from pathlib import Path
from worker_rocksdb_v70 import execute,ROOT
from escalation.receipts_v70 import atomic_json

if __name__=='__main__':
    specpath=Path(sys.argv[1]);out=specpath.parent;spec=json.loads(specpath.read_text())
    scratch=ROOT/'.scratch-v71';scratch.mkdir(exist_ok=True)
    start=time.monotonic();result=None
    with tempfile.TemporaryDirectory(prefix='owned-',dir=scratch) as directory:
        work=Path(directory)
        try:result=execute(spec,work)
        except Exception as exc:result={'status':'failed','error':repr(exc),'traceback':traceback.format_exc()}
        finally:
            for path in work.glob('*.json'):shutil.copyfile(path,out/path.name)
            retained=out/'db';retained.mkdir()
            if (work/'db').exists():
                inventory={}
                for path in sorted((work/'db').iterdir()):
                    if not path.is_file():continue
                    h=hashlib.sha256()
                    with path.open('rb') as f:
                        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
                    inventory[path.name]={'bytes':path.stat().st_size,'sha256':h.hexdigest()}
                    if path.name.startswith(('LOG','OPTIONS','MANIFEST','CURRENT','IDENTITY')) or path.suffix=='.json':
                        shutil.copyfile(path,retained/path.name)
                atomic_json(out/'database_file_inventory.json',inventory)
            result['data_files_retained']=False
            result['archive_worker_seconds']=time.monotonic()-start
            atomic_json(out/'result.json',result)
    if result['status']!='valid':sys.exit(1)
