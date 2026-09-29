"""Feature-only cloud-configuration optimizer with a charged, isolated recorded oracle."""
import json, math, random, time
from pathlib import Path
from collect_smollm_v47 import ROOT, read, write, sha, now, append
from router_v132 import features
import router_v147 as router
A=ROOT/'artifacts/study_v148';O=ROOT/'results/v148_hadoop'
SOURCE=ROOT/'artifacts/sources/v146/scout'
APPS=['pagerank','terasort','wordcount'];SEEDS=[11,23,37,53,71]
CONTROLS=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal']

def score_record(record,app):
    if (record.get('framework'),record.get('workload'),record.get('datasize'))!=('hadoop',app,'bigdata'):
        raise ValueError('Recorded context mismatch')
    if type(record.get('completed')) is not bool:raise ValueError('Missing/invalid completion status')
    if not record['completed']:return 7200.,'incomplete_failure_penalty'
    t=float(record['elapsed_time'])
    if not math.isfinite(t) or t<=0:raise ValueError('Invalid completed duration')
    return min(t,7200.),'completed_capped' if t>7200 else 'completed'

def candidate(app,tree,receipts):
    dirs=sorted(e['path'] for e in tree if e['path'].endswith(app+'_hadoop_bigdata_1'))
    xs=[[int(n.split('_')[0]),n.split('_')[1]] for n in dirs]
    assert len(xs)==len({tuple(x) for x in xs})==69
    domains=[sorted({x[j] for x in xs}) for j in range(2)]
    normalized=[[(x[0]-domains[0][0])/(domains[0][-1]-domains[0][0]),domains[1].index(x[1])] for x in xs]
    # Numeric outcomes are never parsed here. Receipt hashes authenticate every hidden report.
    sources=[str((SOURCE/'selected'/n/'report.json').relative_to(ROOT)) for n in dirs]
    assert all(n in receipts and sha(ROOT/n)==receipts[n] for n in sources)
    return {'app':app,'system_group':'hadoop_mapreduce','names':['cluster_vm_count','vm_type'],'raw_features':xs,'x':normalized,'domains':domains,'grid_domains':[list(range(10)),list(range(9))],'sources':sources,'source_hashes':[receipts[n] for n in sources]}

def distance(a,b):return (abs(a[0]-b[0])+float(a[1]!=b[1]))/2

def choose(c,s,mode,anchor=None):
    if len(s['ids'])!=len(s['labels']) or len(set(s['ids']))!=len(s['ids']) or not 0<=len(s['ids'])<20:raise ValueError('Invalid state or budget')
    available=[i for i in s['order'] if i not in s['ids']]
    if len(s['ids'])<4 or mode=='random_full':return available[0]
    if mode in ['adaptive_neighbor','fixed_neighbor']:
        best=anchor if mode=='fixed_neighbor' else s['ids'][min(range(len(s['ids'])),key=lambda k:s['labels'][k][0])]
        return min(available,key=lambda i:distance(c['x'][i],c['x'][best]))
    if mode!='sequential_3nn':raise ValueError('Unknown mode')
    def estimate(i):
        nearest=sorted(range(len(s['ids'])),key=lambda k:(distance(c['x'][i],c['x'][s['ids'][k]]),k))[:3]
        return sum(s['labels'][k][0] for k in nearest)/len(nearest)
    return min(available,key=estimate)

def project(c,s,proposals):
    if len(proposals)!=10:raise ValueError('Ten proposals required')
    seen=set(s['ids']);selected=[];prior=[];diag=[]
    for p in proposals:
        if len(p)!=2 or any(type(v)!=int or v not in d for v,d in zip(p,c['grid_domains'])):raise ValueError('Invalid proposal')
        x=[p[0]/9,p[1]];i=min((i for i in s['order'] if i not in seen),key=lambda i:distance(c['x'][i],x));seen.add(i);selected.append(i)
        diag.append({'row_id':i,'distance':distance(x,c['x'][i]),'repeated_proposal':p in prior,'matches_prefix':any(distance(x,c['x'][k])==0 for k in s['ids'])});prior.append(list(p))
    return selected,diag

def messages(c,s):
    return [{'role':'system','content':'Optimize a cloud deployment configuration from ten acquired measurements. Propose ten diverse promising settings. Output only a JSON array of ten two-digit strings in feature_order. First digit specifies equally spaced positions between numeric minimum and maximum; second digit selects a categorical value. Proposals project to unobserved recorded configurations. Infer settings from performance and avoid duplicate proposals.'},
            {'role':'user','content':json.dumps({'feature_order':c['names'],'numeric_bounds':{'0':[c['domains'][0][0],c['domains'][0][-1]]},'categorical_values':{'1':c['domains'][1]},'encoding':'Observations have VM counts normalized to [0,1] and VM type indices. Proposal first digit0..9 means digit/9; second digit0..8 indexes vm_type. Projection uses mean numeric absolute distance and categorical mismatch.',
             'observed_examples':[{'settings':c['x'][i],'performance':y[0]} for i,y in zip(s['ids'],s['labels'])],
             'direction':'minimize','performance_meaning':'Capped completion-time score: completed elapsed seconds capped at7200; incomplete source runs receive failure penalty7200 (not observed runtime). Fixed Hadoop workload and bigdata input. Optimize this score; cloud-dollar costs are not estimated.'},separators=(',',':'))}]

