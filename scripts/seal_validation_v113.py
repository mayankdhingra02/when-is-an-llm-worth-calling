"""Seal V106–V113 native engineering and confirmation while preserving history."""
import argparse,json
from datetime import datetime,timezone
from collect_smollm_v47 import ROOT,read,write,sha
ART=ROOT/'artifacts/study_v113'
def history():
    # Anchor the immutable prior audit, then recheck every byte with explicit
    # snapshot resolution. No old manifest/mapping is rewritten for new docs.
    m=ROOT/'artifacts/study_v105/evidence_manifest.json'
    assert sha(m)=='2bda57422f27ae174e3b86648b0cf7b7a7aa9286e39cec5ddb0e81bcbcbd7077'
    stages=read(m)['historical']+[{'stage':'v105_nginx_feasibility','manifest_sha256':sha(m),'redirects':{}}]
    manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')}
    mapping=read(ROOT/'artifacts/study_v106/previous_snapshot/mapping.json');verified=[];cache={}
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
    for stage in [106,107,108,109,110,111,113]:
        for n,h in read(ROOT/f'reports/protocol_v{stage}.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical_checkpoints':len(hist)}));return
    assert not manifest.exists()
    names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v105/evidence_manifest.json','.local-runtime/nginx-v105/nginx-1.28.3/objs/nginx']
    names += [f'.local-runtime/http-client-v{v}/client' for v in [106,107,110]]
    paths={ROOT/n for n in names}
    for v in range(106,114):
        for folder in ['scripts','reports','configs','tests/synthetic','native']:
            paths.update(p for p in (ROOT/folder).glob(f'*v{v}*') if p.is_file())
        for parent in ['artifacts','results']:
            for folder in (ROOT/parent).glob(f'*v{v}*'):
                if folder.is_dir():paths.update(p for p in folder.rglob('*') if p.is_file())
    paths.update(p for p in (ROOT/'output/v113_replication').rglob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    write(manifest,{'scope':'V106–V111 native NGINX engineering/retained failures; V112 synthetic-only adapter; V113 ninety real fixed-incumbent confirmations, independent certificate and timing-noise audit; no new model requests; private unexecuted independent-host packet','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
