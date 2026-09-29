from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v103.freeze.json'
    assert not out.exists() and not (ROOT/'results/v103_reasoning').exists()
    assert read(ROOT/'artifacts/study_v102/feasibility.json')['feasibility_passed']
    previous=read(ROOT/'reports/protocol_v102.freeze.json')
    for n,h in previous['sha256'].items():assert sha(ROOT/n)==h,n
    names=list(previous['sha256'])+['reports/protocol_v103.md','configs/study_v103.json','artifacts/study_v103/jobs.json','artifacts/study_v102/evidence_manifest.json','artifacts/study_v102/feasibility.json']
    for folder in ['scripts','tests/synthetic']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*v103.py')]
    jobs=read(ROOT/'artifacts/study_v103/jobs.json');assert jobs==[j for j in read(ROOT/'artifacts/study_v99/jobs.json') if j['seed'] in [11,37]]
    write(out,{'at':now(),'scope':'24-condition exploratory development comparison; before fresh model calls/objective acquisitions','sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'files',sha(out))
if __name__=='__main__':main()
