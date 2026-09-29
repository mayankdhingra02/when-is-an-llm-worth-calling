"""Freeze the next decoder diagnostic before its first generation."""
from collect_smollm_v47 import ROOT, read, write, sha, now
from decoder_v93_common import validate

def main():
    out=ROOT/'reports/protocol_v93_decoder.freeze.json';assert not out.exists()
    validate(read(ROOT/'configs/study_v93.json'))
    pins=read(ROOT/'reports/protocol_v92b.freeze.json')['sha256']
    for n,h in pins.items():assert sha(ROOT/n)==h,n
    names=['reports/protocol_v93_decoder.md','configs/study_v93.json','artifacts/study_v93/jobs.json',
        'reports/protocol_v92b.freeze.json','artifacts/study_v92/evidence_manifest.json',
        'scripts/decoder_v49_common.py','scripts/decoder_v93_common.py','scripts/runtime_decoder_v93.py',
        'tests/synthetic/test_decoder_v93.py','results/v92b_sensitivity/ledger.json']
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'scripts').glob('*decoder_v93.py')]
    for sub in ['preflight','choices']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/'results/v92b_sensitivity'/sub).glob('*.json')]
    pins.update({n:sha(ROOT/n) for n in names})
    write(out,{'at':now(),'scope':'Fixed development decoder diagnostic; no new objective labels','sha256':pins})
    print('Frozen',len(pins),'files')
if __name__=='__main__':main()
