"""Seal V92 matched-model sensitivity diagnostic with exact older scientific records preserved."""
import argparse,json
from datetime import datetime,timezone
from seal_frontier_v86 import ROOT,read
from collect_smollm_v47 import sha
ART=ROOT/'artifacts/study_v92'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v91/evidence_manifest.json'
    assert sha(m)=='e1ac0e67df71c04e20316b4bc802622a80452c9622524aefaf97a533d10cd645'
    stages=read(m)['historical']+[{'stage':'v91_qwen_larger_model_comparison','manifest_sha256':sha(m),'redirects':{}}]
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
    pins={}
    for name in ['reports/protocol_v92.freeze.json','reports/protocol_v92b.freeze.json']:
        pins.update(read(ROOT/name)['sha256'])
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md',
        'reports/sensitivity_v92.md','reports/protocol_v92.freeze.json','reports/protocol_v92b.freeze.json',
        'scripts/seal_sensitivity_v92.py','scripts/replay_sensitivity_v92.py','scripts/package_sensitivity_v92.py',
        'artifacts/study_v91/evidence_manifest.json','output/sensitivity_v92_reproduction.zip']
    paths={ROOT/n for n in list(pins)+names}
    for d in [ART,ROOT/'results/v92_sensitivity',ROOT/'results/v92b_sensitivity',ROOT/'results/v92b_analysis']:
        paths.update(f for f in d.rglob('*') if f.is_file())
    paths={f for f in paths if f!=manifest and f.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in f.parts}
    manifest.write_text(json.dumps({'scope':'V92 Qwen3 development sensitivity diagnostic with preserved zero-generation preflight failure; no new objective outcomes; portable response replay','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(f.relative_to(ROOT)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
