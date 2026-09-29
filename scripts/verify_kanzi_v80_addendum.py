"""Read-only supplementary raw receipt audit; no frozen policy/code changes."""
import json
from analyze_kanzi_v80 import ROOT,read,analyze
from escalation.kanzi_receipt_audit_v78 import request_receipt,trial_limits,finite_nonnegative

def verify():
    data=analyze();out=ROOT/'results/v80_kanzi_paired';ledger=read(out/'ledger.json')
    workloads=read(ROOT/'artifacts/study_v79/workloads.json')['files'];cases=[];expected=[];usage=[];invalid=0;fallbacks=0
    for w in workloads:
        for seed in [11,23,37,53,71]:
            case=read(out/f"case_{w['name']}_{seed}.json");cases.append(case);failed=False;steps=[]
            for step in range(1,8):
                if not failed:
                    name=f"v80_{w['name']}_seed{seed}_step{step}";expected.append(name);p=out/name
                    request=read(p/'request.json');decision=read(p/'decision.json');assert request['request_id']==name
                    usage.append(request_receipt(request,read(p/'rendered.json'),read(p/'response.json'),decision,seed))
                    assert type(decision['valid']) is bool;failed=not decision['valid'];invalid+=failed
                if failed:steps.append(step)
            assert case['fallback_steps']==steps;fallbacks+=len(steps)
    starts=[json.loads(s) for s in (out/'request_starts.jsonl').read_text().splitlines()]
    assert [s['request_id'] for s in starts]==expected
    assert {p.name for p in out.glob('v80_*_seed*_step*') if (p/'request.json').exists()}==set(expected)
    assert ledger['generation_requests']==len(expected)<=105 and ledger['unattempted_generation_requests']==105-len(expected)
    assert ledger['fallback_search_evaluations']==fallbacks and ledger['retries']==0 and ledger['stop_reason'] is None
    assert finite_nonnegative(ledger['seconds'])<=1800 and finite_nonnegative(ledger['startup_seconds'])<=120
    assert ledger['external_spend_usd']==0 and ledger['server_exit_code']==0
    byname={w['name']:w for w in workloads};lock=read(ROOT/'configs/runtime_v76.lock.json')
    base=[str(ROOT/lock['java']),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(ROOT/lock['jar'])]
    for row in read(out/'acquisitions.json'):
        p=ROOT/row['path'];trial_limits(read(p/'result.json'),read(p/'supervision.json'))
        c=row['config'];source=ROOT/byname[row['workload']]['path']
        assert read(p/'commands.json')=={'compression':base+['-c','-i',str(source),'-o',str(p/'output.knz'),'-x','-t',c['transform'],'-e',c['entropy'],'-b',str(c['block_bytes']),'-j','1','-v','3'],
            'decompression':base+['-d','-i',str(p/'output.knz'),'-o',str(p/'decoded.bin'),'-j','1','-v','3']}
        assert read(p/'retention.json')['removed_after_validation']==['output.knz','decoded.bin']
        assert not (p/'output.knz').exists() and not (p/'decoded.bin').exists()
    totals={m:0.0 for m in ['rf_lcb','preset','llm']};seen=set()
    desired={(c['workload'],c['seed'],m,step):c['arms'][m][step+9]['config_id'] for c in cases for m in totals for step in range(1,8)}
    costs=[json.loads(s) for s in (out/'selection_costs.jsonl').read_text().splitlines()]
    for row in costs:
        key=(row['workload'],row['seed'],row['arm'],row['step']);assert key not in seen and row['config_id']==desired[key];seen.add(key)
        totals[row['arm']]+=finite_nonnegative(row['seconds'])
    assert set(desired)==seen and len(costs)==315
    return {'verified':True,'requests':len(expected),'invalid_responses':invalid,'fallback_search_slots':fallbacks,'selection_seconds':totals,'usage_unknown_requests':{k:sum(u[k] is None for u in usage) for k in ['tokens_predicted','tokens_evaluated']},'physical_trials':data['new_physical_trials'],'exact_commands_checked':900,'scope':'supplementary real receipt verification; no new measurements'}
if __name__=='__main__':
    result=verify();(ROOT/'artifacts/study_v80_execution/supplementary_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
