"""Seal corrected feasibility/classical evidence with V69 historical redirects."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v69 import history as previous_history
from seal_evidence_v67 import sha,read,ROOT
ART=ROOT/'artifacts/study_v71'

def history():
    previous=previous_history();seal=ROOT/'artifacts/study_v69/evidence_manifest.json'
    assert sha(seal)=='5daedbc21c1d3a918d078d332b77a73d9e754bdf33c6cf70deda094f5c6c04f5'
    files=read(seal)['files'];mapping=read(ROOT/'artifacts/study_v70/previous_snapshot/mapping.json');redirects={}
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256']:continue
        assert name in mapping,name
        old=ROOT/mapping[name]['snapshot_path'];assert sha(old)==meta['sha256'],name
        redirects[name]=str(old.relative_to(ROOT))
    return previous+[{'stage':69,'manifest_sha256':sha(seal),'verified_files':len(files),'snapshot_redirects':redirects}]

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args();hist=history();manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,meta in data['files'].items():
            p=ROOT/name;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','requirements.lock.txt','artifacts/study_v69/evidence_manifest.json']}
        for pattern in ['artifacts/study_v7[01]/**/*','results/v7[01]*/**/*','scripts/*v7[01].py','src/escalation/*v7[01].py','tests/**/*v7[01].py','reports/*v7[01]*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        for freeze in ROOT.glob('reports/protocol_v7[01].freeze.json'):
            paths.update(ROOT/n for n in read(freeze)['sha256'])
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'study':'v70_v71_corrected_feasibility_and_classical','sealed_at_utc':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
