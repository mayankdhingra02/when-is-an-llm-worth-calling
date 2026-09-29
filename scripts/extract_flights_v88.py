"""Allowlisted data extraction without tar/zip path traversal or package code."""
import hashlib,io,json,tarfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/flights_v88'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=ROOT/'artifacts/sources/v88/nycflights13-0.0.3.tar.gz';assert sha(source)=='d9ef2f5cf1bebca7e30b4daf69dcd7a8fd71f25b7196f5dc489879ad7e3e8a37';OUT.mkdir(exist_ok=False)
    prefix='nycflights13-0.0.3/';spent=0;files={}
    with tarfile.open(source,'r:gz') as t:
        for name in ['PKG-INFO','README.md','nycflights13/data/airlines.csv','nycflights13/data/airports.csv','nycflights13/data/planes.csv','nycflights13/data/flights.csv.zip']:
            m=t.getmember(prefix+name);assert m.isfile() and m.size<=10*1024**2
            body=t.extractfile(m).read();assert len(body)==m.size
            if name.endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(body)) as z:
                    entries=[i for i in z.infolist() if i.filename=='flights.csv'];assert len(entries)==1 and entries[0].file_size<=64*1024**2
                    body=z.read(entries[0]);assert len(body)==entries[0].file_size;dest=OUT/'flights.csv'
            else:dest=OUT/Path(name).name
            spent+=len(body);assert spent<=80*1024**2;dest.write_bytes(body);files[str(dest.relative_to(ROOT))]={'sha256':sha(dest),'bytes':len(body),'archive_member':prefix+name}
    assert 'License: CC0' in (OUT/'PKG-INFO').read_text()
    (ROOT/'artifacts/study_v88/data_extraction.json').write_text(json.dumps({'source_archive_sha256':sha(source),'executed_package_code':False,'uncompressed_bytes':spent,'files':files},indent=2)+'\n')
    for p in OUT.glob('*.csv'):
        with p.open() as f:print(p.name,f.readline().strip(),f.readline().strip())
if __name__=='__main__':main()
