"""Read-only verification of checkpoint and unchanged prepared experiment."""
import json
from seal_v78_failure_checks import ROOT,sha,read,history
ART=ROOT/'artifacts/study_v78_blocked'
if __name__=='__main__':
    prior=history();manifest=ROOT/'artifacts/study_v78_failure_checks/evidence_manifest.json'
    assert sha(manifest)=='0254302037b3d8ac548bbea8f5ac8e44ed119c850594b751da4d916015675999'
    files=read(manifest)['files'];redirects={}
    for n,m in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==m['sha256']:continue
        assert n=='STATUS.md',n
        p=ART/'previous_snapshot/STATUS.md';assert sha(p)==m['sha256'],n
        redirects[n]=str(p.relative_to(ROOT))
    audit=read(ART/'audit.json');assert sha(ROOT/'STATUS.md')==audit['status_sha256']
    assert sha(ART/'previous_snapshot/STATUS.md')==audit['previous_status_sha256']
    freeze=ROOT/'reports/protocol_v78.freeze.json';assert sha(freeze)==audit['frozen_scope_sha256']
    for n,d in read(freeze)['sha256'].items():assert sha(ROOT/n)==d,n
    print(json.dumps({'verified':True,'checkpoint':'v78_pending_allowance','frozen_scope_unchanged':True,'latest_prior_files':len(files),'redirects':redirects,'older_manifests_verified':len(prior)}))
