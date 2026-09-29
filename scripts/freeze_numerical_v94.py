"""Freeze V94 before objective acquisition or model generation."""
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v94.freeze.json';assert not out.exists()
    assert not (ROOT/'results/v94_native').exists() and not (ROOT/'results/v94_qwen').exists()
    cfg=read(ROOT/'configs/study_v94.json');assert cfg['max_native_acquisitions']==500
    total=sum(__import__('json').loads(s)['bytes'] for s in (ROOT/'artifacts/sources/v94/fetch.jsonl').read_text().splitlines())
    assert total<=cfg['download_stage_cap_bytes'] and total+cfg['prior_download_bytes']<=cfg['total_download_cap_bytes']
    names=['reports/protocol_v94.md','reports/source_audit_v94.md','configs/study_v94.json','configs/requirements_v94.txt',
           'requirements.lock.txt','scripts/runtime_qwen_v91.py','scripts/collect_smollm_v47.py','scripts/run_planning_v55.py',
           'src/escalation/qwen_v91.py','src/escalation/receipts_v70.py','src/escalation/finite_domain.py',
           'src/escalation/finite_v6.py','src/escalation/core.py','src/escalation/selection_v8.py','src/escalation/transfer_v41.py',
           'src/escalation/io.py','scripts/freeze_numerical_v94.py','scripts/worker_numerical_v94.py',
           'scripts/run_numerical_v94.py','scripts/collect_numerical_v94.py','src/escalation/numerical_v94.py',
           'tests/synthetic/test_numerical_v94.py','data/native_v94/orsreg_1.mtx',
           'artifacts/study_v91/model_manifest.json','.local-runtime/llama-b11146/llama-server',
           'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf']
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'artifacts/sources/v94').iterdir() if p.is_file()]
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'artifacts/study_v94').glob('*.json')]
    import scipy,highspy
    names += [str(p.relative_to(ROOT)) for root,pattern in [(Path(scipy.__file__).parent/'sparse/linalg/_dsolve','*_superlu*so'),(Path(highspy.__file__).parent,'*.so')] for p in root.glob(pattern)]
    names += [str(Path(scipy.__file__).parent.relative_to(ROOT)/'sparse/linalg/_dsolve/linsolve.py')]
    pins={n:sha(ROOT/n) for n in names}
    assert pins['models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf']=='d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785'
    write(out,{'at':now(),'scope':'fixed-policy fresh numerical families; before first native or model outcome','download_bytes':total,'sha256':pins})
    print('Frozen',len(pins),'files; downloaded',total,'bytes')
if __name__=='__main__':main()
