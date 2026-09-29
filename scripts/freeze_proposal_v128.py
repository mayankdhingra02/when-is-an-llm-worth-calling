"""Freeze complete local dependency closure before any V128 generation."""
from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
    dest=ROOT/'reports/protocol_v128.freeze.json';assert not dest.exists();assert not (ROOT/'results/v128_proposals').exists()
    paths=set()
    for v in [119,121,127]:
        f=ROOT/f'reports/protocol_v{v}.freeze.json';paths.add(f);paths.update(ROOT/n for n in read(f)['sha256'])
    for folder in ['scripts','src/escalation']:
        paths.update((ROOT/folder).glob('*.py'))
    paths.update((ROOT/'tests/synthetic').glob('*v128.py'))
    paths.update(ROOT/n for n in ['reports/protocol_v128.md','configs/study_v128.json','artifacts/study_v128/inputs.freeze.json','artifacts/study_v128/tests_precollection.log','artifacts/study_v128/tests_full_precollection.log'])
    paths.update(ROOT/n for n in ['artifacts/study_v128/structural_preflight.json','artifacts/study_v128/synthetic_offline_tokenizer.json','artifacts/study_v128/tests_full_precollection_failed.log','artifacts/study_v128/native_parser_recheck.log'])
    paths.update(ROOT/n for n in read(ROOT/'artifacts/study_v128/inputs.freeze.json')['sha256'])
    for j in read(ROOT/'artifacts/study_v128/cases.json'):
        paths.add(ROOT/j['prefix'])
        paths.update((ROOT/f"results/v{j['classical_version']}_classical/arms").glob(j['key']+'_*.json'))
        if j['classical_version']==119:paths.add(ROOT/f"results/v120_analysis/arms/{j['key']}.json")
    write(dest,{'at':now(),'scope':'V128 exposed two-family extension;12calls/300acquisitions;no new holdout','sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}})
    print('Frozen',len(paths),'inputs',sha(dest))
if __name__=='__main__':main()
