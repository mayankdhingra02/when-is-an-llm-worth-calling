from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v101.freeze.json'
    assert not out.exists() and not (ROOT/'results/v101_reasoning').exists()
    previous=read(ROOT/'reports/protocol_v100.freeze.json')
    for n,h in previous['sha256'].items():assert sha(ROOT/n)==h,n
    names=list(previous['sha256'])+['reports/protocol_v101.md','configs/study_v101.json','artifacts/study_v101/jobs.json','artifacts/study_v101/environment_before.json','artifacts/study_v100/evidence_manifest.json']
    for folder in ['scripts','tests/synthetic']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*v101.py')]
    assert read(ROOT/'artifacts/study_v101/jobs.json')==read(ROOT/'artifacts/study_v100/jobs.json')
    write(out,{'at':now(),'scope':'two-condition post-restart feasibility; zero new objective acquisitions','sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'files',sha(out))
if __name__=='__main__':main()
