"""Seal V98 interrupted reasoning evidence while preserving historical records."""
import argparse,json
from datetime import datetime,timezone
from collect_smollm_v47 import ROOT,read,write,sha
ART=ROOT/'artifacts/study_v98'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v97/evidence_manifest.json'
    assert sha(m)=='9c368dd80c6a0f19ee42d88a90ff6c553163a65de3cae8769c240291a1fce883'
    stages=read(m)['historical']+[{'stage':'v97_restricted_domain','manifest_sha256':sha(m),'redirects':{}}]
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
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    hist=history();manifest=ART/'evidence_manifest.json'
    for filename in ['reports/protocol_v98.freeze.json','artifacts/study_v98/report_pin_before_acquisition.json']:
        for n,h in read(ROOT/filename)['sha256'].items():assert sha(ROOT/n)==h,n
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical_checkpoints':len(hist)}));return
    assert not manifest.exists()
    names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','reports/protocol_v98.freeze.json','artifacts/study_v97/evidence_manifest.json']
    paths={ROOT/n for n in names}
    for folder in ['scripts','reports','configs','tests/synthetic','src/escalation']:
        paths.update(p for p in (ROOT/folder).glob('*v98*') if p.is_file())
    for folder in [ART,ROOT/'results/v98_reasoning',ROOT/'results/v98_analysis']:
        paths.update(p for p in folder.rglob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    write(manifest,{'scope':'V98 interrupted development reasoning attempt; missing usage retained; V97 complete evidence preserved','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
