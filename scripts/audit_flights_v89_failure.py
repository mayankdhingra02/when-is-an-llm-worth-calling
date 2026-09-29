"""Post-failure integrity audit; cannot emit a grid-comparison claim."""
from analyze_flights_v89 import ROOT,RAW,read,sha,QUERIES,validate_answer,CONFIGS,schedule,CHECKED
import json,math

def main():
    f=read(ROOT/'reports/protocol_v89.freeze.json')
    for n,d in f['sha256'].items():assert sha(ROOT/n)==d,n
    s=read(RAW/'summary.json');rows=read(RAW/'acquisitions.json');assert not s['complete'] and s['charged_trials']==9 and s['valid_trials']==8 and s['failed_trials']==1 and s['unattempted_trials']==71
    contract=read(ROOT/'data/flights_v88/query_contract.json');interference=read(ROOT/'artifacts/study_v89/collection_interference.json');overlap=[];checked=0
    for idx,row in enumerate(rows):
        folder=RAW/f'trial_{idx:02d}';item=schedule()[idx];assert row['configuration']==CONFIGS[item['configuration_index']] and all(row[k]==v for k,v in item.items())
        charge=read(folder/'charge.json');assert charge['status']=='charged' and all(row[k]==v for k,v in charge.items() if k!='status')
        process=read(folder/'process_receipt.json');assert process==row['process']
        if row['at_unix']<=interference['test_log_last_write_unix'] and row['at_unix']+process['wall_seconds']>=interference['test_log_creation_unix']:overlap.append(idx)
        if row['status']=='failed':assert idx==8 and process['termination_reason']=='wall_timeout' and process['exit_code']==-9;continue
        assert process['exit_code']==0 and process['termination_reason'] is None
        result=read(folder/'result.json');answers=read(folder/'answers.json');assert result==row['result'] and sha(folder/'answers.json')==result['answers_sha256'] and len(answers)==CHECKED
        for j,a in enumerate(answers):
            assert a['repetition']==j//3 and a['query']==list(QUERIES)[j%3] and a['scored']==(j//3>=3) and math.isfinite(a['seconds']) and a['seconds']>0
            validate_answer(a['query'],a['columns'],a['rows'],contract['expected']['answers'][a['query']]);checked+=1
        assert sum(a['seconds'] for a in answers if a['scored'])==result['query_seconds']
    plans=read(RAW/'trial_08/plans.json');cross={q:'CROSS_PRODUCT' in json.dumps(p) for q,p in plans.items()}
    out=ROOT/'results/v89_flights_failure_audit';out.mkdir(exist_ok=False);(out/'summary.json').write_text(json.dumps({'collection':s,'verified_completed_answers':checked,'failed_trial_completed_answers':'unknown: worker buffered answers until successful finish','possible_test_overlap_trial_indices':overlap,'failed_plan_contains_cross_product':cross,'comparison_valid':False,'reason':'No complete block/baseline comparison; retained timeout and shared-host test interference; no trial dropped.'},indent=2)+'\n');print('failure and completed-answer audit passed')
if __name__=='__main__':main()
