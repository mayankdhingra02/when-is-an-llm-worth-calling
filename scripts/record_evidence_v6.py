"""Final local evidence inventory; no inference, acquisition or external writes."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,now
from escalation.data import sha
from escalation.study_v6 import verify_freeze

def main():
    path=Path('artifacts/study_v6/evidence_manifest.json')
    if path.exists():raise RuntimeError('refuse to overwrite evidence inventory')
    verify_freeze();v=read('artifacts/study_v6/verification.json');assert v['verified'] and v['verified_pairs']==30
    ledger=read('artifacts/resource_ledger_v2.json');assert ledger['active_since'] is None and ledger['requests']==98
    write('artifacts/study_v6/final_ledger_snapshot.json',ledger)
    files=[p for p in Path('results/v6').rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    files += [p for p in Path('artifacts/study_v6').glob('*') if p.is_file()]
    files += [Path(p) for p in ['STATUS.md','README.md','reports/pilot_report_v6.md','reports/admission_v6.md','reports/protocol_v6.md','reports/protocol_v6.freeze.json',
      'reports/next_experiment.md','scripts/verify_v6.py','scripts/report_v6.py','scripts/diagnose_v6.py','scripts/record_evidence_v6.py','data/manifest_v6.json']]
    write(path,{'at':now(),'scope':'actual v6 evidence plus explicitly labeled post-hoc diagnostics; no new inference','sha256':{str(p):sha(p) for p in sorted(set(files))}})
    print('Recorded',len(set(files)),'evidence files; all frozen sources intact; ledger inactive')
if __name__=='__main__':main()
