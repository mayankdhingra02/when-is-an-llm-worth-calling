"""Seal H2 source admission and all failed/correct feasibility attempts."""
import argparse,json
from datetime import datetime,timezone
from seal_v80_execution import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v83'
def history():
    prior=older_history();m=ROOT/'artifacts/study_v80_execution/evidence_manifest.json'
    assert sha(m)=='ee42d19c2d499430867c736d10cd6c19e4618ac17ed74ec61d46cd707a5e2ed9'
    mapping=read(ART/'previous_snapshot/mapping.json');redirect={};files=read(m)['files']
    for n,meta in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes'],n
        redirect[n]=str(p.relative_to(ROOT))
    return prior+[{'stage':'v80_execution','verified_files':len(files),'manifest_sha256':sha(m),'redirects':redirect}]
def main():
    a=argparse.ArgumentParser();a.add_argument('--verify-only',action='store_true');args=a.parse_args();hist=history();paths=set()
    freezes={81:'bf4914afaece3685d50cabf8e69a6d135fca2016ff7ad737ea818e4e4502173a',82:'b1dec9337bcfdbee1e3c49db8b3b240fbfbc952869aeddfe9332d445dffbf340',83:'509af0f3aec4e6872f73e3f6c27f1e937d4b99d02cfa58cffa5158691ede7552'}
    for v,d in freezes.items():
        p=ROOT/f'reports/protocol_v{v}.freeze.json';assert sha(p)==d;paths.add(p)
        for n,h in read(p)['sha256'].items():assert sha(ROOT/n)==h,n;paths.add(ROOT/n)
    manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not manifest.exists()
    for n in ['STATUS.md','README.md','reports/next_experiment.md','reports/h2_v83.md','reports/third_party_v81.md','scripts/seal_h2_v83.py','scripts/analyze_h2_v82.py','scripts/write_h2_v83_report.py','artifacts/study_v80_execution/evidence_manifest.json']:paths.add(ROOT/n)
    for v in [81,82,83]:
        for pat in [f'scripts/*h2_v{v}.py',f'reports/*v{v}*']:
            paths.update(p for p in ROOT.glob(pat) if p.is_file())
        for d in [f'artifacts/study_v{v}',f'results/v{v}_h2_feasibility',f'results/v{v}_h2_analysis']:
            paths.update(p for p in (ROOT/d).rglob('*') if p.is_file())
    paths.update(p for p in (ROOT/'artifacts/sources/v81').iterdir() if p.is_file())
    paths={p for p in paths if p!=manifest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope':'H2 development feasibility V81–V83, retaining one failed acquisition; no new LLM study','sealed_at':datetime.now(timezone.utc).isoformat(),'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n')
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
