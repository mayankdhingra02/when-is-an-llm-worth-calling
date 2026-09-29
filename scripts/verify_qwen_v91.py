"""Independent stdlib audit of recorded outcomes, budgets and request traces."""
import csv,hashlib,json,math,statistics
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def sha(p):
    from collect_smollm_v47 import sha as stream_sha
    return stream_sha(ROOT/p)
def main():
    freeze=read('reports/protocol_v91.freeze.json')
    for p,h in freeze['sha256'].items():assert sha(p)==h,p
    seal=read('results/v91_qwen/preflight_seal.json')
    for p,h in seal['sha256'].items():assert sha(p)==h
    ledger=read('results/v91_qwen/ledger.json');summary=read('results/v91_analysis/summary.json')
    starts=rows('results/v91_qwen/request_starts.jsonl');responses=rows('results/v91_qwen/responses.jsonl')
    events=rows('results/v91_analysis/acquisitions.jsonl');cases=read('results/v91_analysis/cases.json')
    specs={d['id']:d for d in read('data/manifest_v41.json')['datasets']}
    assert len(starts)==len(responses)==ledger['scientific_requests']==300
    assert len(events)==300 and len(cases)==30 and summary['fallbacks']==0
    assert ledger['server_exit_code']==0 and ledger['stage_seconds']<1800 and ledger['generation_requests']==303 and ledger['compatibility_requests']==3 and ledger['resource_stop_reason'] is None
    assert seal['at']<starts[0]['at']
    response_map={r['request_id']:r for r in responses}
    assert len(response_map)==300
    for r in starts:
        rr=response_map[r['request_id']]
        assert rr['payload']==r['payload'] and rr['status']=='response'
        assert rr['response']['tokens_predicted']==1 and not rr['response']['truncated']
    targets={k:list(csv.DictReader((ROOT/s['path']).open(),delimiter=s['delimiter'])) for k,s in specs.items()}
    for s in specs.values():assert sha(s['path'])==s['sha256']
    sequence_counts=Counter();row_matches={'0.5':0,'1.5':0};gain_values={};first10_matches=0
    for row in cases:
        key=row['key'];p=read(row['prefix']);s=specs[row['dataset']]
        c=read(f'results/v91_qwen/choices/{key}.json');arm=read(f'results/v91_analysis/arms/{key}.json')
        pre=read(f'results/v91_qwen/preflight/{key}.json')
        assert pre['messages']==p['messages']
        ids=c['selected_ids'];assert len(ids)==len(set(ids))==10
        sequence_counts[tuple(ids)]+=1
        first10_matches+=ids==list('0123456789')
        for i,request_id in enumerate(c['request_ids']):
            r=response_map[request_id];payload=r['payload'];response=r['response']
            assert payload['prompt']==pre['rendered']['prompt']+''.join(x+'\n' for x in ids[:i])
            allowed=[x for x in '0123456789ABCDEFGHIJ' if x not in ids[:i]]
            assert payload['grammar']=='root ::= '+' | '.join(json.dumps(x) for x in allowed)
            assert payload['n_predict']==1 and response['content']==ids[i]
            assert payload['cache_prompt']==bool(i)
            if i==0:assert response['timings']['cache_n']==0
        selected=[p['pool']['mapping'][x] for x in ids]
        assert arm['state']['ids']==p['state']['ids']+selected
        assert len(set(arm['state']['ids']))==20
        observed=[e for e in events if e['case']==key];assert len(observed)==10
        assert [e['row_id'] for e in observed]==selected
        new=[]
        for e in observed:
            line=s['subset']['source_lines'][e['row_id']]
            assert e['source_line']==line
            raw=targets[row['dataset']][line-2][s['primary_objective']]
            assert raw==e['raw_target'];new.append([float(raw)])
        assert arm['state']['labels']==p['state']['labels']+new
        target=(min if s['direction']=='-' else max)(x[0] for x in arm['state']['labels'])
        assert target==row['target']
        for size in ('0.5','1.5'):
            old=read(f'results/v41_models/{size}/arms/{key}.json')
            row_matches[size]+=old['state']['ids'][10:]==selected
        for name,reference in row['references'].items():
            path=f'results/v41_models/{name[5:]}/arms/{key}.json' if name.startswith('qwen_') else f'results/v41_transfer/arms/{key}_{name}.json'
            if name=='smollm_3b':path=f'results/v47_analysis/arms/{key}.json'
            if name=='presentation_first10':path=f'results/v41_models/0.5/arms/{key}.json'
            old=read(path)['state']
            assert old['ids'][:10]==p['state']['ids'] and old['labels'][:10]==p['state']['labels']
            assert reference==(min if s['direction']=='-' else max)(x[0] for x in old['labels'])
            gain=((reference-target) if s['direction']=='-' else (target-reference))/reference
            assert math.isclose(gain,row['gains'][name],abs_tol=1e-14)
            gain_values.setdefault(name,[]).append((row['system_group'],gain))
    for name,values in gain_values.items():
        expected={g:statistics.mean(v for gg,v in values if g==gg) for g,_ in values}
        actual=summary['contrasts'][name]
        assert all(math.isclose(v,actual['family_means'][g],abs_tol=1e-14) for g,v in expected.items())
        assert math.isclose(statistics.mean(expected.values()),actual['family_mean_gain'],abs_tol=1e-14)
        assert actual['wins']==sum(v>1e-12 for _,v in values)
        assert actual['harms']==sum(v< -1e-12 for _,v in values)
    decisions=read('results/v41_policy_precommit/decisions.json')
    indexes={(r['dataset'],r['seed']):i for i,r in enumerate(decisions['rows'])}
    for policy in summary['policies']:
        name,ref=policy['policy'],policy['comparator']
        mask=[r['gains'][ref]>0 for r in cases] if name=='hindsight_oracle_diagnostic' else [decisions['masks'][name][indexes[(r['dataset'],r['seed'])]] for r in cases]
        assert sum(mask)==policy['selected_cases']
        assert sum(mask)*10==policy['generation_requests_if_deployed']
        means=[statistics.mean(r['gains'][ref] if m else 0 for r,m in zip(cases,mask) if r['system_group']==g) for g in {r['system_group'] for r in cases}]
        assert math.isclose(statistics.mean(means),policy['contrast']['family_mean_gain'],abs_tol=1e-14)
    receipt={'verified':True,'acquisitions_source_checked':300,'generation_requests_checked':300,
        'paired_contrasts_checked':330,'policy_summaries_checked':len(summary['policies']),
        'first_ten_ID_sequence_cases':first10_matches,'exact_Qwen_row_sequence_matches':row_matches,
        'sequence_counts':[{'ids':list(k),'cases':v} for k,v in sequence_counts.items()],
        'generated_choice_tokens':sum(r['response']['tokens_predicted'] for r in responses),
        'full_context_input_token_sum':sum(r['response']['tokens_evaluated'] for r in responses),
        'actually_prefilled_tokens_reported':sum(r['response']['timings']['prompt_n'] for r in responses),
        'generation_request_wall_seconds':sum(r['wall_seconds'] for r in responses),
        'source':'All costs/results derive from preserved real local responses and existing source tables; no synthetic research outcomes.'}
    (ROOT/'artifacts/study_v91/independent_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
