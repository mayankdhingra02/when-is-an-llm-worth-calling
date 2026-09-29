"""Regenerate descriptive artifacts and verify byte identity, no new data collection."""
import subprocess,sys
from collect_smollm_v47 import ROOT,write,sha
def main():
    names=['reports/proposals_v128.md','reports/proposals_v129.md','reports/policy_envelope_v129.md',
      'results/v128_analysis/comparison.json','results/v128_analysis/proposals.png',
      'results/v129_analysis/comparison.json','results/v129_analysis/proposals.png',
      'results/v129_analysis/policy_envelope.json','results/v129_analysis/policy_envelope.png']
    before={n:sha(ROOT/n) for n in names}
    for script in ['report_original_v129.py','report_proposal_v129.py','policy_envelope_v129.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=60)
    after={n:sha(ROOT/n) for n in names};assert before==after
    receipt={'verified':True,'byte_identical':after,'new_model_calls':0,'new_objective_acquisitions':0}
    write(ROOT/'artifacts/study_v129/reproduction.json',receipt);print('Nine reports/data/figures reproduce byte-identically')
if __name__=='__main__':main()
