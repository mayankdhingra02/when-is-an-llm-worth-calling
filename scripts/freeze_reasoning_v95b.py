from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
    out=ROOT/'reports/protocol_v95b.freeze.json';assert not out.exists()
    pins=read(ROOT/'reports/protocol_v95.freeze.json')['sha256']
    for n,h in pins.items():assert sha(ROOT/n)==h,n
    ledger=read(ROOT/'results/v95_reasoning/ledger.json')
    assert ledger['generation_requests']==0 and ledger['stage_seconds']<2
    names=['reports/protocol_v95b.md','reports/protocol_v95.freeze.json','configs/study_v95b.json',
           'scripts/reasoning_v95b_common.py','scripts/runtime_reasoning_v95b.py','scripts/collect_reasoning_v95b.py',
           'scripts/freeze_reasoning_v95b.py','tests/synthetic/test_reasoning_v95b.py','results/v95_reasoning/ledger.json',
           'results/v95_reasoning/runtime.json','artifacts/study_v95/model_execution.log']
    pins.update({n:sha(ROOT/n) for n in names})
    write(out,{'at':now(),'scope':'zero-generation adapter correction; original shared limits','sha256':pins})
    print('Frozen',len(pins),'original and amended inputs')
if __name__=='__main__':main()
