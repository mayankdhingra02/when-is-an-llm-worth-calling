"""Independent stdlib replay of V49 inputs, traces, mappings and arithmetic."""
import hashlib,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()] if (ROOT/p).exists() else []
def sha(p):
    h=hashlib.sha256()
    with (ROOT/p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def close(a,b):assert math.isclose(a,b,abs_tol=1e-12),(a,b)
def main():
    freeze=read('reports/protocol_v93_decoder.freeze.json')
    for p,h in freeze['sha256'].items():assert sha(p)==h,p
    jobs=read('artifacts/study_v93/jobs.json');bykey={j['key']:j for j in jobs}
    assert len(jobs)==len(bykey)==63
    assert sum(j['decoder']=='native' for j in jobs)==54
    assert {j['system_group'] for j in jobs}=={'mysql_family','brotli','lrzip'}
    starts=lines('results/v93_decoder/request_starts.jsonl');responses=lines('results/v93_decoder/responses.jsonl')
    ledger=read('results/v93_decoder/ledger.json');summary=read('results/v93_analysis/summary.json')
    assert len(starts)==ledger['scientific_requests']<=144
    assert ledger['objective_accesses']==ledger['external_spend_usd']==ledger['retries']==0
    assert ledger['stage_seconds']<=1800 and ledger['server_exit_code']==-9
    assert ledger['peak_server_rss_bytes']>8589934592 and ledger['resource_stop_reason']=='server_rss_cap'
    charges=lines('results/v93_decoder/generation_starts.jsonl')
    assert len(charges)==ledger['generation_requests']==len(starts) and ledger['compatibility_requests']==0
    assert all(c['identity']==r['request_id'] and c['payload']==r['payload'] and c['generation']==i+1 for i,(c,r) in enumerate(zip(charges,starts)))
    assert sum(r['response']['tokens_predicted'] for r in responses)<=7002
    seal=read('results/v93_decoder/preflight_seal.json')
    assert freeze['at']<seal['at']<starts[0]['at']
    for p,h in seal['sha256'].items():assert sha(p)==h,p
    assert len(seal['sha256'])==63
    start_by_id={r['request_id']:r for r in starts};response_by_id={r['request_id']:r for r in responses}
    assert len(start_by_id)==len(starts) and len(response_by_id)==len(responses)
    computed={};IDS='0123456789ABCDEFGHIJ';valid_total=0;completed=0
    for j in jobs:
        p=read(j['prefix']);pre=read(f"results/v93_decoder/preflight/{j['key']}.json")
        oldpre=read(f"results/v92b_sensitivity/preflight/{j['source_key']}.json")
        assert pre['messages']==p['messages']==oldpre['messages']
        assert pre['prompt_tokens']==oldpre['prompt_tokens'] and pre['rendered']['prompt']==oldpre['rendered']['prompt']
        assert len(pre['prompt_tokens'])+(128 if j['decoder']=='native' else 20)<=8192
        used=[];case_responses=sorted([r for r in responses if r['case']==j['key']],key=lambda r:r['step'])
        for r in case_responses:
            q=r['payload'];response=r['response']
            assert start_by_id[r['request_id']]['payload']==q
            assert q['temperature']==0 and q['seed']==11 and q['repeat_penalty']==1 and not q['stream']
            assert q['cache_prompt']==bool(r['step'])
            assert response['tokens_predicted']<=q['n_predict']
            if r['step']==0:assert response['timings']['cache_n']==0
            assert q['prompt']==pre['rendered']['prompt']+''.join(c+'\n' for c in used)
            if j['decoder']=='native':
                assert r['step']==0 and q['n_predict']==128 and 'grammar' not in q
            else:
                assert q['n_predict']==1 and r['step']==len(used)
                assert q['grammar']=='root ::= '+' | '.join(json.dumps(c) for c in IDS if c not in used)
                raw=response['content']
                if len(raw)==1 and raw in IDS and raw not in used:used.append(raw)
        f=ROOT/f"results/v93_decoder/choices/{j['key']}.json"
        if not f.exists():
            computed[j['key']]={'status':'missing','rows':None,'ids':[]};continue
        completed+=1;c=json.loads(f.read_text())
        assert c['request_ids']==[r['request_id'] for r in starts if r['case']==j['key']]
        if j['decoder']=='native':
            assert len(case_responses)==1
            response=case_responses[0]['response'];tokens=[s.strip() for s in response['content'].splitlines() if s.strip()]
            reasons=[]
            if response.get('truncated',False) or response.get('stopped_limit',False) or response.get('stop_type')=='limit':reasons.append('truncated')
            if len(tokens)!=10:reasons.append('wrong_count')
            if any(len(s)!=1 or s not in IDS for s in tokens):reasons.append('invalid_format_or_id')
            if len(set(tokens))!=len(tokens):reasons.append('duplicate')
            assert c['reasons']==reasons and c['parsed_lines']==tokens and c['duplicate']==(len(set(tokens))!=len(tokens))
            valid=not reasons;expected=tokens if valid else []
        else:
            valid=len(used)==10;expected=used if valid else []
        assert c['valid']==valid and c['selected_ids']==expected
        assert c['status']==('valid' if valid else 'invalid')
        valid_total+=valid
        computed[j['key']]={'status':c['status'],'rows':[p['mapping'][i] for i in expected] if valid else None,'ids':expected}
    assert completed==ledger['completed_cases'] and valid_total==ledger['valid_cases']
    cases=read('results/v93_analysis/cases.json');assert len(cases)==63
    for row in cases:
        c=computed[row['key']];j=bykey[row['key']];p=read(j['prefix'])
        assert row['status']==c['status'] and row['selected_rows']==c['rows'] and row['selected_ids']==c['ids']
        old=read(f"results/v92b_sensitivity/choices/{j['source_key']}.json")
        expected=[p['mapping'][i] for i in old['selected_ids']];assert row['historical_selected_rows']==expected
        if c['rows'] is None:assert row['historical_overlap'] is None
        else:
            close(row['historical_overlap'],len(set(c['rows'])&set(expected))/10)
            close(row['displayed_first_ten_fraction'],len(set(c['ids'])&set(p['presentation'][:10]))/10)
    pairs=read('results/v93_analysis/paired.json');assert len(pairs)==63
    seen=set()
    for p in pairs:
        a=bykey[p['a']];b=bykey[p['b']]
        assert a['base_case']==b['base_case']==p['base_case'] and a['system_group']==b['system_group']==p['system_group']
        assert a['decoder']==b['decoder']=='native'
        if p['intervention']=='loss_removal':
            assert a['loss_mode']=='observed' and b['loss_mode']=='withheld' and a['presentation_mode']==b['presentation_mode']==p['context']
        else:
            assert a['presentation_mode']=='base' and b['presentation_mode']==p['intervention'] and a['loss_mode']==b['loss_mode']==p['context']
        seen.add((p['base_case'],p['intervention'],p['context']))
        aa=computed[p['a']]['rows'];bb=computed[p['b']]['rows']
        if aa is None or bb is None:assert p['overlap'] is None
        else:close(p['overlap'],len(set(aa)&set(bb))/10)
    assert len(seen)==63
    for s in summary['paired_sensitivities']:
        pp=[p for p in pairs if (p['intervention'],p['context'])==(s['intervention'],s['context'])]
        assert s['intended']==len(pp)==9
        assert s['valid']==sum(p['overlap'] is not None for p in pp)
        assert s['set_changes']==sum(p['overlap'] is not None and p['overlap']<1 for p in pp)
        lows=[];highs=[]
        for group,g in s['families'].items():
            gg=[p for p in pp if p['system_group']==group];values=[p['overlap'] for p in gg if p['overlap'] is not None]
            assert g['intended']==len(gg)==3 and g['valid']==len(values)
            assert g['set_changes']==sum(x<1 for x in values)
            lo=sum(values)/3;hi=(sum(values)+3-len(values))/3
            close(g['overlap_lower'],lo);close(g['overlap_upper'],hi);lows.append(lo);highs.append(hi)
        close(s['family_mean_overlap_lower'],statistics.mean(lows));close(s['family_mean_overlap_upper'],statistics.mean(highs))
    chosen={(s['intervention'],s['context']):s for s in summary['paired_sensitivities']}
    native=[r for r in cases if r['decoder']=='native'];forced=[r for r in cases if r['decoder']=='forced']
    valid=sum(r['status']=='valid' for r in native);assert valid==summary['native_valid']
    screen={'format_reliability_pass':valid/54>=.95,'loss_responsiveness_pass':sum(g['set_changes']>=2 for g in chosen['loss_removal','base']['families'].values())>=2,
        'row_stability_pass':all(chosen[o,'observed']['family_mean_overlap_lower']>=.8 for o in ('reverse','relabel')),
        'forced_reproduction_pass':all(r['historical_overlap']==1 for r in forced)}
    screen['screen_pass']=all(screen.values());assert screen==summary['screen']
    for mode,cost in summary['cost']['by_decoder'].items():
        rr=[r for r in responses if bykey[r['case']]['decoder']==mode]
        assert cost['requests']==sum(bykey[r['case']]['decoder']==mode for r in starts) and cost['responses']==len(rr)
        assert cost['generated_tokens']==sum(r['response']['tokens_predicted'] for r in rr)
        assert cost['input_full_context_tokens']==sum(r['response']['tokens_evaluated'] for r in rr)
        assert cost['actual_prefill_tokens_reported']==sum(r['response']['timings']['prompt_n'] for r in rr)
        close(cost['request_wall_seconds'],sum(r['wall_seconds'] for r in rr))
    print(json.dumps({'verified':True,'completion_status':'incomplete_resource_stopped','frozen_files':len(freeze['sha256']),'checked_prompts':63,'checked_requests':len(starts),'checked_responses':len(responses),
        'checked_pairs':len(pairs),'native_valid':valid,'screen':screen,'new_objective_accesses':0,
        'scope':'Independent stdlib saved-evidence replay; no target-table reads or new inference.'},indent=2))
if __name__=='__main__':main()
