"""V79 evidence sealing; preserve all earlier frozen outputs via exact snapshots."""
import argparse,json
from datetime import datetime,timezone
from seal_v78_execution import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v79'

def history():
    older=older_history();manifest=ROOT/'artifacts/study_v78_execution/evidence_manifest.json'
    assert sha(manifest)=='816fa1a3dc8301e9a344c072dde17109ece99dc1e72999174645c79ddc0225de'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for name,meta in files.items():
        path=ROOT/name
        if path.exists() and sha(path)==meta['sha256'] and path.stat().st_size==meta['bytes']:continue
        assert name in mapping,name
        path=ROOT/mapping[name]['snapshot_path'];assert sha(path)==meta['sha256'] and path.stat().st_size==meta['bytes'],name
        redirects[name]=str(path.relative_to(ROOT))
    return older+[{'stage':'v78_execution','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args()
    hist=history();freeze=ROOT/'reports/protocol_v79.freeze.json'
    assert sha(freeze)=='13bf1f34b1cca0cf77854b8bc9a71d22df336d15d757b26e359bb176ee920dfc'
    pins=read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    next_freeze=ROOT/'reports/protocol_v80.freeze.json'
    assert sha(next_freeze)=='9369379ed6b74d19b5eb031875314ee27303d57027f7783fe525437e688d6814'
    next_pins=read(next_freeze)['sha256']
    for n,d in next_pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'frozen_protocol_unchanged':True,'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+list(next_pins)+['reports/protocol_v80.freeze.json','STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','reports/kanzi_v79.md','reports/third_party_v79.md','reports/protocol_v79.freeze.json','scripts/fetch_silesia_v79.py','scripts/report_kanzi_v79.py','scripts/verify_kanzi_v79.py','scripts/seal_evidence_v79.py','artifacts/study_v78_execution/evidence_manifest.json']}
    for d in [ART,ROOT/'artifacts/study_v80',ROOT/'results/v79_kanzi_classical',ROOT/'results/v79_kanzi_analysis']:
        paths.update(p for p in d.rglob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope':'V79 real classical-only new-workload control; zero model requests','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n')
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
