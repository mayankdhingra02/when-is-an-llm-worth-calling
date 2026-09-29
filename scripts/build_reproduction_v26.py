"""Deterministic focused reconstruction bundle; local files only."""
import argparse,hashlib,json
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Preserve archive; select a new path')
    names=set(json.loads((ROOT/'reports/protocol_v25_shortlist.freeze.json').read_text())['sha256'])
    names.update(['BUNDLE_V26_README.md','THIRD_PARTY.md','requirements.lock.txt','reports/shortlist_v25.md',
      'reports/reproduction_v26.md','reports/protocol_v25_shortlist.freeze.json','scripts/verify_reproduction_v26.py',
      'scripts/build_reproduction_v26.py','scripts/render_shortlist_v25.py','tests/synthetic/test_reproduction_v26.py',
      'results/v22_larger/requests.jsonl','results/v22_larger/request_starts.jsonl','results/v22_larger/model_runtime.json',
      'artifacts/model_manifest_v22.json','models/Qwen2.5-1.5B-Instruct/tokenizer.json','models/Qwen2.5-1.5B-Instruct/LICENSE',
      'artifacts/reproduction_v26/tests.log','artifacts/reproduction_v26/staging_replay.json',
      'artifacts/reproduction_v26/second_runtime_replay.json','artifacts/reproduction_v26/tamper_checks.json',
      'artifacts/sources/registry_v5/ChristianKaltenecker__PerformanceEvolution_Website/LICENSE'])
    for d in json.loads((ROOT/'data/manifest_v8.json').read_text())['datasets']:names.update(d['evidence'])
    for base in ['results/v25_shortlist','artifacts/study_v25']:
        names.update(p.relative_to(ROOT).as_posix() for p in (ROOT/base).rglob('*') if p.is_file())
    files={name:(ROOT/name).read_bytes() for name in sorted(names)}
    files['README.md']=files['BUNDLE_V26_README.md']
    manifest={'scope':'Focused independent V25 saved-result reconstruction; no fresh inference',
       'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in files.items()},
       'excluded':['model weights','installed dependencies','other studies not required by this reconstruction','physical workload/payload bytes','credentials and Git metadata']}
    files['REPRODUCTION_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(args.output,'x',compression=ZIP_DEFLATED,compresslevel=9) as archive:
        for n,b in sorted(files.items()):
            info=ZipInfo('llm-escalation-v25-reproduction/'+n,date_time=(2026,9,24,0,0,0));info.external_attr=0o100644<<16
            archive.writestr(info,b,compress_type=ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'archive':str(args.output),'bytes':args.output.stat().st_size,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),'included_files':len(manifest['files'])},indent=2))

if __name__=='__main__':main()
