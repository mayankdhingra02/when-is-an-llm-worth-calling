"""Isolated saved-analysis replay; requires only Python3.10+ standard library."""
import hashlib,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from analyze_frontier_v86 import normalize,analyze

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for n,m in manifest['files'].items():
        p=ROOT/n;assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],n
    freeze=json.loads((ROOT/'reports/protocol_v86.freeze.json').read_text())
    for n,d in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==d,n
    with tempfile.TemporaryDirectory(prefix='frontier-v86-') as td:
        out=Path(td);result=analyze(normalize(ROOT),out)
        for p in out.iterdir():assert p.read_bytes()==(ROOT/'results/v86_frontier'/p.name).read_bytes(),p.name
    print(json.dumps({'verified':True,'families':3,'cases':25,'masks':sum(r['mask_count'] for r in result),'scope':'saved-summary exact reconstruction; no native/model/optimizer execution'}))
if __name__=='__main__':main()
