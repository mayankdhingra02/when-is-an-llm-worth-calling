"""Portable standard-library replay of saved V123 evidence, not new inference."""
from pathlib import Path
import json,hashlib,csv,re,math
ROOT=Path(__file__).resolve().parent
IDS='0123456789ABCDEFGHIJ';ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def read(n):return json.loads((ROOT/n).read_text())
def lines(n):return [json.loads(x) for x in (ROOT/n).read_text().splitlines()]
def main():
    for n,m in read('manifest.json')['files'].items():
        b=(ROOT/n).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],n
    specs={s['id']:s for s in read('data/manifest_v41.json')['datasets']};jobs=read('artifacts/study_v123/jobs.json');jm={j['key']:j for j in jobs};starts=lines('results/v123_pointwise/generation_starts.jsonl');raw=lines('results/v123_pointwise/responses.jsonl');ledger=read('results/v123_pointwise/ledger.json');scores={}
    assert len(starts)==ledger['generation_requests']<=99 and [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]]
    assert ledger['allocated_output_tokens']==16*len(starts)<=1584 and ledger['retries']==ledger['external_spend_usd']==0
    assert ledger['stage_seconds']<=900 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['server_exit_code']==0
    assert len({r['key'] for r in raw})==len(raw) and set(r['key'] for r in raw)<=set(s['identity'] for s in starts)
    for r in raw:
        out=r['response'];v=out.get('content');n=out.get('tokens_predicted')
        if isinstance(v,str) and re.fullmatch(r'(?:0\.\d{2}|1\.00)',v) and type(n) is int and 0<n<=16 and out.get('truncated') is False and out.get('stop_type')=='eos':scores[r['key']]=float(v)
    for s in starts:
        j=jm[s['identity']];p=read(j['prefix']);body=json.loads(p['messages'][1]['content'].split('\n',1)[1]);pre=read(f"results/v123_pointwise/preflight/{j['key']}.json");msgs=read(j['messages_path']);assert pre['messages']==msgs;user=json.loads(msgs[1]['content'])
        def decode(x):return [domain[ALPHABET.index(ch)] for domain,ch in zip(body['symbol_to_value'],x)]
        obs=[{'settings':decode(o['x']),'normalized_loss':.5 if j['condition']=='loss_blind' else o['loss']} for o in body['observations']]
        if j['condition']=='observations_reversed':obs.reverse()
        assert user['observations']==obs and user['new_configuration']==decode(next(c['x'] for c in body['candidates'] if c['id']==j['candidate_id']))
        assert 'id' not in user and 'candidates' not in user and user['feature_order']==body['feature_order'] and user['task_metric']==specs[j['dataset']]['meaning']
        payload=s['payload'];assert payload=={'prompt':pre['rendered']['prompt'],'n_predict':16,'temperature':0,'seed':11,'grammar':'root ::= '+' | '.join(json.dumps(f'{i/100:.2f}') for i in range(101)),'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
        assert len(pre['prompt_tokens'])+16<=4096
    es=lines('results/v123_analysis/acquisitions.jsonl');summary=read('results/v123_analysis/summary.json');assert summary['complete'] and len(es)==summary['actual_new_acquisitions']==30
    responsive=0;stable=0
    for arm in summary['cases']:
        key=arm['key'];spec=specs[arm['dataset']];p=read(arm['prefix']);body=json.loads(p['messages'][1]['content'].split('\n',1)[1]);normal={i:scores[f'{key}_normal_{i}'] for i in IDS if f'{key}_normal_{i}' in scores}
        if len(normal)==20:
            chosen=sorted(IDS,key=lambda i:(normal[i],IDS.index(i)))[:10];selected=[p['pool']['mapping'][i] for i in chosen];assert not arm['fallback']
        else:
            selected=read(f'results/v41_transfer/arms/{key}_batch_3nn.json')['state']['ids'][10:];assert arm['fallback']
        assert selected==arm['selected_rows'];source=(ROOT/spec['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==spec['sha256'];source=source.decode().splitlines();head=next(csv.reader([source[0]],delimiter=spec['delimiter']));events=[e for e in es if e['key']==key];assert [e['row_id'] for e in events]==selected
        labels=p['state']['labels'][:]
        for e in events:
            assert e['source_line']==spec['subset']['source_lines'][e['row_id']];row=dict(zip(head,next(csv.reader([source[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];v=float(e['raw_target']);assert math.isfinite(v) and v>0;labels.append([v])
        assert arm['state']['ids']==p['state']['ids']+selected and len(set(arm['state']['ids']))==20 and arm['state']['labels']==labels
        choose_best=min if spec['direction']=='-' else max;target=choose_best(y[0] for y in labels);assert target==arm['target']
        for mode,reference in arm['references'].items():
            path=f'results/v41_transfer/arms/{key}_{mode}.json'
            if mode=='presentation_first10':path=f'results/v41_models/0.5/arms/{key}.json'
            elif mode=='single_portfolio':path=f'results/v115_portfolio/arms/{key}.json'
            state=read(path)['state'];assert state['ids'][:10]==p['state']['ids'] and state['labels'][:10]==p['state']['labels'] and len(set(state['ids']))==20
            if mode=='presentation_first10':assert state['ids'][10:]==[p['pool']['mapping'][i] for i in IDS[:10]]
            assert reference==choose_best(y[0] for y in state['labels']);gain=(reference-target)/reference if spec['direction']=='-' else (target-reference)/reference;assert gain==arm['gains'][mode]
        changes=0
        for i in IDS[:10]:
            a=scores.get(f'{key}_normal_{i}');b=scores.get(f'{key}_loss_blind_{i}');changes+=a is not None and b is not None and abs(a-b)+1e-12>=.02
        responsive+=changes>=3
        for i in IDS[:3]:
            a=scores.get(f'{key}_normal_{i}');b=scores.get(f'{key}_observations_reversed_{i}');stable+=a is not None and b is not None and abs(a-b)<=.05+1e-12
    diag=read('results/v123_analysis/diagnostics.json');assert diag['responsive_families']==responsive and diag['stable_order_probes']==stable
    print(json.dumps({'verified':True,'real_requests_replayed':len(starts),'responses':len(raw),'source_events_replayed':len(es),'responsive_families':responsive,'stable_order_probes':stable,'new_inference':0,'new_acquisitions':0}))
if __name__=='__main__':main()
