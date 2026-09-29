"""Seal V89 failure, V90 control screen and V91 resource proposal with exact older scientific records preserved."""
import argparse,json
from datetime import datetime,timezone
from seal_frontier_v86 import ROOT,sha,read
ART=ROOT/'artifacts/study_v90'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v88/evidence_manifest.json'
    assert sha(m)=='105e39d72641ecd97ecb6f0bc2aa390ed6a7c23567c7634850ce0353c5cc4e42'
    stages=read(m)['historical']+[{'stage':'v88_flights_feasibility','manifest_sha256':sha(m),'redirects':{}}]
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
    freeze=ROOT/'reports/protocol_v90.freeze.json'
    pins=read(ROOT/'reports/protocol_v89.freeze.json')['sha256'] | read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','reports/flights_v90.md','reports/protocol_v90.freeze.json','scripts/report_flights_v89.py','scripts/report_flights_v90.py','scripts/audit_flights_v89_failure.py','scripts/seal_flights_v90.py','artifacts/study_v88/evidence_manifest.json','reports/resources_v91.md','configs/resource_proposal_v91.json','scripts/check_resources_v91.py','tests/synthetic/test_resources_v91.py']}
    for d in [ART,ROOT/'artifacts/study_v89',ROOT/'artifacts/study_v91',ROOT/'results/v89_flights_grid',ROOT/'results/v89_flights_failure_audit',ROOT/'results/v90_flights_grid',ROOT/'results/v90_flights_analysis']:paths.update(f for f in d.rglob('*') if f.is_file())
    paths={f for f in paths if f!=manifest and f.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in f.parts}
    manifest.write_text(json.dumps({'scope':'V89 retained failed screen, V90 completed exploratory control grid, V91 proposed resource change only; no new model calls','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(f.relative_to(ROOT)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
