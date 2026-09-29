"""Seal the source-only V73 audit while preserving all V72 execution evidence."""
import argparse
import json
from datetime import datetime, timezone
from seal_v72_execution import ROOT, sha, read, history as older_history
from audit_admission_v73 import audit

ART=ROOT/'artifacts/study_v73'

def history():
    prior=older_history();manifest=ROOT/'artifacts/study_v72_execution/evidence_manifest.json'
    assert sha(manifest)=='25ee08272cc5537cb115ac748163fdd435a727e401e5ae0f800c8ededa0a5e46'
    files=read(manifest)['files'];mapping=read(ART/'previous_snapshot/mapping.json');redirects={}
    for name,meta in files.items():
        path=ROOT/name
        if path.exists() and sha(path)==meta['sha256']:continue
        assert name in mapping,name
        path=ROOT/mapping[name]['snapshot_path'];assert sha(path)==meta['sha256'],name
        redirects[name]=str(path.relative_to(ROOT))
    return prior+[{'stage':'v72_execution','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args()
    hist=history();result=audit();assert result==read(ROOT/'results/v73_admission/summary.json')
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,meta in data['files'].items():
            path=ROOT/name;assert sha(path)==meta['sha256'] and path.stat().st_size==meta['bytes'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'audit_reproduced':True,'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v72_execution/evidence_manifest.json']}
        for pattern in ['artifacts/study_v73/**/*','artifacts/sources/v73/**/*','results/v73*/**/*','scripts/*v73.py','src/escalation/*v73.py','tests/**/*v73.py','reports/*v73*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'scope':'v73_source_only_admission','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,
              'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
