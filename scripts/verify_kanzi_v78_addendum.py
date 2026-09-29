"""Supplementary pre-execution audit of all cost/failure/provenance counters.
Run AFTER a complete real batch. No model requests or synthetic result generation.
"""
import json
from analyze_kanzi_v78 import analyze,ROOT,read
from escalation.kanzi_receipt_audit_v78 import request_receipt,completed_accounting,trial_limits,selection_costs

def verify():
    base=analyze();out=ROOT/'results/v78_kanzi_paired';ledger=read(out/'ledger.json')
    cases=[read(out/f'case_{seed}.json') for seed in [11,23,37,53,71]]
    decisions={};usage=[]
    for p in sorted(out.glob('v78_seed*_step*')):
        if not (p/'request.json').exists():continue
        request=read(p/'request.json');decision=read(p/'decision.json');seed=int(p.name.split('_')[1][4:])
        usage.append(request_receipt(request,read(p/'rendered.json'),read(p/'response.json'),decision,seed));decisions[p.name]=decision
    starts=[json.loads(s) for s in (out/'request_starts.jsonl').read_text().splitlines()]
    counters=completed_accounting(cases,decisions,starts,ledger)
    for row in read(out/'acquisitions.json'):trial_limits(read(ROOT/row['path']/'result.json'),read(ROOT/row['path']/'supervision.json'))
    costs=selection_costs(cases,[json.loads(s) for s in (out/'selection_costs.jsonl').read_text().splitlines()])
    return {'verified':True,'counters':counters,'selection_seconds':costs,'usage_unknown_requests':{key:sum(u[key] is None for u in usage) for key in ['tokens_predicted','tokens_evaluated']},'collection_ledger_seconds':ledger['seconds'],'physical_trials':base['new_physical_trials'],'scope':'supplementary accounting replay, no new outcomes or inference'}
if __name__=='__main__':
    result=verify();p=ROOT/'artifacts/study_v78_execution';p.mkdir(exist_ok=True);(p/'supplementary_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
