from collect_smollm_v47 import ROOT, read, write, sha, now
from decoder_v93b_common import validate

def main():
    out=ROOT/'reports/protocol_v93b_decoder.freeze.json';assert not out.exists()
    validate(read(ROOT/'configs/study_v93b.json'))
    pins=read(ROOT/'reports/protocol_v93_decoder.freeze.json')['sha256']
    for n,h in pins.items():assert sha(ROOT/n)==h,n
    names=['configs/study_v93b.json','reports/protocol_v93b_decoder.md','reports/protocol_v93_decoder.freeze.json',
        'artifacts/study_v93/remaining_jobs.json','scripts/decoder_v93b_common.py','tests/synthetic/test_decoder_v93b.py']
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'scripts').glob('*decoder_v93b.py')]
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'results/v93_decoder').rglob('*') if p.is_file()]
    pins.update({n:sha(ROOT/n) for n in names});write(out,{'at':now(),'scope':'Resource-only amendment, unattempted cases only; shared original caps unchanged','sha256':pins});print('Frozen',len(pins),'files')
if __name__=='__main__':main()
