"""Pin inference and charged analysis together before V99 begins."""
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
    out=ROOT/'reports/protocol_v99.freeze.json'
    assert not out.exists() and not (ROOT/'results/v99_reasoning').exists()
    names=['reports/protocol_v99.md','reports/source_audit_v98.md','reports/protocol_v98.md','scripts/reasoning_v98_common.py','configs/study_v99.json',
        'artifacts/study_v99/jobs.json','scripts/decoder_v49_common.py','scripts/reasoning_v95b_common.py',
        'artifacts/sources/v91/README.md','artifacts/study_v91/model_manifest.json',
        'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf','.local-runtime/llama-b11146/llama-server',
        'scripts/collect_smollm_v47.py','scripts/run_planning_v55.py','src/escalation/receipts_v70.py',
        'src/escalation/core.py','src/escalation/finite_v6.py','src/escalation/transfer_v41.py',
        'src/escalation/io.py','data/manifest_v41.json','results/v91_analysis/cases.json',
        'requirements.lock.txt']
    for folder in ['scripts','tests/synthetic']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*v99.py')]
    jobs=read(ROOT/'artifacts/study_v99/jobs.json');assert len(jobs)==36
    assert len({j['base_key'] for j in jobs})==18
    assert {j['system_group'] for j in jobs}=={'berkeleydb','dune_hsmgp','hipacc','llvm','openvpn','sac'}
    names += [j['prefix'] for j in jobs]
    # Exact public table files are already pinned in each source spec.
    for d in read(ROOT/'data/manifest_v41.json')['datasets']:
        if 'path' in d:names.append(d['path'])
    write(out,{'at':now(),'scope':'development-only final-answer reserve; before model calls/new labels',
        'sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'files',sha(out))

if __name__=='__main__':main()