class Oracle:
    def __init__(self,c,key,prefix=None):self.c=c;self.key=key;self.seen=set(prefix['ids'] if prefix else [])
    def acquire(self,i):
        if type(i)!=int or not 0<=i<len(self.c['x']) or i in self.seen or len(self.seen)>=20:raise ValueError('Duplicate/over-budget acquisition')
        ledger=read(O/'ledger.json');cfg=read(ROOT/'configs/study_v148.json')
        if ledger['acquisitions']>=cfg['total_new_recorded_acquisitions']:raise PermissionError('Global acquisition cap')
        if time.time()-ledger['collection_started_unix']>=cfg['total_collection_seconds_cap']:raise TimeoutError('Collection time cap')
        ledger['acquisitions']+=1;write(O/'ledger.json',ledger);self.seen.add(i)
        n=self.c['sources'][i];event={'at_unix':time.time(),'key':self.key,'row_id':i,'source':n,'source_sha256':self.c['source_hashes'][i]}
        try:
            if sha(ROOT/n)!=event['source_sha256']:raise ValueError('Changed source')
            r=read(ROOT/n);event['raw_record']=r;value,status=score_record(r,self.c['app']);event.update(value=value,status=status)
        except Exception as e:event.update(value=None,status='invalid_source',error=repr(e));append(O/'acquisitions.jsonl',event);raise
        append(O/'acquisitions.jsonl',event);return [value]

def check_freeze():
    for n,h in read(ROOT/'reports/protocol_v148.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def prepare():
    assert not (ROOT/'reports/protocol_v148.freeze.json').exists()
    receipt=read(ROOT/'artifacts/sources/v146/scout_records_receipt.json');assert receipt['error'] is None and len(receipt['files'])==207
    tree=read(SOURCE/'multi_tree.json')['tree'];receipts={f['path']:f['sha256'] for f in receipt['files']}
    for app in APPS:write(A/'candidates'/f'{app}.json',candidate(app,tree,receipts))
    write(A/'models.json',read(ROOT/'artifacts/study_v144/models.json'))
    development=read(ROOT/'artifacts/study_v147/inputs.json')['rows'];folds=read(ROOT/'results/v147_router/folds.json');trained={}
    for m in ['smollm3_3b','qwen3_8b']:
        rows=[r for r in development if r['model']==m];scores={k:v for f in folds[m] for k,v in f['variants']['all']['outer_scores'].items()};ordered=[scores[r['key']] for r in rows]
        trained[m]={'model':router.fit(rows,list(range(7))), 'calibration':router.select(ordered,rows),'benefit_80pct_threshold':router.quantile(ordered,rows,.8),
                    'uncertainty_calibration':router.select([r['features'][-1] for r in rows],rows),'uncertainty_80pct_threshold':router.quantile([r['features'][-1] for r in rows],rows,.8),
                    'training_keys':[r['key'] for r in rows],'training_groups':sorted({r['group'] for r in rows})}
        assert 'hadoop_mapreduce' not in trained[m]['training_groups']
    write(A/'routers.json',trained);print('Prepared207 feature-only configurations and two development-only routers; no Hadoop targets acquired')

def prefixes():
    check_freeze();O.mkdir(exist_ok=False);write(O/'ledger.json',{'at':now(),'collection_started_unix':time.time(),'acquisitions':0});(O/'acquisitions.jsonl').touch();jobs=[];decisions=[];trained=read(A/'routers.json');started=time.monotonic()
    rng={m:random.Random(148001) for m in trained}
    for app in APPS:
        c=read(A/'candidates'/f'{app}.json')
        for seed in SEEDS:
            key=f'{app}_{seed}';order=list(range(69));random.Random(seed).shuffle(order);s={'ids':[],'labels':[],'order':order};o=Oracle(c,key+'_prefix')
            for _ in range(10):
                i=choose(c,s,'sequential_3nn');value=o.acquire(i);s['ids'].append(i);s['labels'].append(value)
            p=A/'prefixes'/f'{key}.json';write(p,s);mp=A/'prompts'/f'{key}.json';write(mp,messages(c,s));f=features(s,c['domains'],'minimize')
            for model,t in trained.items():
                score=router.predict(t['model'],{'features':f});threshold=t['calibration']['selected']['threshold'];u=t['uncertainty_calibration']['selected']['threshold']
                decisions.append({'key':key,'model':model,'features':f,'score':score,'benefit':threshold is not None and score>=threshold,'uncertainty':u is not None and f[-1]>=u,
                                  'benefit_80pct':score>=t['benefit_80pct_threshold'],'uncertainty_80pct':f[-1]>=t['uncertainty_80pct_threshold'],
                                  'random_development_rate':rng[model].random()<t['calibration']['selected']['rate'],
                                  'outside_training_range':[router.FEATURES[i] for i,x in enumerate(f) if x<t['model']['min'][i] or x>t['model']['max'][i]]})
            jobs.append({'key':key,'app':app,'system_group':'hadoop_mapreduce','seed':seed,'domains':c['grid_domains'],'sampling_seed':148000+seed,'prefix':str(p.relative_to(ROOT)),'prefix_sha256':sha(p),'messages_path':str(mp.relative_to(ROOT))})
    for model in trained:
        sub=[d for d in decisions if d['model']==model];selected=set(random.Random(148002).sample(range(15),sum(d['benefit'] for d in sub)))
        for i,d in enumerate(sub):d['random_matched_rate']=i in selected
    write(A/'decisions.json',{'at_unix':time.time(),'rows':decisions,'prefix_and_controller_seconds':time.monotonic()-started});random.Random(148100).shuffle(jobs);write(A/'jobs.json',jobs)
    paths=[p for folder in ['prefixes','prompts','candidates'] for p in (A/folder).glob('*.json')]+[A/'jobs.json',A/'decisions.json',A/'routers.json',A/'models.json']
    write(A/'inputs.freeze.json',{'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}});print('15 B10prefixes saved;150charged outcomes; decisions frozen before continuation')

def classical():
    check_freeze();dest=O/'classical';dest.mkdir(exist_ok=False);start=time.monotonic()
    for job in read(A/'jobs.json'):
        c=read(A/'candidates'/f"{job['app']}.json");p=read(ROOT/job['prefix']);anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])]
        for mode in CONTROLS:
            s=json.loads(json.dumps(p));key=job['key']+'_'+mode;o=Oracle(c,key,p);diag=[]
            if mode=='random_proposal':
                rng=random.Random(148200+job['seed']);proposals=[[rng.choice(d) for d in c['grid_domains']] for _ in range(10)];ids,diag=project(c,p,proposals)
            for step in range(10):
                i=ids[step] if mode=='random_proposal' else choose(c,s,mode,anchor);value=o.acquire(i);s['ids'].append(i);s['labels'].append(value)
            write(dest/(key+'.json'),{'key':key,'case':job['key'],'mode':mode,'state':s,'target':min(y[0] for y in s['labels']),'projection':diag})
    assert read(O/'ledger.json')['acquisitions']==900
    write(O/'classical_summary.json',{'complete':True,'at_unix':time.time(),'arms':75,'new_acquisitions':750,'seconds':time.monotonic()-start});classical_gate();print('75 complete B20classical arms;900 cumulative charges')

