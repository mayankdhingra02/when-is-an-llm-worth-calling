"""Freeze all V97 acquisition, inference and primary analysis before execution."""
from pathlib import Path
from collect_smollm_v47 import ROOT, read, write, sha, now
import scipy

def main():
    out = ROOT / 'reports/protocol_v97.freeze.json'
    assert not out.exists()
    assert not (ROOT/'results/v97_native').exists() and not (ROOT/'results/v97_qwen').exists()
    cfg = read(ROOT/'configs/study_v97.json')
    assert cfg['families']==['superlu'] and cfg['max_native_acquisitions']==250
    assert cfg['new_generation_request_cap']==50 and cfg['allow_paid_api'] is False
    names = [n for n in read(ROOT/'reports/protocol_v94.freeze.json')['sha256']
        if n.startswith(('src/', 'requirements.', 'scripts/runtime_', 'scripts/collect_smollm',
                         'scripts/run_planning', 'models/', '.local-runtime/', '.venv/',
                         'artifacts/study_v91/', 'data/native_v94/'))]
    names += ['artifacts/study_v94/router_precommit.json','reports/source_audit_v96.md',
        'reports/protocol_v97.md','configs/study_v97.json','configs/requirements_v94.txt']
    names += [str(p.relative_to(ROOT)) for folder in ['scripts','src/escalation','tests/synthetic']
              for p in (ROOT/folder).glob('*v97.py')]
    manifest = dict(group='superlu', status='previously_exposed_development',
        source_manifest='artifacts/study_v94/dataset_manifest.json',
        source_manifest_sha256=sha(ROOT/'artifacts/study_v94/dataset_manifest.json'),
        data_path='data/native_v94/orsreg_1.mtx',
        data_sha256=sha(ROOT/'data/native_v94/orsreg_1.mtx'), scipy_version=scipy.__version__,
        configurations=240, domain_change='relax1,2,4,8; panel4,8,16; no prior outcomes reused',
        new_download_bytes=0)
    write(ROOT/'artifacts/study_v97/dataset_manifest.json',manifest)
    names += ['artifacts/study_v97/dataset_manifest.json']
    pins = {n:sha(ROOT/n) for n in sorted(set(names))}
    assert pins['models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf']=='d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785'
    write(out, dict(at=now(),scope='exploratory restricted-domain study; before first new outcome',
        download_bytes=0,sha256=pins))
    print('Frozen',len(pins),'files',sha(out))

if __name__=='__main__':
    main()
