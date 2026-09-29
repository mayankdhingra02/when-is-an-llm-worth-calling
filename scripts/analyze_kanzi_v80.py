"""Independent acquired-only replay of the prospective V78 batch; no inference."""
import hashlib,json,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid,features,SEEDS
from escalation.kanzi_v79 import choose
from escalation.kanzi_policy_v80 import METHODS,messages,vectors
from escalation.legal_proposals_v66 import LegalProposals
from escalation.kanzi_v74 import parse_header,verify_settings

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def analyze():
    for n,d in read(ROOT/'reports/protocol_v80.freeze.json')['sha256'].items():assert sha(ROOT/n)==d,n
    out=ROOT/'results/v80_kanzi_paired';s=read(out/'summary.json');ledger=read(out/'ledger.json')
    assert s['complete'] and s['charged_evaluations']==s['successful_evaluations']==450
    events=read(out/'acquisitions.json');charges=[json.loads(l) for l in (out/'charges.jsonl').read_text().splitlines()]
    assert len(events)==len(charges)==450 and ledger['generation_requests']<=105 and ledger['retries']==0 and ledger['external_spend_usd']==0
    configs=grid();x=features(configs);workloads=read(ROOT/'artifacts/study_v79/workloads.json')['files'];byname={w['name']:w for w in workloads};by_path={r['path']:r for r in events}
    for row,charge in zip(events,charges):
        assert all(row[k]==v for k,v in charge.items() if k!='status') and row['status']=='valid'
        sourcehash=byname[row['workload']]['sha256'];result=read(ROOT/row['path']/'result.json');assert result['status']=='valid' and result['exact_byte_equality']
        assert result['config']==configs[row['config_id']] and result['compressed_bytes']==row['compressed_bytes']
        assert result['decoded_sha256']==result['input_sha256']==sourcehash and result['decoded_bytes']==byname[row['workload']]['bytes']
        header=parse_header(bytes.fromhex(result['header_hex']));assert header==result['stream_header']
        verify_settings(header,result['config'],(ROOT/row['path']/'compression.log').read_text())
        for phase in ['compression','decompression']:assert result[phase]['exit_code']==0 and result[phase]['termination_reason'] is None
    cases=[];used=[];requests=0;invalid=0;usage=[]
    def check(o,seed,method,ordinal,purpose):
        row=by_path[o['physical_receipt']];assert row['workload']==workload['name'] and row['seed']==seed and row['arm']==method and row['ordinal']==ordinal and row['purpose']==purpose
        assert row['config_id']==o['config_id'] and row['compressed_bytes']==o['compressed_bytes'];used.append(row['path'])
    for workload in workloads:
        for seed in SEEDS:
            case=read(out/f"case_{workload['name']}_{seed}.json");prefixpath=ROOT/f"results/v79_kanzi_classical/prefix_{workload['name']}_{seed}.json";prefix=read(prefixpath)
            assert case['prefix_sha256']==sha(prefixpath);session=LegalProposals(vectors(configs),[o['config_id'] for o in prefix],count=7)
            model_ids=[];arms={}
            for method in METHODS:
                obs=case['arms'][method];assert obs[:10]==prefix and len(obs)==17 and len({o['config_id'] for o in obs})==17
                for j in range(10,17):
                    if method!='llm':cid=choose(x,obs[:j],method,seed)
                    elif session.failure:cid=choose(x,obs[:j],'rf_lcb',seed)
                    else:
                        folder=out/f"v80_{workload['name']}_seed{seed}_step{j-9}";assert read(folder/'messages.json')==messages(configs,obs[:j],workload)
                        request=read(folder/'request.json');proposal=session.begin_request();requests+=1
                        assert request['payload']['grammar']==proposal['grammar'] and request['eligible_ids']==proposal['eligible_ids']
                        response=read(folder/'response.json');d=read(folder/'decision.json')
                        parsed=session.finish_request(response.get('content'),truncated=bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type')=='limit'))
                        assert all(d[k]==v for k,v in parsed.items());usage.append(d['usage']);invalid+=not parsed['valid']
                        cid=parsed['selected_id']
                        if cid is None:cid=choose(x,obs[:j],'rf_lcb',seed)
                        else:model_ids.append(cid)
                    assert cid==obs[j]['config_id'];check(obs[j],seed,method,j+1,'search')
                selected=min(obs,key=lambda o:(o['compressed_bytes'],o['config_id']))['config_id'];assert selected==case['selected_config_ids'][method]
                confirmation=case['confirmation'][method];assert len(confirmation)==3
                for j,o in enumerate(confirmation):assert o['config_id']==selected;check(o,seed,method,j+18,'confirmation')
                sizes=[o['compressed_bytes'] for o in confirmation];arms[method]={'config_id':selected,'confirmation_bytes':sizes,'median_bytes':statistics.median(sizes)}
                if method=='llm':arms[method]['incumbent_from_real_model_proposal']=selected in model_ids
            rng=random.Random(seed+80000);expected=[]
            for j in range(7):
                order=list(METHODS);rng.shuffle(order);expected.extend(case['arms'][m][j+10]['physical_receipt'] for m in order)
            for j in range(3):
                order=list(METHODS);rng.shuffle(order);expected.extend(case['confirmation'][m][j]['physical_receipt'] for m in order)
            assert expected==[r['path'] for r in events if r['seed']==seed and r['workload']==workload['name']]
            cases.append({'workload':workload['name'],'seed':seed,'arms':arms,'llm_saved_bytes':{m:arms[m]['median_bytes']-arms['llm']['median_bytes'] for m in ['rf_lcb','preset']}})
    assert sorted(used)==sorted(by_path) and requests==ledger['generation_requests']
    assert ledger['seconds']<=1800 and ledger['resource_guard']['reason'] is None
    assert ledger['resource_guard']['peak_server_rss_bytes']<=8*1024**3 and ledger['server_exit_code']==0
    assert ledger['intended_generation_requests']==105 and ledger['unattempted_generation_requests']==105-requests
    starts=[json.loads(l) for l in (out/'request_starts.jsonl').read_text().splitlines()]
    assert len(starts)==requests and len({s['request_id'] for s in starts})==requests
    selection=[json.loads(l) for l in (out/'selection_costs.jsonl').read_text().splitlines()]
    assert len(selection)==315 and all(s['seconds']>=0 for s in selection)
    fallback=0
    for workload in workloads:
        for seed in SEEDS:
            case=read(out/f"case_{workload['name']}_{seed}.json")
            fallback+=len(case['fallback_steps'])
            for method in METHODS:
                for j,o in enumerate(case['arms'][method][10:],1):
                    matches=[s for s in selection if s['workload']==workload['name'] and s['seed']==seed and s['arm']==method and s['step']==j]
                    assert len(matches)==1 and matches[0]['config_id']==o['config_id']
    assert fallback==ledger['fallback_search_evaluations']
    for row in events:
        receipt=read(ROOT/row['path']/'result.json')
        for phase in ['compression','decompression']:
            p=receipt[phase];assert p['wall_seconds']<=40 and p['sampled_maxima']['rss_bytes']<=2*1024**3 and p['sampled_maxima']['scratch_bytes']<=128*1024**2
    for folder in out.glob('v80_*_seed*_step*'):
        req=read(folder/'request.json');rendered=read(folder/'rendered.json');response=read(folder/'response.json');decision=read(folder/'decision.json')
        assert req['payload']['prompt']==rendered['rendered']['prompt']
        assert hashlib.sha256(req['payload']['prompt'].encode()).hexdigest()==req['prompt_sha256']
        assert req['payload']['n_predict']==64 and req['payload']['temperature']==0 and req['payload']['cache_prompt'] is False
        assert len(rendered['tokens'])+64<=4096
        for key in ['tokens_predicted','tokens_evaluated']:assert decision['usage'][key]==response.get(key)
        assert response.get('tokens_predicted') is None or response['tokens_predicted']<=64
    return {'cases':cases,'new_physical_trials':450,'logical_charges':900,'historical_prefix_trials':150,'requests':requests,'intended_requests':105,'invalid_responses':invalid,
       'mean_seed_median_bytes_by_workload':{w['name']:{m:statistics.mean(c['arms'][m]['median_bytes'] for c in cases if c['workload']==w['name']) for m in METHODS} for w in workloads},
       'usage':{key:{'observed_sum':sum(u[key] for u in usage if u and u.get(key) is not None),'unknown_requests':sum(not u or u.get(key) is None for u in usage)} for key in ['tokens_predicted','tokens_evaluated']},
       'ledger':ledger,'scope':'one development family; no router fit or held-out claim'}
if __name__=='__main__':
    result=analyze();out=ROOT/'results/v80_kanzi_analysis';out.mkdir(exist_ok=True);(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
