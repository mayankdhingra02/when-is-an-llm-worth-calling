"""Retain observable progress for the interrupted request without inventing totals."""
import re,json
from collect_smollm_v47 import ROOT,read,write,sha
def main():
    p=ROOT/'results/v128_proposals/server.log';s=p.read_text();chunks=s.split('processing task,')
    assert len(chunks)==3
    tail=chunks[-1];progress=[int(x) for x in re.findall(r'prompt processing, n_tokens =\s*(\d+)',tail)]
    generated=[int(x) for x in re.findall(r'n_gen =\s*(\d+)',tail)]
    assert progress and 'total time =' not in tail
    usage=read(ROOT/'results/v129_analysis/comparison.json')['actual_cost']['usage']
    result={'scope':'Returned complete receipts plus interrupted-request server progress; lower bounds are not total usage',
      'server_log':str(p.relative_to(ROOT)),'server_log_sha256':sha(p),
      'interrupted_request':'mongodb_twins_23_normal','interrupted_prompt_progress_lower_bound':max(progress),
      'interrupted_generated_progress_lower_bound':max(generated) if generated else None,
      'returned_generated_tokens':usage['tokens_predicted']['observed_sum'],
      'returned_prefill_tokens':usage['tokens_evaluated']['observed_sum'],
      'combined_observed_prefill_lower_bound':usage['tokens_evaluated']['observed_sum']+max(progress),
      'requests_with_unknown_total_usage':1,'new_requests':0,'new_objective_accesses':0}
    write(ROOT/'artifacts/study_v129/cost_detail.json',result);print(result)
if __name__=='__main__':main()
