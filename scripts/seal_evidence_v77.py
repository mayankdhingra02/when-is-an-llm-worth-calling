"""Seal V76 diagnosis, V77 results and unexecuted V78 preparation; history retained."""
import argparse,json
from datetime import datetime,timezone
from seal_evidence_v75 import ROOT,sha,read,history as older_history
from verify_kanzi_v76 import verify as diagnosis
from analyze_kanzi_v77 import verify as classical
ART=ROOT/'artifacts/study_v77'
def history():
    prior=older_history();manifest=ROOT/'artifacts/study_v75/evidence_manifest.json'
    assert sha(manifest)=='6250d14236778d112186f34939cd9af11d2e79ad223a6fd07774453b8cc2d645'
    mapping=read(ART/'previous_snapshot/mapping.json');files=read(manifest)['files'];redirects={}
    for name,meta in files.items():
        p=ROOT/name
        if p.exists() and sha(p)==meta['sha256']:continue
        assert name in mapping,name
        p=ROOT/mapping[name]['snapshot_path'];assert sha(p)==meta['sha256'],name
        redirects[name]=str(p.relative_to(ROOT))
    return prior+[{'stage':'v75','manifest_sha256':sha(manifest),'verified_files':len(files),'redirects':redirects}]
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    hist=history();assert diagnosis()==read(ROOT/'artifacts/study_v76/verification.json')
    assert classical()==read(ROOT/'results/v77_kanzi_analysis/summary.json')
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'diagnosis_replayed':True,'physical_trials_replayed':200,'historical':hist},indent=2))
    else:
        assert not manifest.exists()
        paths={ROOT/n for n in ['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v75/evidence_manifest.json']}
        for stage in [76,77,78]:
            for pattern in [f'artifacts/study_v{stage}/**/*',f'results/v{stage}*/**/*',f'scripts/*v{stage}*.py',f'src/escalation/*v{stage}.py',f'tests/**/*v{stage}.py',f'reports/*v{stage}*',f'configs/*v{stage}*']:
                paths.update(p for p in ROOT.glob(pattern) if p.is_file())
            paths.update(ROOT/n for n in read(ROOT/f'reports/protocol_v{stage}.freeze.json')['sha256'])
        paths={p for p in paths if '__pycache__' not in p.parts and p!=manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        data={'scope':'v76_controlled_diagnosis_v77_classical_results_v78_unexecuted_preparation','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,
              'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)},indent=2))
