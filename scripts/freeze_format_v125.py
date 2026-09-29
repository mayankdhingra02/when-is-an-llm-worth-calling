"""Freeze real V124 comparator receipts after their completed verification."""
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
 p=ROOT/'reports/protocol_v125.freeze.json';assert not p.exists();ledger=read(ROOT/'results/v124_surrogate/ledger.json');assert ledger['server_exit_code']==0;assert read(ROOT/'artifacts/study_v124/verification.json')['verified']
 paths={ROOT/n for n in read(ROOT/'reports/protocol_v124.freeze.json')['sha256']};paths.add(ROOT/'reports/protocol_v124.freeze.json')
 paths.update(ROOT/n for n in ['reports/protocol_v125.md','configs/study_v125.json','artifacts/study_v125/inputs.freeze.json','artifacts/study_v125/tests_precollection.log','artifacts/study_v125/tests_full_precollection.log','artifacts/study_v124/verification.json','results/v124_surrogate/generation_starts.jsonl','results/v124_surrogate/responses.jsonl','results/v124_surrogate/ledger.json'])
 paths.update(ROOT/n for n in read(ROOT/'artifacts/study_v125/inputs.freeze.json')['sha256'])
 for folder in ['scripts','tests/synthetic']:paths.update((ROOT/folder).glob('*v125.py'))
 # The final evidence sealer is mutable checkpoint plumbing, not experiment code.
 paths.discard(ROOT/'scripts/seal_surrogate_v125.py')
 for j in read(ROOT/'artifacts/study_v125/jobs.json'):paths.add(ROOT/f"results/v124_surrogate/preflight/{j['original_request_key']}.json")
 write(p,{'at':now(),'scope':'V125 HIPAcc format-only probe;18requests,zero new objective acquisitions;V124unchanged','sha256':{str(f.relative_to(ROOT)):sha(f) for f in sorted(paths)}});print('Frozen',len(paths),'inputs',sha(p))
if __name__=='__main__':main()
