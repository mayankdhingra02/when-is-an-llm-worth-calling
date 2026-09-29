"""Seal V74 native feasibility and verify historical evidence via exact snapshots."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v73 import ROOT,sha,read,history as older_history
from analyze_kanzi_v74 import analyze
ART=ROOT/'artifacts/study_v74'

def history():
    prior=older_history();manifest=ROOT/'artifacts/study_v73/evidence_manifest.json'
    assert sha(manifest)=='7a84bef09f64bd51dd8eb8c83e4729ab1af99c3085d98874e7e757e0155f09e1'
    mapping=read(ART/'previous_snapshot/mapping.json');redirects={};files=read(manifest)['files']
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256']:continue
        assert name in mapping,name
        p=ROOT/mapping[name]['snapshot_path'];assert sha(p)==meta['sha256'],name
        redirects[name]=str(p.relative_to(ROOT))
    return prior+[{'stage':'v73','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    hist=history();rows,summary=analyze()
    assert rows==read(ROOT/'results/v74_kanzi_analysis/summary.json')['records']
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,meta in data['files'].items():
            p=ROOT/name;assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'replayed_trials':len(rows),'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v73/evidence_manifest.json']}
        for pattern in ['artifacts/study_v74/**/*','artifacts/sources/v74/**/*','results/v74*/**/*','scripts/*v74.py','src/escalation/*v74.py','tests/**/*v74.py','reports/*v74*','configs/*v74*','data/generated_v74/*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        paths.update(ROOT/n for n in read(ROOT/'reports/protocol_v74.freeze.json')['sha256'])
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'scope':'v74_native_correctness_resource_feasibility','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,
              'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
