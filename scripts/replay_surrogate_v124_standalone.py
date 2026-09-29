"""Standard-library replay of saved V124 evidence. No inference/acquisitions."""
from pathlib import Path
import json,csv,hashlib,re,math,statistics
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;IDS='0123456789ABCDEFGHIJ';SEEDS=(101,102,103);ORDER=[2,8,4,9,1,6,7,3,0,5]
def read(n):return json.loads((ROOT/n).read_text())
def lines(n):return [json.loads(x) for x in (ROOT/n).read_text().splitlines()]
def main():
    manifest=read('manifest.json')
    for n,m in manifest['files'].items():
        b=(ROOT/n).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],n
    jobs=read('artifacts/study_v124/jobs.json');jm={j['key']:j for j in jobs};starts=lines('results/v124_surrogate/generation_starts.jsonl');raw=lines('results/v124_surrogate/responses.jsonl');ledger=read('results/v124_surrogate/ledger.json');sm={s['identity']:s for s in starts};scores={}
    assert len(starts)==len(sm)==ledger['generation_requests']<=180 and ledger['allocated_output_tokens']==32*len(starts)<=5760
    assert ledger['retries']==ledger['external_spend_usd']==0 and ledger['stage_seconds']<=1500 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['server_exit_code']==0
    assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]] and len({r['key'] for r in raw})==len(raw)
    for r in raw:
        p=sm[r['key']]['payload'];o=r['response'];assert o['prompt']==p['prompt']
        for k in ['seed','n_predict','temperature','top_p','top_k','min_p','repeat_penalty']:assert math.isclose(o['generation_settings'][k],p[k],rel_tol=0,abs_tol=1e-6)
        assert not o['generation_settings'].get('grammar');v=o.get('content');n=o.get('tokens_predicted');m=None if not isinstance(v,str) else re.fullmatch(r'\s*## (-?(?:\d+(?:\.\d*)?|\.\d+)) ##\s*',v)
        if m and type(n) is int and 0<n<=32 and o.get('truncated') is False and o.get('stop_type')=='eos' and math.isfinite(float(m[1])):scores[r['key']]=float(m[1])
    for s in starts:
        j=jm[s['identity']];p=read(j['prefix']);pre=read(f"results/v124_surrogate/preflight/{j['key']}.json");msgs=read(j['messages_path']);assert pre['messages']==msgs;body=json.loads(p['messages'][1]['content'].split('\n',1)[1]);user=json.loads(msgs[1]['content']);alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        def decode(x):return [domain[alphabet.index(ch)] for domain,ch in zip(body['symbol_to_value'],x)]
        assert user['observed_examples']==[{'settings':decode(body['observations'][i]['x']),'performance':f"{p['state']['labels'][i][0]:.6f}"} for i in ORDER]
        assert user['new_configuration']==decode(next(c['x'] for c in body['candidates'] if c['id']==j['candidate_id'])) and 'candidates' not in user and 'id' not in user
        assert s['payload']=={'prompt':pre['rendered']['prompt'],'n_predict':32,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.,'seed':j['sampling_seed'],'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0};assert len(pre['prompt_tokens'])+32<=4096
    specs={s['id']:s for s in read('data/manifest_v41.json')['datasets']};es=lines('results/v124_analysis/acquisitions.jsonl');summary=read('results/v124_analysis/summary.json');assert summary['complete'] and len(summary['cases'])==6 and len(es)==summary['actual_new_acquisitions']==60
    for arm in summary['cases']:
        key=arm['base_key'];p=read(arm['prefix']);values={i:[scores[f'{key}_{i}_{seed}'] for seed in SEEDS if f'{key}_{i}_{seed}' in scores] for i in IDS};valid=all(len(v)>=2 for v in values.values());assert arm['fallback']==(not valid)
        if valid:
            best=min(v[0] for v in p['state']['labels']);stats={}
            for i,v in values.items():
                mean=statistics.mean(v);std=statistics.pstdev(v);sd=max(std,1e-5);delta=best-mean;z=delta/sd;ei=max(0.,delta*.5*(1+math.erf(z/math.sqrt(2)))+sd*math.exp(-.5*z*z)/math.sqrt(2*math.pi));stats[i]={'values':v,'mean':mean,'population_std':std,'ei':ei}
            assert stats==arm['statistics'];ids=sorted(IDS,key=lambda i:((-stats[i]['ei'] if arm['mode']=='ei' else stats[i]['mean']),IDS.index(i)))[:10];selected=[p['pool']['mapping'][i] for i in ids];assert ids==arm['selected_ids']
        else:selected=read(f'results/v41_transfer/arms/{key}_batch_3nn.json')['state']['ids'][10:]
        assert selected==arm['selected_rows'];spec=specs[arm['dataset']];source=(ROOT/spec['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==spec['sha256'];source=source.decode().splitlines();head=next(csv.reader([source[0]],delimiter=spec['delimiter']));events=[e for e in es if e['key']==arm['key']];assert [e['row_id'] for e in events]==selected;labels=p['state']['labels'][:]
        for e in events:
            assert e['source_line']==spec['subset']['source_lines'][e['row_id']];row=dict(zip(head,next(csv.reader([source[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];v=float(e['raw_target']);assert math.isfinite(v) and v>0;labels.append([v])
        assert arm['state']['ids']==p['state']['ids']+selected and len(set(arm['state']['ids']))==20 and arm['state']['labels']==labels;target=min(y[0] for y in labels);assert target==arm['target']
        for mode,ref in arm['references'].items():
            path=f'results/v41_transfer/arms/{key}_{mode}.json'
            if mode=='presentation_first10':path=f'results/v41_models/0.5/arms/{key}.json'
            elif mode=='single_portfolio':path=f'results/v115_portfolio/arms/{key}.json'
            state=read(path)['state'];assert state['ids'][:10]==p['state']['ids'] and state['labels'][:10]==p['state']['labels'] and len(set(state['ids']))==20
            if mode=='presentation_first10':assert state['ids'][10:]==[p['pool']['mapping'][i] for i in IDS[:10]]
            assert ref==min(y[0] for y in state['labels']) and arm['gains'][mode]==(ref-target)/ref
    diag=read('results/v124_analysis/diagnostics.json');assert len(scores)==diag['valid_scores'] and len(raw)==diag['returned']
    if (ROOT/'results/v125_design_audit/attainability.json').exists():
        audit=read('results/v125_design_audit/attainability.json');old=read('results/v42_selection_reference/summary.json');possible=0
        for r in old['ceiling_comparisons']:
            if r['reference']=='batch_3nn':possible+=Fraction(r['exact_ceiling_gain'])>=Fraction('0.05')
        assert possible==audit['historical_30cases_batch_5pct_attainable_cases']==0
        for r in audit['current_cases']:
            p=read(next(j['prefix'] for j in read('artifacts/study_v124/cases.json') if j['key']==r['key']));c=next(c for c in old['cases'] if c['dataset']==p['dataset'] and c['seed']==p['seed']);assert c['candidate_ids']==p['pool']['ranked'];ceiling=min([Fraction(c['prefix_best'])]+[Fraction(y) for y in c['acquired_candidate_targets']]);assert ceiling==Fraction(r['hindsight_ceiling_exact'])
            arm=read(f"results/v124_analysis/arms/{r['key']}_ei.json")
            for m,v in arm['references'].items():assert (Fraction(str(v))-ceiling)/Fraction(str(v))==Fraction(r['max_relative_gains_exact'][m])
    print(json.dumps({'verified':True,'hashed_files':len(manifest['files']),'real_requests_replayed':len(starts),'valid_predictions':len(scores),'source_events_replayed':60,'paired_arms':6,'new_inference':0,'new_acquisitions':0}))
if __name__=='__main__':main()
