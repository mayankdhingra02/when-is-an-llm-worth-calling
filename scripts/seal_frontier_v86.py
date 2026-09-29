"""Seal V86 existing-data analysis and preserved native study history."""
import argparse,json
from datetime import datetime,timezone
from seal_h2_v85_execution import ROOT,sha,read
ART=ROOT/'artifacts/study_v86'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v85_execution/evidence_manifest.json'
    assert sha(m)=='8f06a35670d32544a4b1dd0db89c2224a202326d57cb5a4b333027efc8e679d6'
    stages=read(m)['historical']+[{'stage':'v85_completed_real_execution','manifest_sha256':sha(m),'redirects':{}}]
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
    freeze=ROOT/'reports/protocol_v86.freeze.json'
    pins=read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+['STATUS.md','README.md','reports/next_experiment.md','reports/frontier_v86.md','reports/source_followup_v86.md','reports/source_followup_v86_addendum.md','scripts/report_frontier_v86.py','scripts/replay_frontier_v86.py','scripts/bundle_frontier_v86.py','scripts/seal_frontier_v86.py','reports/protocol_v86.freeze.json','artifacts/study_v85_execution/evidence_manifest.json','output/frontier_v86_reproduction.zip','output/frontier_v86_1_reproduction.zip','artifacts/reproduction_v86/verification.json','artifacts/reproduction_v86_1/verification.json']}
    for d in [ART,ROOT/'results/v86_frontier']:paths.update(f for f in d.rglob('*') if f.is_file())
    paths={f for f in paths if f!=manifest and f.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in f.parts}
    manifest.write_text(json.dumps({'scope':'Exact retrospective control-aware frontier; no new measurements','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(f.relative_to(ROOT)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
