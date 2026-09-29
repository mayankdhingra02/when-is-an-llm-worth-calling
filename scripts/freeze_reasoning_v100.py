"""Freeze local feasibility inputs before any new generation."""
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v100.freeze.json'
    assert not out.exists() and not (ROOT/'results/v100_reasoning').exists()
    previous=read(ROOT/'reports/protocol_v99.freeze.json')
    for n,h in previous['sha256'].items():assert sha(ROOT/n)==h,n
    names=list(previous['sha256'])+['reports/protocol_v100.md','configs/study_v100.json','artifacts/study_v100/jobs.json','artifacts/study_v99/runtime_help.txt','artifacts/study_v99/evidence_manifest.json']
    for folder in ['scripts','tests/synthetic']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*v100.py')]
    jobs=read(ROOT/'artifacts/study_v100/jobs.json')
    assert jobs==read(ROOT/'artifacts/study_v99/jobs.json')[:2]
    write(out,{'at':now(),'scope':'two-condition development feasibility; no objective acquisitions','sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'files',sha(out))
if __name__=='__main__':main()
