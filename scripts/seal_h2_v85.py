"""Seal prepared H2 inference scope and genuine zero-generation preflight."""
import argparse,json
from datetime import datetime,timezone
from seal_h2_v84 import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v85'
def history():
    hist=older_history();manifest=ROOT/'artifacts/study_v84/evidence_manifest.json';assert sha(manifest)=='6f7bedeecee6bc6aab3b00ea5d0807bcf164c4fbe7557c2ac1043387bb6f2b8b'
    mapping=read(ART/'previous_snapshot/mapping.json');redirects={};files=read(manifest)['files']
    for n,m in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==m['sha256'] and p.stat().st_size==m['bytes']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],n
        redirects[n]=str(p.relative_to(ROOT))
    return hist+[{'stage':'v84_h2_classical','verified_files':len(files),'manifest_sha256':sha(manifest),'redirects':redirects}]
def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args();hist=history();freeze=ROOT/'reports/protocol_v85.freeze.json';assert sha(freeze)=='e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17'
    pins=read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+['STATUS.md','README.md','reports/next_experiment.md','reports/readiness_v85.md','scripts/seal_h2_v85.py','scripts/check_h2_v85_gate.py','scripts/write_h2_v85_checkpoint.py','reports/protocol_v85.freeze.json','artifacts/study_v84/evidence_manifest.json']}
    paths.update(p for p in ART.rglob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope':'V85 prepared real-model experiment; actual template/tokenization only, no new generation or objective evaluation','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
