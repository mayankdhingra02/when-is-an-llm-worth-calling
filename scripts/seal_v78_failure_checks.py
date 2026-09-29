"""Seal pre-execution synthetic checks; frozen V78 collection remains unchanged."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v77 import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v78_failure_checks'
def history():
    prior=older_history();manifest=ROOT/'artifacts/study_v77/evidence_manifest.json'
    assert sha(manifest)=='d2b5c80927713fee054be41678f98ed5b28a739c21a1b4c49f5aab525396cb46'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for n,m in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==m['sha256']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==m['sha256'],n
        redirects[n]=str(p.relative_to(ROOT))
    return prior+[{'stage':'v77','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    hist=history();pins=read(ART/'supplementary_code_pins.json')
    assert sha(ROOT/'reports/protocol_v78.freeze.json')==pins['original_freeze_sha256']
    for n,d in pins['sha256'].items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'collection_freeze_unchanged':True,'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        names=['STATUS.md','README.md','reports/next_experiment.md','reports/validation_v78_addendum.md','scripts/seal_v78_failure_checks.py','artifacts/study_v77/evidence_manifest.json']+list(pins['sha256'])
        paths={ROOT/n for n in names};paths.update(p for p in ART.rglob('*') if p.is_file())
        paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        manifest.write_text(json.dumps({'scope':'synthetic_preexecution_failure_and_receipt_checks_only','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n')
        print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
