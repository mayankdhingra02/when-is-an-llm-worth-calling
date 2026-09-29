"""Seal supplementary analyzer tests, retaining the unchanged prepared study."""
import argparse,json
from datetime import datetime,timezone
from seal_h2_v85 import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v85_validation'
def history():
    hist=older_history();manifest=ROOT/'artifacts/study_v85/evidence_manifest.json';assert sha(manifest)=='a24b79c920c3b5731ed991bb14f35948106bff7fa60ee378f56880bd49069e7e'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for n,m in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==m['sha256'] and p.stat().st_size==m['bytes']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],n;redirects[n]=str(p.relative_to(ROOT))
    return hist+[{'stage':'v85_preparation','verified_files':len(files),'manifest_sha256':sha(manifest),'redirects':redirects}]
def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args();hist=history();manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in ['STATUS.md','README.md','reports/validation_v85.md','tests/synthetic/test_h2_v85_analyzer.py','scripts/check_h2_v85_analyzer_checkpoint.py','scripts/seal_h2_v85_validation.py','artifacts/study_v85/evidence_manifest.json']}
    paths.update(p for p in ART.rglob('*') if p.is_file());paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
    manifest.write_text(json.dumps({'scope':'synthetic analyzer acceptance/rejection only; no real model/native collection','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
