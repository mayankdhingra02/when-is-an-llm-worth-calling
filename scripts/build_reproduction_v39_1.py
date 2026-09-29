"""Deterministic allowlisted local V38 evidence archive; no downloads."""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('Preserve archive')
    names={'reports/protocol_v39_1_reproduction.freeze.json','reports/protocol_v39_reproduction.freeze.json','reports/protocol_v38_size_prompt.freeze.json',
           'reports/protocol_v35_1_reproduction.freeze.json','scripts/verify_reproduction_v39.py','scripts/build_reproduction_v39_1.py',
           'scripts/verify_reproduction_v35_1.py','BUNDLE_V39_README.md','reports/size_prompt_v38.md','THIRD_PARTY.md',
           'artifacts/model_manifest_v22.json','results/v22_larger/request_starts.jsonl','results/v22_larger/model_runtime.json','models/Qwen2.5-1.5B-Instruct/tokenizer.json','models/Qwen2.5-1.5B-Instruct/LICENSE',
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
                if hashlib.sha256((ROOT/dep).read_bytes()).hexdigest()!=h:raise ValueError('Frozen dependency changed: '+dep)
            names.update(frozen)
    files={}
    for n in sorted(names):
        path=PurePosixPath(n)
        if path.is_absolute() or '..' in path.parts or (ROOT/n).is_symlink():raise ValueError('Unsafe path')
        if any(x in path.parts for x in ('.git','.venv','__pycache__')) or n.endswith('.safetensors'):raise ValueError('Disallowed payload')
        files[n]=(ROOT/n).read_bytes()
    files['README.md']=files['BUNDLE_V39_README.md']
    manifest={'scope':'V38 saved-evidence reconstruction; V35.1 historical replay; no fresh inference',
              'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(files.items())},
              'excluded':['model weights','installed environments','credentials','Git metadata','fresh inference','physical payloads']}
    files['REPRODUCTION_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(a.output,'x',compression=ZIP_DEFLATED,compresslevel=9) as z:
        for n,b in sorted(files.items()):
            info=ZipInfo('llm-escalation-v38-reproduction/'+n,date_time=(2026,9,25,0,0,0));info.external_attr=0o100644<<16
            z.writestr(info,b,compress_type=ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'archive':str(a.output),'bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),
                     'included_files':len(manifest['files']),'included_freezes':sorted(scanned)},indent=2))
if __name__=='__main__':main()