def classical_gate():
    summary=read(O/'classical_summary.json');assert summary['complete'] is True and summary['arms']==75
    assert read(O/'ledger.json')['acquisitions']==900
    events=[json.loads(s) for s in (O/'acquisitions.jsonl').read_text().splitlines()]
    assert len(events)==900 and all(e['value'] is not None for e in events)
    jobs=read(A/'jobs.json');assert len(jobs)==15
    for j in jobs:
        p=read(ROOT/j['prefix'])
        for mode in CONTROLS:
            d=read(O/'classical'/f"{j['key']}_{mode}.json");s=d['state']
            assert len(s['ids'])==len(set(s['ids']))==len(s['labels'])==20
            assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels']
    return True

def evaluate():
    check_freeze();classical_gate();dest=O/'models';dest.mkdir(exist_ok=False);choices=[]
    for model in read(ROOT/'configs/study_v148.json')['model_order']:
        for j in read(A/'jobs.json'):
            c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);sp=ROOT/'results/v148_models'/model/'scores'/f"{j['key']}.json";score=read(sp) if sp.exists() else {'status':'unattempted'}
            ids,diag=project(c,p,score['score']) if score['status']=='valid' else ([],[])
            choices.append({**j,'model':model,'status':score['status'],'selected_rows':ids,'projection':diag})
    write(O/'choices.json',choices);write(O/'selection_seal.json',{'at_unix':time.time(),'choices_sha256':sha(O/'choices.json')})
    for j in choices:
        c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);s=json.loads(json.dumps(p));key=j['model']+'_'+j['key'];o=Oracle(c,key,p)
        for step in range(10):
            i=j['selected_rows'][step] if j['status']=='valid' else choose(c,s,'sequential_3nn');value=o.acquire(i);s['ids'].append(i);s['labels'].append(value)
        write(dest/(key+'.json'),{**j,'key':key,'case':j['key'],'state':s,'target':min(y[0] for y in s['labels']),'fallback':j['status']!='valid'})
    assert read(O/'ledger.json')['acquisitions']==1200
    write(O/'completion.json',{'at_unix':time.time(),'model_arms':30,'total_acquisitions':1200,'total_collection_seconds':time.time()-read(O/'ledger.json')['collection_started_unix']});print('30 model/fallback continuations;1200 total charges')
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','prefixes','classical','evaluate']);args=ap.parse_args();globals()[args.stage]()
