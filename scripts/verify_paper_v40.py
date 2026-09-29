"""Audit central manuscript numbers against saved measured and derived records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def main():
    v38=read('results/v38_size_prompt/summary.json');v40=read('results/v40_frontier/summary.json');text=(ROOT/'paper/manuscript.md').read_text()
    claims=[]
    def check(label,ok,display):
        if not ok or display not in text:raise ValueError('Unsupported/missing manuscript claim: '+label)
        claims.append({'claim':label,'display':display,'checked':True})
    primary=next(s for s in v38['summaries'] if (s['condition'],s['baseline'])==('assigned_ids','exact_joint_shortlist'))
    check('primary gain',f"{100*primary['equal_family_mean_gain']:.4f}"=='1.7534','1.7534%')
    rr=[r for r in v38['comparisons'] if r['baseline']=='runtime_3nn']
    check('runtime3NNdominance',(sum(r['relative_gain']>0 for r in rr),sum(r['relative_gain']==0 for r in rr),sum(r['relative_gain']<0 for r in rr))==(0,24,6),'0 LLM wins,24 ties and 6 harms')
    for base,expected in [('exact_joint_shortlist','1.9745'),('exact_joint_full','1.6507'),('runtime_3nn','0.0000'),('static_rank','3.6254')]:
        r=next(s for s in v40['scenarios'] if (s['scenario'],s['baseline'])==('assigned_ids',base))
        check(base+' maximum',f"{r['maximum_gain']*100:.4f}"==expected,expected)
    r=next(s for s in v40['scenarios'] if (s['scenario'],s['baseline'])==('worst_tested_presentation','exact_joint_shortlist'))
    check('worstpresentationmaximum',f"{r['maximum_gain']*100:.4f}"=='0.3238','0.3238%')
    r=next(s for s in v40['primary_leave_one_case_out'] if (s['excluded_dataset'],s['excluded_seed'])==('brotli',23))
    check('caseinfluence',f"{r['equal_family_mean_gain']*100:.4f}"=='0.0475','0.0475%')
    check('allocationcount',v40['enumerated_allocations']==30720,'30,720')
    check('tokens',v38['input_tokens']==55302 and v38['output_tokens']==600,'55,302 input and 600 output tokens')
    check('requests',v38['actual_new_requests']==30 and v38['actual_new_joint_vectors']==300,'30 real calls and 300 recorded-vector accesses')
    check('infeasiblevectors',sum(r['infeasible_continuation_vectors'] for r in v38['records'])==84,'84/300')
    print(json.dumps({'central_claims_checked':len(claims),'claims':claims,'scope':'Central numerical claims only; not novelty, complete prose accuracy or publication certification'},indent=2))
if __name__=='__main__':main()
