"""Independent stdlib checks of diagnostic inputs, real traces and aggregates."""
import hashlib,itertools,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(x) for x in (ROOT/p).read_text().splitlines()]
from collect_smollm_v47 import sha as streaming_sha
def sha(p):return streaming_sha(ROOT/p)
def close(a,b):assert math.isclose(a,b,abs_tol=1e-12),(a,b)
def main():
    IDS='0123456789ABCDEFGHIJ';alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    freeze=read('reports/protocol_v92b.freeze.json')
    for p,h in freeze['sha256'].items():assert sha(p)==h,p
    jobs=read('artifacts/study_v48/jobs.json');summary=read('results/v92b_analysis/summary.json')
    ledger=read('results/v92b_sensitivity/ledger.json');historical=lines('results/v8/requests.jsonl')
    starts=lines('results/v92b_sensitivity/request_starts.jsonl');responses=lines('results/v92b_sensitivity/responses.jsonl')
    assert len(jobs)==ledger['completed_cases']==108
    assert len(starts)==len(responses)==ledger['scientific_requests']==1080
    assert ledger['server_exit_code']==0 and ledger['stage_seconds']<1799
    assert ledger['generation_requests']==1080 and ledger['compatibility_requests']==0
    assert ledger['peak_server_rss_bytes']<=8589934592 and ledger['resource_stop_reason'] is None
    charges=lines('results/v92b_sensitivity/generation_starts.jsonl')
    assert len(charges)==1080 and [c['generation'] for c in charges]==list(range(1,1081))
    assert [c['identity'] for c in charges]==[r['request_id'] for r in starts]
    assert all(c['kind']=='scientific' and c['payload']==r['payload'] for c,r in zip(charges,starts))
    assert ledger['objective_accesses']==0 and ledger['external_spend_usd']==0 and ledger['retries']==0
    seal=read('results/v92b_sensitivity/preflight_seal.json')
    assert seal['at']<starts[0]['at']
    for p,h in seal['sha256'].items():assert sha(p)==h
    response={r['request_id']:r for r in responses};request={r['request_id']:r for r in starts}
    assert len(response)==len(request)==1080
    for k,r in response.items():
        assert r['payload']==request[k]['payload'] and r['status']=='response'
        assert r['response']['tokens_predicted']==1 and not r['response']['truncated']
    configurations={};same_baseline_messages=0;verified_prompts=0
    for job in jobs:
        p=read(job['prefix']);key=job['key'];base=job['base_case']
        old=next(r for r in historical if r['dataset']==job['dataset'] and r['seed']==job['seed'])
        assert old['split']=='development' and old['system_group'] in ('mysql_family','brotli','lrzip')
        body=json.loads(old['messages'][1]['content'].split('\n',1)[1])
        candidate_specs={r['id']:r['x'] for r in body['candidates']}
        original_mapping=p['source_pool']['mapping']
        mode=job['presentation_mode']
        transform={c:IDS[(i+10)%20] if mode=='relabel' else c for i,c in enumerate(IDS)}
        expected_mapping={transform[c]:row for c,row in original_mapping.items()}
        candidate_order=list(candidate_specs)
        if mode=='reverse':candidate_order.reverse()
        expected_display=[transform[c] for c in candidate_order]
        assert p['mapping']==expected_mapping and p['presentation']==expected_display
        assert set(p['mapping'].values())==set(original_mapping.values())
        assert p['messages'][0]==old['messages'][0]
        content=p['messages'][1]['content'];observed=job['loss_mode']=='observed'
        expected_observations=[dict(r) for r in body['observations']]
        if not observed:
            for r in expected_observations:del r['loss']
            assert 'losses are withheld' in content
        if job['representation']=='symbols':
            actual=json.loads(content.split('\n',1)[1])
            assert actual['observations']==expected_observations
            assert actual['feature_order']==body['feature_order'] and actual['symbol_to_value']==body['symbol_to_value']
            assert actual['candidates']==[{'id':transform[c],'x':candidate_specs[c]} for c in candidate_order]
            if observed and mode=='base':
                assert p['messages']==old['messages'];same_baseline_messages+=1
        else:
            header,rest=content.split('feature_order=',1)
            features,rest=rest.split('\nOBSERVATIONS\n',1)
            assert json.loads(features)==body['feature_order']
            obs,cand=rest.split('CANDIDATES\n')
            def values(x):return [d[alphabet.index(c)] for c,d in zip(x,body['symbol_to_value'])]
            expected=[]
            for r in expected_observations:
                line='settings='+json.dumps(values(r['x']),separators=(',',':'))
                if observed:line+=' loss='+json.dumps(r['loss'])
                expected.append(line)
            assert obs.splitlines()==expected
            assert cand.splitlines()==[transform[c]+' settings='+json.dumps(values(candidate_specs[c]),separators=(',',':')) for c in candidate_order]
        pre=read(f'results/v92b_sensitivity/preflight/{key}.json')
        assert pre['messages']==p['messages'] and pre['prefix_hash']==p['prefix_hash']
        assert len(pre['prompt_tokens'])+20<=8192
        choice=read(f'results/v92b_sensitivity/choices/{key}.json')
        ids=choice['selected_ids'];assert len(ids)==len(set(ids))==10 and choice['fallback_reason'] is None
        for i,rid in enumerate(choice['request_ids']):
            r=response[rid];a=r['payload'];b=r['response']
            assert b['content']==ids[i]
            assert a['prompt']==pre['rendered']['prompt']+''.join(c+'\n' for c in ids[:i])
            assert a['grammar']=='root ::= '+' | '.join(json.dumps(c) for c in IDS if c not in ids[:i])
            assert a['n_predict']==1 and a['cache_prompt']==bool(i)
            if not i:assert b['timings']['cache_n']==0
        configurations[base,job['representation'],job['loss_mode'],mode]=(job['system_group'],{p['mapping'][c] for c in ids})
        verified_prompts+=1
    paired=read('results/v92b_analysis/paired.json')
    assert len(paired)==126
    for r in paired:
        base,rep=r['base_case'],r['representation']
        if r['intervention']=='loss_removal':
            a=configurations[base,rep,'observed',r['context']][1];b=configurations[base,rep,'withheld',r['context']][1]
        else:
            a=configurations[base,rep,r['context'],'base'][1];b=configurations[base,rep,r['context'],r['intervention']][1]
        ov=len(a&b)/10;close(ov,r['overlap']);assert r['set_changed']==(a!=b)
    for s in summary['paired_sensitivities']:
        rr=[r for r in paired if (r['representation'],r['intervention'],r['context'])==(s['representation'],s['intervention'],s['context'])]
        assert len(rr)==9 and s['paired_cases']==9
        assert sum(r['set_changed'] for r in rr)==s['set_changes']
        means=[]
        for g,t in s['families'].items():
            gg=[r for r in rr if r['system_group']==g];assert len(gg)==3
            mean=statistics.mean(x['overlap'] for x in gg);means.append(mean)
            close(mean,t['mean_overlap']);assert t['set_changes']==sum(x['set_changed'] for x in gg)
        close(statistics.mean(means),s['family_mean_overlap'])
    cases=read('results/v92b_analysis/cases.json');assert len(cases)==108
    for rate in summary['ordering_rates']:
        rr=[r for r in cases if all(r[k]==rate[k] for k in ('representation','loss_mode','presentation_mode'))]
        assert len(rr)==9
        assert sum(set(r['selected_ids'])==set(IDS[:10]) for r in rr)==rate['lowest_ten_ID_sets']
        fractions=[]
        for r in rr:
            p=read(r['prefix']);fractions.append(len(set(r['selected_ids'])&set(p['presentation'][:10]))/10)
        close(statistics.mean(fractions),rate['mean_displayed_first_ten_fraction'])
    for rep,s in summary['screens'].items():
        ss={(a['intervention'],a['context']):a for a in summary['paired_sensitivities'] if a['representation']==rep}
        responsive=sum(g['set_changes']>=2 for g in ss['loss_removal','base']['families'].values())>=2
        stable=all(ss[o,'observed']['family_mean_overlap']>=.8 for o in ('reverse','relabel'))
        assert s['loss_responsiveness_pass']==responsive and s['row_stability_pass']==stable and s['screen_pass']==(responsive and stable)
    for field,source in [('input_full_context_tokens','tokens_evaluated'),('generated_choice_tokens','tokens_predicted')]:
        assert summary['cost'][field]==sum(r['response'][source] for r in responses)
    receipt={'verified':True,'checked_prompts':verified_prompts,'unchanged_original_symbol_baselines':same_baseline_messages,
        'checked_requests':1080,'checked_paired_sensitivities':126,'new_objective_accesses':0,
        'screens':summary['screens'],'scope':'Independent read-only stdlib replay; source is saved development messages, no raw objective tables opened.'}
    (ROOT/'artifacts/study_v92/verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
