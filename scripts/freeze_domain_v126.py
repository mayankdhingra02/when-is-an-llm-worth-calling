"""Create-once pre-acquisition freeze for the development feasibility audit."""
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    dest=ROOT/'reports/protocol_v126.freeze.json';assert not dest.exists();assert not (ROOT/'results/v126_domain_audit').exists()
    paths={ROOT/n for n in read(ROOT/'reports/protocol_v123.freeze.json')['sha256']}
    paths.update(ROOT/n for n in ['reports/protocol_v126.md','configs/study_v126.json','data/manifest_v41.json','results/v42_selection_reference/summary.json','artifacts/study_v126/tests_precollection.log'])
    paths.update(p for p in (ROOT/'artifacts/study_v126').glob('*.json'))
    for folder in ['scripts','tests/synthetic']:paths.update((ROOT/folder).glob('*v126.py'))
    for s in read(ROOT/'data/manifest_v41.json')['datasets']:paths.add(ROOT/s['path'])
    for j in read(ROOT/'artifacts/study_v126/cases.json'):
        paths.add(ROOT/j['prefix'])
        paths.update(ROOT/f"results/v41_transfer/arms/{j['key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full'])
        p=ROOT/f"results/v115_portfolio/arms/{j['key']}.json"
        if p.exists():paths.add(p)
    write(dest,{'at':now(),'scope':'V126 development coverage audit,4932charged labels,497bounded branches,zero inference','sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}})
    print('Frozen',len(paths),'inputs',sha(dest))
if __name__=='__main__':main()
