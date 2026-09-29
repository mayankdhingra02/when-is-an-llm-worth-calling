"""Reconcile request charges and response usage; missing usage remains null."""
import json
from collect_smollm_v47 import ROOT,read,write
from reasoning_v98_common import check_payload

def main():
    raw=ROOT/'results/v99_reasoning';out=ROOT/'results/v99_analysis'
    starts=[json.loads(x) for x in (raw/'generation_starts.jsonl').read_text().splitlines()]
    responses=[json.loads(x) for x in (raw/'responses.jsonl').read_text().splitlines()]
    sm={r['identity']:r for r in starts};rm={r['key']:r for r in responses}
    ledger=read(raw/'ledger.json');jobs=read(ROOT/'artifacts/study_v99/jobs.json')
    allowed={j['key']+'_'+phase for j in jobs for phase in (['thought','final'] if j['mode']=='thinking' else ['final'])}
    assert len(sm)==len(starts)==ledger['generation_requests']<=54
    assert len(rm)==len(responses) and set(rm)<=set(sm)<=allowed
    for row in starts:check_payload(row['payload'])
    assert sum(r['payload']['n_predict'] for r in starts)==ledger['allocated_output_tokens']<=13824
    assert ledger['server_exit_code'] is not None and ledger['stage_seconds']<=1800
    runtime=read(raw/'runtime.json');cmd=runtime['command']
    assert cmd[cmd.index('-c')+1]=='4096' and runtime['config']['context_tokens']==4096
    phases={}
    for phase in ['thought','final']:
        ids=[k for k in sm if k.endswith('_'+phase)]
        rows=[rm[k]['response'] for k in ids if k in rm];missing=[k for k in ids if k not in rm]
        for response in rows:
            assert response['tokens_predicted']<=sm[next(k for k in ids if k in rm and rm[k]['response'] is response)]['payload']['n_predict']
            if 'n_ctx' in response.get('generation_settings',{}):
                assert response['generation_settings']['n_ctx']==4096
        generated=sum(r['tokens_predicted'] for r in rows)
        prefill=[r.get('timings',{}).get('prompt_n') for r in rows]
        unknown_prefill=bool(missing) or any(v is None for v in prefill)
        phases[phase]={'charged_requests':len(ids),'returned_responses':len(rows),'missing_response_ids':missing,
            'returned_generated_tokens':generated,'total_generated_tokens':None if missing else generated,
            'returned_observed_prefill_tokens':sum(v for v in prefill if v is not None),
            'total_actual_prefill_tokens':None if unknown_prefill else sum(prefill)}
    jobs_with_final=sum(j['key']+'_final' in rm for j in jobs if j['mode']=='thinking')
    write(out/'usage_completeness.json',{'scope':'all charged requests, including missing responses',
        'phases':phases,'thinking_final_responses':jobs_with_final,
        'inference_scope':'changed-context development repeat; V98 failure remains separately charged'})
    print(json.dumps(phases,indent=2))

if __name__=='__main__':main()
