"""Seal bounded H2 classical evidence with exact historical snapshots."""
import argparse,json
from datetime import datetime,timezone
from seal_h2_v83 import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v84'
def history():
    hist=older_history();manifest=ROOT/'artifacts/study_v83/evidence_manifest.json';assert sha(manifest)=='5f6f007ed4b19140bcf4abd94d5757e1e0c2323a9857dbcc4923f29c54a99212'
    mapping=read(ART/'previous_snapshot/mapping.json');redirects={};files=read(manifest)['files']
    for n,m in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==m['sha256'] and p.stat().st_size==m['bytes']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],n
        redirects[n]=str(p.relative_to(ROOT))
    return hist+[{'stage':'v81_v83_h2_feasibility','verified_files':len(files),'manifest_sha256':sha(manifest),'redirects':redirects}]
def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');args=p.parse_args();hist=history();freeze=ROOT/'reports/protocol_v84.freeze.json';assert sha(freeze)=='f648dd7e4598f207dfc22e301b6fb408cc50f1ab43b5a71dcb0b8226b24ec51f'
    pins=read(freeze)['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    paths={ROOT/n for n in list(pins)+['STATUS.md','README.md','reports/next_experiment.md','reports/h2_v84.md','scripts/replay_h2_v84_portable.py','scripts/bundle_h2_v84.py','output/h2_v84_outcome_reconstruction.zip','artifacts/reproduction_v84/verification.json','reports/novelty_boundary_v84.md','reports/readiness_v84.md','scripts/write_h2_v84_report.py','scripts/seal_h2_v84.py','reports/protocol_v84.freeze.json','artifacts/study_v83/evidence_manifest.json']}
    for d in [ART,ROOT/'results/v84_h2_classical',ROOT/'results/v84_h2_analysis']:
        paths.update(p for p in d.rglob('*') if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope':'H2 classical paired continuations and standalone cheap prior; no LLM inference','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
