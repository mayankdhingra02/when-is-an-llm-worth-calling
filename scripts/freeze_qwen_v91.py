"""Immutable protocol before any compatibility or scientific generation."""
from collect_smollm_v47 import ROOT,read,write,sha,now
from check_resources_v91 import validate

def main():
    out=ROOT/'reports/protocol_v91.freeze.json';assert not out.exists();cfg=read(ROOT/'configs/resource_proposal_v91.json');validate(cfg,read(ROOT/'artifacts/study_v91/approval.json'),sha(ROOT/'configs/resource_proposal_v91.json'))
    pins=read(ROOT/'reports/protocol_v47_smollm.freeze.json')['sha256']
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    names=['reports/protocol_v91.md','reports/protocol_v47_smollm.freeze.json','configs/resource_proposal_v91.json','artifacts/study_v91/approval.json','artifacts/study_v91/model_manifest.json','scripts/collect_qwen_v91.py','scripts/runtime_qwen_v91.py','scripts/analyze_qwen_v91.py','scripts/verify_qwen_v91.py','scripts/report_qwen_v91.py','scripts/freeze_qwen_v91.py','scripts/check_resources_v91.py','scripts/fetch_qwen_v91.py','scripts/run_planning_v55.py','src/escalation/receipts_v70.py','src/escalation/qwen_v91.py','tests/synthetic/test_qwen_v91.py','models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf']
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'results/v47_analysis/arms').glob('*.json')]
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'artifacts/sources/v91').glob('*') if p.is_file()]
    pins.update({n:sha(ROOT/n) for n in names});assert pins['models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf']==cfg['model_sha256']
    write(out,{'at':now(),'scope':'Approved exploratory larger-model comparison on unchanged exposed cases','sha256':pins});print('frozen',len(pins),'files')
if __name__=='__main__':main()
