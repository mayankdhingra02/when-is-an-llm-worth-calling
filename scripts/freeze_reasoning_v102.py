from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v102.freeze.json'
    assert not out.exists() and not (ROOT/'results/v102_reasoning').exists()
    previous=read(ROOT/'reports/protocol_v101.freeze.json')
    for n,h in previous['sha256'].items():assert sha(ROOT/n)==h,n
    names=list(previous['sha256'])+['reports/protocol_v102.md','configs/study_v102.json','artifacts/study_v102/jobs.json','artifacts/study_v101/evidence_manifest.json']
    for folder in ['scripts','tests/synthetic']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*v102.py')]
    assert read(ROOT/'artifacts/study_v102/jobs.json')==read(ROOT/'artifacts/study_v101/jobs.json')
    write(out,{'at':now(),'scope':'two-condition shorter-thought feasibility; zero new objective acquisitions','sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'files',sha(out))
if __name__=='__main__':main()
