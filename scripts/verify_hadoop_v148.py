"""Independent replay of charged records, all search choices, routing and local inference."""
import copy, hashlib, json, math, random
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
from verify_router_v147 import ref_fit, threshold, q
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v148';O=ROOT/'results/v148_hadoop'
MODES=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal'];MODELS=['smollm3_3b','qwen3_8b']
def read(p):return json.loads(Path(p).read_text())
def lines(p):return [json.loads(s) for s in Path(p).read_text().splitlines()]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def close(a,b):assert np.allclose(a,b,rtol=1e-11,atol=1e-12),(a,b)
def dist(a,b):return .5*(abs(a[0]-b[0])+(a[1]!=b[1]))
def value(raw,app):
    assert (raw['framework'],raw['workload'],raw['datasize'])==('hadoop',app,'bigdata')
    assert type(raw['completed']) is bool
    if not raw['completed']:return 7200.,'incomplete_failure_penalty'
    t=float(raw['elapsed_time']);assert math.isfinite(t) and t>0
    return min(t,7200.),'completed_capped' if t>7200 else 'completed'
def nextrow(c,s,mode,anchor=None):
    unseen=[i for i in s['order'] if i not in s['ids']]
    if len(s['ids'])<4 or mode=='random_full':return unseen[0]
    if mode.endswith('neighbor'):
        best=anchor if mode=='fixed_neighbor' else s['ids'][int(np.argmin([y[0] for y in s['labels']]))]
        return min(unseen,key=lambda i:dist(c['x'][i],c['x'][best]))
    assert mode=='sequential_3nn'
    def prediction(i):
        ranked=sorted(enumerate(s['ids']),key=lambda p:(dist(c['x'][i],c['x'][p[1]]),p[0]))[:3]
        return sum(s['labels'][j][0] for j,_ in ranked)/len(ranked)
    return min(unseen,key=prediction)
def project(c,p,proposals):
    seen=set(p['ids']);ids=[];prior=[];ds=[]
    for row in proposals:
        target=[row[0]/9,row[1]];i=min([i for i in p['order'] if i not in seen],key=lambda i:dist(c['x'][i],target));seen.add(i);ids.append(i)
        ds.append({'row_id':i,'distance':dist(c['x'][i],target),'repeated_proposal':list(row) in prior,'matches_prefix':any(dist(target,c['x'][j])==0 for j in p['ids'])});prior.append(list(row))
    return ids,ds

def prefix_features(p,c):
    y=[v[0] for v in p['labels']];best=[min(y[:i+1]) for i in range(10)];rng=random.Random(132000)
    boot=[min(y[rng.randrange(10)] for _ in range(10)) for _ in range(64)]
    return [math.log1p(len(p['order'])),sum(len(d)>1 for d in c['domains']),np.mean([len(d) for d in c['domains']]),np.std(y)/np.mean(y),(best[0]-best[-1])/best[0],(9-max(i for i in range(10) if i==0 or best[i]!=best[i-1]))/9,np.std(boot)/np.mean(y)]

def bundle():
    return {'events':lines(O/'acquisitions.jsonl'),'report':read(O/'comparison.json'),'seal':read(O/'selection_seal.json'),
            'ledgers':{m:read(ROOT/'results/v148_models'/m/'ledger.json') for m in MODELS}}

