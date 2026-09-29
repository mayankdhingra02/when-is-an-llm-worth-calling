"""Seal authorized real V85 evidence without replacing historical snapshots."""
import argparse,json
from datetime import datetime,timezone
from seal_h2_v85_blocked import ROOT,sha,read
ART=ROOT/'artifacts/study_v85_execution'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v85_blocked/evidence_manifest.json'
    assert sha(m)=='93d66fa26918f42a18fff3e6999f0ada344019be70608c1499490949c53db89b'
    stages=read(m)['historical']+[{'stage':'v85_permission_blocker_before_explicit_grant','manifest_sha256':sha(m),'redirects':{}}]
    manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')}
    mapping=read(ART/'previous_snapshot/mapping.json');verified=[];cache={}
    def matches(p,meta):
        if not p.exists() or p.stat().st_size!=meta['bytes']:return False
        if p not in cache:cache[p]=sha(p)
        return cache[p]==meta['sha256']
    for stage in stages:
        if 'manifest_sha256' not in stage:
            assert stage=={'stage':'v78_blocked_checkpoint','audit_status_verified':True}
            audit=read(ROOT/'artifacts/study_v78_blocked/audit.json')
            assert sha(ROOT/'artifacts/study_v78_execution/previous_snapshot/STATUS.md')==audit['status_sha256']
            assert sha(ROOT/'artifacts/study_v78_blocked/previous_snapshot/STATUS.md')==audit['previous_status_sha256']
            verified.append(stage);continue
        manifest=manifests[stage['manifest_sha256']];files=read(manifest)['files'];redirects={}
        for n,meta in files.items():
            candidates=[ROOT/n]
            if n in stage['redirects']:candidates.append(ROOT/stage['redirects'][n])
            if n in mapping:candidates.append(ROOT/mapping[n]['snapshot_path'])
            resolved=next((p for p in candidates if matches(p,meta)),None)
            assert resolved is not None,(stage['stage'],n)
            if resolved!=ROOT/n:redirects[n]=str(resolved.relative_to(ROOT))
        verified.append({'stage':stage['stage'],'verified_files':len(files),'manifest_sha256':sha(manifest),'redirects':redirects})
    return verified
def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args();hist=history()
    freeze=ROOT/'reports/protocol_v85.freeze.json';assert sha(freeze)=='e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17'
    pins=read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+['STATUS.md','README.md','reports/next_experiment.md','reports/h2_v85.md','scripts/report_h2_v85.py','scripts/seal_h2_v85_execution.py','reports/protocol_v85.freeze.json','artifacts/study_v85_blocked/evidence_manifest.json']}
    for d in [ART,ROOT/'results/v85_h2_paired',ROOT/'results/v85_h2_analysis']:paths.update(f for f in d.rglob('*') if f.is_file())
    paths={f for f in paths if f!=manifest and f.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in f.parts}
    manifest.write_text(json.dumps({'scope':'Authorized frozen real H2 model continuation; all seeds, no fitted router','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(f.relative_to(ROOT)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
