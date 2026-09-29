from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
    out=ROOT/'reports/protocol_v95.freeze.json';assert not out.exists()
    assert not (ROOT/'results/v95_reasoning').exists()
    names=['reports/protocol_v95.md','configs/study_v95.json','artifacts/study_v95/jobs.json',
        'scripts/runtime_reasoning_v95.py','scripts/collect_reasoning_v95.py','scripts/reasoning_v95_common.py',
        'scripts/decoder_v49_common.py','scripts/freeze_reasoning_v95.py','tests/synthetic/test_reasoning_v95.py',
        'artifacts/sources/v91/README.md','artifacts/study_v91/model_manifest.json',
        'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf','.local-runtime/llama-b11146/llama-server',
        'scripts/collect_smollm_v47.py','scripts/run_planning_v55.py','src/escalation/receipts_v70.py']
    jobs=read(ROOT/'artifacts/study_v95/jobs.json');assert len(jobs)==36
    names += [j['prefix'] for j in jobs]
    assert {j['system_group'] for j in jobs}=={'berkeleydb','dune_hsmgp','hipacc','llvm','openvpn','sac'}
    write(out,{'at':now(),'scope':'development-only owner-informed sampling, bounded thinking; no fresh-family inference','sha256':{n:sha(ROOT/n) for n in sorted(set(names))}})
    print('Frozen',len(set(names)),'inputs')
if __name__=='__main__':main()