def verify(b):
    jobs=read(A/'jobs.json');assert len(jobs)==15
    candidates={app:read(A/'candidates'/f'{app}.json') for app in ['pagerank','terasort','wordcount']}
    for app,c in candidates.items():
        assert len(c['x'])==69 and c['system_group']=='hadoop_mapreduce'
        expected=[]
        for n in c['sources']:
            fields=Path(n).parent.name.split('_');assert fields[2:]==[app,'hadoop','bigdata','1'];expected.append([int(fields[0]),fields[1]])
        assert expected==c['raw_features'];ds=[sorted({x[i] for x in expected}) for i in range(2)];assert ds==c['domains']
        close(c['x'],[[(x[0]-ds[0][0])/(ds[0][-1]-ds[0][0]),ds[1].index(x[1])] for x in expected])
    events=b['events'];report=b['report'];assert len(events)==1200==read(O/'ledger.json')['acquisitions']
    grouped={k:[e for e in events if e['key']==k] for k in {e['key'] for e in events}}
    assert len(grouped)==120 and all(len(v)==10 for v in grouped.values())
    mapping={}
    for j in jobs:
        for suffix in ['prefix']+MODES:mapping[j['key']+'_'+suffix]=j
        for m in MODELS:mapping[m+'_'+j['key']]=j
    assert set(mapping)==set(grouped)
    for e in events:
        j=mapping[e['key']];c=candidates[j['app']];i=e['row_id'];assert e['source']==c['sources'][i] and e['source_sha256']==c['source_hashes'][i]==sha(ROOT/e['source'])
        raw=read(ROOT/e['source']);assert raw==e['raw_record'];v,status=value(raw,j['app']);assert e['value']==v and e['status']==status
    decision=read(A/'decisions.json');ledger=read(O/'ledger.json')
    assert read(ROOT/'reports/protocol_v148.freeze.json')['at_unix']<=min(e['at_unix'] for e in events)
    classical_events=[e for e in events if e['key'] in {j['key']+'_'+mode for j in jobs for mode in MODES}]
    model_events=[e for e in events if e['key'].startswith(tuple(m+'_' for m in MODELS))]
    assert max(e['at_unix'] for e in events if e['key'].endswith('_prefix'))<=decision['at_unix']<min(e['at_unix'] for e in classical_events)
    assert b['seal']['choices_sha256']==sha(O/'choices.json') and b['seal']['at_unix']<min(e['at_unix'] for e in model_events)
    expected_states={}
    for j in jobs:
        c=candidates[j['app']];p=read(ROOT/j['prefix']);assert sha(ROOT/j['prefix'])==j['prefix_sha256'];order=list(range(69));random.Random(j['seed']).shuffle(order);assert p['order']==order
        s={'ids':[],'labels':[],'order':order}
        for event in grouped[j['key']+'_prefix']:
            i=nextrow(c,s,'sequential_3nn');assert i==event['row_id'];s['ids'].append(i);s['labels'].append([event['value']])
        assert s==p
        # Prompt lists only the ten acquired observations, never source targets for unseen settings.
        body=json.loads(read(ROOT/j['messages_path'])[1]['content'])
        assert body['observed_examples']==[{'settings':c['x'][i],'performance':y[0]} for i,y in zip(p['ids'],p['labels'])]
        assert set(body)=={'feature_order','numeric_bounds','categorical_values','encoding','observed_examples','direction','performance_meaning'}
        anchor=p['ids'][int(np.argmin([y[0] for y in p['labels']]))]
        for mode in MODES:
            s=copy.deepcopy(p);arm=read(O/'classical'/f"{j['key']}_{mode}.json")
            if mode=='random_proposal':
                rng=random.Random(148200+j['seed']);proposals=[[rng.choice(ds) for ds in c['grid_domains']] for _ in range(10)];chosen,diags=project(c,p,proposals);assert arm['projection']==diags
            for k,event in enumerate(grouped[j['key']+'_'+mode]):
                i=chosen[k] if mode=='random_proposal' else nextrow(c,s,mode,anchor);assert i==event['row_id'];s['ids'].append(i);s['labels'].append([event['value']])
            assert s==arm['state'] and len(set(s['ids']))==20 and arm['target']==min(y[0] for y in s['labels']);expected_states[j['key']+'_'+mode]=s
    development=read(ROOT/'artifacts/study_v147/inputs.json')['rows'];folds=read(ROOT/'results/v147_router/folds.json');trained=read(A/'routers.json')
    for m in MODELS:
        rs=[r for r in development if r['model']==m];t=trained[m];assert 'hadoop_mapreduce' not in t['training_groups'];a,s,coef,inter=ref_fit(rs,list(range(7)))
        for k,v in zip(['mean','scale','coef','intercept'],[a,s,coef,inter]):close(t['model'][k],v)
        scores={k:v for f in folds[m] for k,v in f['variants']['all']['outer_scores'].items()};ordered=[scores[r['key']] for r in rs]
        bt,bg,br=threshold(ordered,rs);assert t['calibration']['selected']['threshold']==bt
        ut,_,_=threshold([r['features'][-1] for r in rs],rs);assert t['uncertainty_calibration']['selected']['threshold']==ut
        close(t['benefit_80pct_threshold'],q(ordered,rs,.8));close(t['uncertainty_80pct_threshold'],q([r['features'][-1] for r in rs],rs,.8))
        decisions=[d for d in decision['rows'] if d['model']==m];assert len(decisions)==15;rng=random.Random(148001)
        for d in decisions:
            j=next(j for j in jobs if j['key']==d['key']);c=candidates[j['app']];f=prefix_features(read(ROOT/j['prefix']),c);close(f,d['features']);prediction=float((np.array(f)-a)/s@coef+inter);close(d['score'],prediction)
            assert d['benefit']==(bt is not None and d['score']>=bt);assert d['uncertainty']==(ut is not None and f[-1]>=ut)
            assert d['benefit_80pct']==(d['score']>=t['benefit_80pct_threshold']);assert d['uncertainty_80pct']==(f[-1]>=t['uncertainty_80pct_threshold']);assert d['random_development_rate']==(rng.random()<br)
        selected=set(random.Random(148002).sample(range(15),sum(d['benefit'] for d in decisions)))
        assert all(d['random_matched_rate']==(i in selected) for i,d in enumerate(decisions))
        base=ROOT/'results/v148_models'/m;starts=lines(base/'generation_starts.jsonl');responses=lines(base/'responses.jsonl');cost=b['ledgers'][m]
        assert cost['generation_requests']==len(starts)==len(responses)==15 and cost['retries']==0 and cost['allocated_output_tokens']==15360
        assert cost['peak_server_rss_bytes']<=8589934592 and cost['stage_seconds']<=700 and cost['server_exit_code']==0
        assert {r['identity'] for r in starts}=={j['key'] for j in jobs}=={r['key'] for r in responses}
        assert min(r['at_unix'] for r in starts)>read(O/'classical_summary.json')['at_unix']
        assert max(r['at_unix'] for r in starts)<b['seal']['at_unix']
        for j in jobs:
            c=candidates[j['app']];p=read(ROOT/j['prefix']);start=next(r for r in starts if r['identity']==j['key']);response=next(r for r in responses if r['key']==j['key'])['response'];preflight=read(base/'preflight'/f"{j['key']}.json");payload=start['payload']
            assert preflight['messages']==read(ROOT/j['messages_path']) and payload['prompt']==preflight['rendered']['prompt']
            assert payload['seed']==148000+j['seed'] and payload['n_predict']==1024 and payload['temperature']==.7 and payload['top_p']==.95 and payload['cache_prompt'] is False
            assert response['truncated'] is False and response['stop_type']=='eos' and 0<response['tokens_predicted']<=1024
            strings=json.loads(response['content']);assert len(strings)==10 and response['content']==json.dumps(strings,separators=(',',':'))
            assert all(len(x)==2 and x[0] in '0123456789' and x[1] in '012345678' for x in strings)
            proposals=[[int(x) for x in row] for row in strings];chosen,diags=project(c,p,proposals)
            key=m+'_'+j['key'];arm=read(O/'models'/f'{key}.json');assert not arm['fallback'] and arm['selected_rows']==chosen and arm['projection']==diags
            state=copy.deepcopy(p)
            for i,e in zip(chosen,grouped[key]):assert i==e['row_id'];state['ids'].append(i);state['labels'].append([e['value']])
            assert arm['state']==state and arm['target']==min(y[0] for y in state['labels']) and len(set(state['ids']))==20
            case=next(r for r in report['cases'] if r['model']==m and r['key']==j['key']);assert case['target']==arm['target']
            for mode in MODES:
                target=min(v[0] for v in expected_states[j['key']+'_'+mode]['labels']);assert case['references'][mode]==target
                close(case['gains'][mode],float((Fraction(str(target))-Fraction(str(arm['target'])))/Fraction(str(target))))
            d=next(d for d in decisions if d['key']==j['key'])
            assert case['policies']=={'never':False,'always':True,**{k:d[k] for k in ['benefit','uncertainty','random_development_rate','random_matched_rate','benefit_80pct','uncertainty_80pct']}}
        rs=[r for r in report['cases'] if r['model']==m];summary=report['models'][m]
        for mode in MODES:
            gs=[r['gains'][mode] for r in rs];v=summary['contrasts'][mode];close(v['mean_gain'],np.mean(gs));assert [v[x] for x in ['n','wins','ties','losses','practical_wins','practical_harms']]==[15,sum(x>0 for x in gs),sum(x==0 for x in gs),sum(x<0 for x in gs),sum(x>.01 for x in gs),sum(x<-.01 for x in gs)]
        for policy,st in summary['policies'].items():
            chosen=[r for r in rs if r['policies'][policy]];assert st['calls']==len(chosen);close(st['mean_gain'],sum(r['gains']['sequential_3nn'] for r in chosen)/15)
            assert st['harmful_calls']==sum(r['gains']['sequential_3nn']<-.01 for r in chosen)
        c=summary['cost'];assert c['request_starts']==15 and c['responses']==15 and c['unknown_usage_requests']==0
        assert c['generated_tokens_lower_bound']==sum(r['response']['tokens_predicted'] for r in responses);assert c['prefill_tokens_lower_bound']==sum(r['response']['tokens_evaluated'] for r in responses)
    assert report['acquisition_status_counts']==dict(Counter(e['status'] for e in events));assert report['unique_source_records_acquired']==len({e['source'] for e in events})
    assert report['collection']['total_acquisitions']==1200 and report['collection']['total_collection_seconds']<1800
    return {'verified':True,'charged_outcomes':1200,'source_records':len({e['source'] for e in events}),'prefixes':15,'B20_arms':105,'real_requests':30,'independent_router_fit':'augmented least squares','all_model_server_exits':0}

def main():
    for file in [ROOT/'reports/protocol_v148.freeze.json',A/'inputs.freeze.json']:
        for n,h in read(file)['sha256'].items():assert sha(ROOT/n)==h,n
    b=bundle();result=verify(b);mutations=[]
    for name in ['raw_outcome','reported_gain','request_undercount','late_selection']:
        changed=copy.deepcopy(b)
        if name=='raw_outcome':changed['events'][0]['value']+=1
        elif name=='reported_gain':changed['report']['models']['smollm3_3b']['contrasts']['sequential_3nn']['mean_gain']+=.1
        elif name=='request_undercount':changed['ledgers']['qwen3_8b']['generation_requests']-=1
        else:changed['seal']['at_unix']=max(e['at_unix'] for e in b['events'])+1
        try:verify(changed)
        except AssertionError:mutations.append({'name':name,'rejected':True})
        else:raise AssertionError('Mutation survived: '+name)
    result['semantic_mutations']=mutations;(A/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
