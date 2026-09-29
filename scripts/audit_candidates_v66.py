"""Identifier-only exposure audit; raw objective tables are never opened."""
import hashlib,json,re,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    t=time.monotonic();out=ROOT/'artifacts/study_v66/exposure.json';assert not out.exists()
    patterns={'duckdb':re.compile(rb'(?<![a-z])duckdb(?![a-z])',re.I),'gnu_sort':re.compile(rb'gnu[ _-]sort|coreutils|gnusort',re.I),'openjpeg':re.compile(rb'openjpeg|openjp2|opj_compress',re.I)}
    paths=set((ROOT/'results').rglob('*.json'))|set((ROOT/'results').rglob('*.jsonl'))|set((ROOT/'data').glob('*manifest*.json'))
    hits=[];total=0
    for p in sorted(paths):
        if time.monotonic()-t>120:raise TimeoutError('120s audit cap')
        data=p.read_bytes();total+=len(data)
        found=[k for k,pattern in patterns.items() if pattern.search(data)]
        if found:hits.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'groups':found})
    result={'scanned_files':len(paths),'scanned_bytes':total,'hits':hits,'seconds':time.monotonic()-t,'scope':'saved research JSON/JSONL and top-level data manifests only','untouched_outcomes_certified':False,'blind_spots':['deleted or external records','unidentified aliases','unstructured/binary files'],'new_objective_accesses':0,'model_requests':0}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
