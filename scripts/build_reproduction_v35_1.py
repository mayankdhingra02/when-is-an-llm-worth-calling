"""Deterministic local V34 reconstruction archive; recursive frozen dependencies."""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('Preserve existing archive')
    names={'reports/protocol_v34_constrained.freeze.json','reports/protocol_v35_1_reproduction.freeze.json',
        'reports/constrained_v34.md','BUNDLE_V35.1_README.md','THIRD_PARTY.md','scripts/build_reproduction_v35_1.py','scripts/verify_reproduction_v35_1.py',
        'results/v22_larger/request_starts.jsonl','results/v22_larger/model_runtime.json','artifacts/model_manifest_v22.json',
        'models/Qwen2.5-1.5B-Instruct/tokenizer.json','models/Qwen2.5-1.5B-Instruct/LICENSE',
        'artifacts/sources/registry_v5/ChristianKaltenecker__PerformanceEvolution_Website/LICENSE'}
    for d in json.loads((ROOT/'data/manifest_v8.json').read_text())['datasets']:names.update(d['evidence'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'results/v34_constrained').rglob('*') if p.is_file())
    scanned=set()
    while True:
        pending=[n for n in names if n.endswith('.freeze.json') and n not in scanned]
        if not pending:break
        for n in pending:
            frozen=json.loads((ROOT/n).read_text())['sha256'];scanned.add(n)
            for dep,h in frozen.items():
                if hashlib.sha256((ROOT/dep).read_bytes()).hexdigest()!=h:raise ValueError('Changed frozen dependency: '+dep)
            names.update(frozen)
    files={}
    for n in sorted(names):
        path=PurePosixPath(n)
        if path.is_absolute() or '..' in path.parts or (ROOT/n).is_symlink():raise ValueError('Unsafe/nonregular input')
        files[n]=(ROOT/n).read_bytes()
    files['README.md']=files['BUNDLE_V35.1_README.md']
    manifest={'scope':'V34 constrained saved-result reconstruction with original response provenance; no fresh inference',
        'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(files.items())},
        'excluded':['model weights','installed environments','credentials','Git metadata','unrelated later studies','fresh inference and physical benchmarks']}
    files['REPRODUCTION_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(a.output,'x',compression=ZIP_DEFLATED,compresslevel=9) as archive:
        for n,b in sorted(files.items()):
            info=ZipInfo('llm-escalation-v34-reproduction/'+n,date_time=(2026,9,25,0,0,0));info.external_attr=0o100644<<16
            archive.writestr(info,b,compress_type=ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'archive':str(a.output),'bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),
        'included_files':len(manifest['files']),'included_freezes':sorted(scanned)},indent=2))

if __name__=='__main__':main()
