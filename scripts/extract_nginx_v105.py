"""Reproduce safe extraction from the preserved official owner archive."""
import argparse,hashlib,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--destination',type=Path,default=ROOT/'.local-runtime/nginx-v105');args=ap.parse_args()
    archive=ROOT/'artifacts/sources/v105/nginx-1.28.3.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()=='2c96a946bfb0882a21744ed429770a2123ae1828c7c48665092993ddee91a918'
    with tarfile.open(archive) as t:
        members=t.getmembers()
        for m in members:
            p=Path(m.name)
            if p.is_absolute() or '..' in p.parts or p.parts[0]!='nginx-1.28.3' or not (m.isfile() or m.isdir()):raise ValueError(m.name)
        assert sum(m.size for m in members)<30*1024**2
        args.destination.mkdir(parents=True,exist_ok=False)
        t.extractall(args.destination)
    print('Extracted pinned source; no source code executed.')
