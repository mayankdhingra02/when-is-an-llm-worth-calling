"""Seal V66/V67 and verify historical V65 through preserved mutable snapshots."""
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from seal_evidence_v65 import history
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'artifacts/study_v67'
def read(p):return json.loads(p.read_text())
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def old_history():
    older=history();seal=ROOT/'artifacts/study_v65/evidence_manifest.json'
    assert sha(seal)=='d93e0f5ecf6d35c5a471ddafb9b45f82e70111772d975a089a499e3e42f227f3'
    mapping=read(ROOT/'artifacts/study_v66/previous_snapshot/mapping.json');redirects={};files=read(seal)['files']
    for name,meta in files.items():
        path=ROOT/name
        if sha(path)==meta['sha256']:continue
        assert name in mapping,name
        p=ROOT/mapping[name]['snapshot_path'];assert sha(p)==meta['sha256'],name
        redirects[name]=str(p.relative_to(ROOT))
    return older+[{'stage':65,'manifest_sha256':sha(seal),'verified_files':len(files),'snapshot_redirects':redirects}]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args();hist=old_history()
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,meta in data['files'].items():
            p=ROOT/name;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/name for name in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','requirements.lock.txt','configs/runtime_v66.lock.json','data/live_manifest_v67.json','artifacts/study_v65/evidence_manifest.json']}
    for pattern in ['artifacts/study_v6[67]/**/*','artifacts/sources/v66/**/*','data/generated_v66/**/*','results/v6[67]*/**/*','reports/*v6[67]*','scripts/*v6[67].py','src/escalation/*v6[67].py','tests/synthetic/*v6[67].py']:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    for freeze in ROOT.glob('reports/protocol_v6[67]*.freeze.json'):paths.update(ROOT/name for name in read(freeze)['sha256'])
    paths={p for p in paths if p!=manifest and '__pycache__' not in p.parts and p.name not in ['seal_creation.log','seal_verification.json']}
    data={'studies':'v66_v67_complete','sealed_at_utc':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
    manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
if __name__=='__main__':main()
