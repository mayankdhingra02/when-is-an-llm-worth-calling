"""Supplementary accounting checks; no policy changes or inference."""
import hashlib,math

def finite_nonnegative(value):
    assert type(value) in (int,float) and math.isfinite(value) and value>=0
    return value

def request_receipt(request,rendered,response,decision,seed):
    payload=request['payload'];prompt=rendered['rendered']['prompt']
    assert payload['prompt']==prompt and request['prompt_sha256']==hashlib.sha256(prompt.encode()).hexdigest()
    assert len(rendered['tokens'])+64<=4096
    for key,value in {'n_predict':64,'temperature':0,'seed':seed,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}.items():assert payload[key]==value,key
    expected={key:response.get(key) for key in ['tokens_predicted','tokens_evaluated']}
    assert decision['usage']==expected
    for key,value in expected.items():
        if value is not None:assert type(value) is int and value>=0
    if expected['tokens_predicted'] is not None:assert expected['tokens_predicted']<=64
    finite_nonnegative(decision['wall_seconds'])
    return expected

def completed_accounting(cases,decisions,starts,ledger):
    """Requires all five complete cases; parse failures can reduce actual calls."""
    assert {c['seed'] for c in cases}=={11,23,37,53,71} and len(cases)==5
    expected_ids=[];fallbacks=0
    for case in cases:
        failed=False;expected_fallback=[]
        for step in range(1,8):
            name=f'v78_seed{case["seed"]}_step{step}'
            if not failed:
                expected_ids.append(name);d=decisions[name]
                assert type(d['valid']) is bool
                failed=not d['valid']
            if failed:expected_fallback.append(step)
        assert case['fallback_steps']==expected_fallback
        fallbacks+=len(expected_fallback)
    assert set(decisions)==set(expected_ids) and len(decisions)==len(expected_ids)
    startids=[s['request_id'] for s in starts];assert startids==expected_ids
    assert ledger['generation_requests']==len(expected_ids)<=35
    assert ledger['intended_generation_requests']==35 and ledger['unattempted_generation_requests']==35-len(expected_ids)
    assert ledger['fallback_search_evaluations']==fallbacks and ledger['retries']==0 and ledger['external_spend_usd']==0
    assert ledger['stop_reason'] is None and ledger['resource_guard']['reason'] is None
    assert finite_nonnegative(ledger['seconds'])<=1800 and finite_nonnegative(ledger['startup_seconds'])<=120
    assert finite_nonnegative(ledger['resource_guard']['peak_server_rss_bytes'])<=8*1024**3
    assert ledger['server_exit_code'] is not None
    return {'requests':len(expected_ids),'fallback_search_slots':fallbacks,'invalid_responses':sum(not d['valid'] for d in decisions.values())}

def trial_limits(result,supervision):
    assert supervision['exit_code']==0 and supervision['termination_reason'] is None
    finite_nonnegative(supervision['wall_seconds'])
    for phase in ['compression','decompression']:
        receipt=result[phase]
        assert receipt['exit_code']==0 and receipt['termination_reason'] is None
        assert finite_nonnegative(receipt['wall_seconds'])<=40
        assert finite_nonnegative(receipt['sampled_maxima']['rss_bytes'])<=2*1024**3
        assert finite_nonnegative(receipt['sampled_maxima']['scratch_bytes'])<=128*1024**2

def selection_costs(cases,costs):
    expected={(c['seed'],method,step):(c['arms'][method][step+9]['config_id']) for c in cases for method in ['rf_lcb','nn','llm'] for step in range(1,8)}
    assert len(costs)==len(expected)==105
    seen=set();totals={m:0.0 for m in ['rf_lcb','nn','llm']}
    for row in costs:
        key=(row['seed'],row['arm'],row['step']);assert key not in seen and row['config_id']==expected[key];seen.add(key)
        totals[row['arm']]+=finite_nonnegative(row['seconds'])
    return totals
