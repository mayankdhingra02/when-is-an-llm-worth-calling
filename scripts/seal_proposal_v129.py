"""Seal combined V128 interruption/V129 recovery while retaining all history."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
from seal_proposal_v128 import history
ART=ROOT/'artifacts/study_v129'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    hist=history();dest=ART/'evidence_manifest.json'
    for v in [128,129]:
        for n,h in read(ROOT/f'reports/protocol_v{v}.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    if args.verify_only:
        d=read(dest)
        for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
    assert not dest.exists()
    names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v127/evidence_manifest.json','output/v128_replay.zip','output/v129_replay.zip']
    paths={ROOT/n for n in names}
    for folder in ['scripts','reports','configs','tests/synthetic']:
        for v in [128,129]:paths.update(p for p in (ROOT/folder).glob(f'*v{v}*') if p.is_file())
    for folder in ['artifacts/study_v128','artifacts/study_v129','results/v128_proposals','results/v128_analysis','results/v129_proposals','results/v129_merged','results/v129_analysis','output/v128_replay','output/v129_replay']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
    write(dest,{'at':now(),'scope':'V128partial collection and explicit V129recovery;two exposed application families;13actualrequests/390experimentalaccesses+2incidental;posthocfinitepolicyceiling;no new heldout/Q2claim',
        'historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
    print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
