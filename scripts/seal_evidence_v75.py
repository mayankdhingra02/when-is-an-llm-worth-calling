"""Seal incomplete V75 and verify prior evidence against exact snapshots."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v74 import ROOT,sha,read,history as older_history
from audit_kanzi_v75_failure import audit
ART=ROOT/'artifacts/study_v75'
def history():
    prior=older_history();manifest=ROOT/'artifacts/study_v74/evidence_manifest.json'
    assert sha(manifest)=='a1dfe594dd6c7c35ad900276c7fe9746db8a58da9cf77962d30079a450d88183'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256']:continue
        assert name in mapping,name
        p=ROOT/mapping[name]['snapshot_path'];assert sha(p)==meta['sha256'],name
        redirects[name]=str(p.relative_to(ROOT))
    return prior+[{'stage':'v74','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    hist=history();assert audit()==read(ROOT/'results/v75_failure_audit/summary.json')
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'acquisitions_replayed':9,'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v74/evidence_manifest.json']}
        for pattern in ['artifacts/study_v75/**/*','results/v75*/**/*','scripts/*v75*.py','src/escalation/*v75.py','tests/**/*v75.py','reports/*v75*','data/*v75*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        paths.update(ROOT/n for n in read(ROOT/'reports/protocol_v75.freeze.json')['sha256'])
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'scope':'v75_incomplete_classical_collection_application_failure','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,
              'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
