"""Seal real V80 execution and local portable replay, retaining exact history."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v79 import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v80_execution'

def history():
    previous=older_history();manifest=ROOT/'artifacts/study_v79/evidence_manifest.json'
    assert sha(manifest)=='23e4ef551c82bbb30dde36e8a4326623c99035d98288d973ee9151202881b998'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes']:continue
        assert name in mapping,name
        p=ROOT/mapping[name]['snapshot_path'];assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes'],name
        redirects[name]=str(p.relative_to(ROOT))
    return previous+[{'stage':'v79_and_v80_preparation','verified_files':len(files),'manifest_sha256':sha(manifest),'redirects':redirects}]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    historical=history();freeze=ROOT/'reports/protocol_v80.freeze.json'
    assert sha(freeze)=='9369379ed6b74d19b5eb031875314ee27303d57027f7783fe525437e688d6814'
    pins=read(freeze)['sha256']
    for name,digest in pins.items():assert sha(ROOT/name)==digest,name
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for name,m in data['files'].items():assert sha(ROOT/name)==m['sha256'] and (ROOT/name).stat().st_size==m['bytes'],name
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'original_frozen_protocol_unchanged':True,'historical':historical},indent=2));return
    assert not manifest.exists()
    names=['STATUS.md','README.md','reports/next_experiment.md','reports/kanzi_v80.md','reports/reproduction_v80.md','reports/protocol_v80.freeze.json','scripts/seal_v80_execution.py','scripts/verify_kanzi_v80_addendum.py','scripts/report_kanzi_v80.py','scripts/write_kanzi_v80_report.py','scripts/diagnose_kanzi_v80.py','scripts/replay_kanzi_v80_portable.py','scripts/bundle_kanzi_v80.py','scripts/check_portable_kanzi_v80.py','output/kanzi_v80_outcome_reconstruction.zip','artifacts/study_v79/evidence_manifest.json']
    paths={ROOT/name for name in list(pins)+names}
    for directory in [ART,ROOT/'results/v80_kanzi_paired',ROOT/'results/v80_kanzi_analysis',ROOT/'results/v80_proposal_diagnostic']:
        paths.update(p for p in directory.rglob('*') if p.is_file())
    # ZIP seals its included files; extracted and corrupted local fixtures are reproducible derivatives.
    paths.update(p for p in (ROOT/'artifacts/reproduction_v80').glob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope':'V80 genuine local-model/native paired execution, post-hoc diagnostics and isolated saved-outcome reconstruction; no held-out/router claim','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':historical,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n')
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
