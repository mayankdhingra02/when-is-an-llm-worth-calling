"""Seal V69 receipts and validity correction while preserving V68 history."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v68 import history as previous_history
from seal_evidence_v67 import sha,read,ROOT
ART=ROOT/'artifacts/study_v69'

def history():
    prior=previous_history();seal=ROOT/'artifacts/study_v68/evidence_manifest.json'
    assert sha(seal)=='8bf33a61e9164379bd07bf710b8a9f30d0ec704fa5292d634cd9db5804aab8ad'
    files=read(seal)['files'];mapping=read(ART/'previous_snapshot/mapping.json');redirects={}
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256']:continue
        assert name in mapping,name
        old=ROOT/mapping[name]['snapshot_path'];assert sha(old)==meta['sha256'],name
        redirects[name]=str(old.relative_to(ROOT))
    return prior+[{'stage':68,'manifest_sha256':sha(seal),'verified_files':len(files),'snapshot_redirects':redirects}]

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args();hist=history();manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,meta in data['files'].items():
            p=ROOT/name;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','requirements.lock.txt','configs/runtime_v69.lock.json','artifacts/study_v68/evidence_manifest.json']}
        for pattern in ['artifacts/study_v69/**/*','artifacts/sources/v69*/**/*','results/v69*/**/*','data/generated_v69/**/*','scripts/*v69*.py','src/escalation/*v69*.py','tests/**/*v69*.py','reports/*v69*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        for freeze in ROOT.glob('reports/protocol_v69*.freeze.json'):
            paths.update(ROOT/n for n in read(freeze)['sha256'])
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'study':'v69_physical_feasibility_with_validity_correction','sealed_at_utc':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
