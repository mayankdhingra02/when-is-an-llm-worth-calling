"""Standard-library reconstruction of H2 V84 saved outcomes, not fresh measurement.

Run from extracted bundle with python3 -I -S scripts/replay_h2_v84_portable.py.
The full original analyzer separately replays RF decisions with pinned sklearn.
"""
import csv,hashlib,itertools,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
    manifest=read(ROOT/'manifest.json')
    for n,m in manifest['files'].items():
        p=ROOT/n;assert p.is_file() and p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],n
    raw=ROOT/'results/v84_h2_classical';rows=read(raw/'acquisitions.json');cases=read(raw/'cases.json');summary=read(raw/'summary.json');analysis=read(ROOT/'results/v84_h2_analysis/summary.json')
    assert summary['complete'] and summary['intended_trials']==summary['charged_trials']==summary['valid_trials']==len(rows)==165
    assert len(analysis['cases'])==5
    assert summary['completed_seeds']==len(cases)==5 and summary['new_model_requests']==summary['unattempted']==0 and summary['seconds']<1800
    configs=[dict(mask=m,recompile=r,analyze_sample=a) for m in range(64) if bin(m).count('1')<=3 for r,a in itertools.product([False,True],[0,100,2000,10000])]
    prior=configs.index(dict(mask=56,recompile=False,analyze_sample=10000));truth={}
    for q,t in itertools.product(range(3),range(16)):
        count=total=0
        for i in range(100000):
            grp=i*37%97;acct=i*29%997;score=i*13%10000
            yes=(grp==t*7%97 and t*431%9000<=score<=t*431%9000+500) if q==0 else (acct==t*43%997 and grp==t*11%97) if q==1 else (t*5701%90000<=i<t*5701%90000+1000)
            if yes:count+=1;total+=i*7919%100000
        truth[q,t]=count,total
    allowed=set(itertools.product(range(128),range(3),range(16)));cols=['GRP','ACCT','SCORE','GRP,SCORE','ACCT,GRP','TICK']
    for i,r in enumerate(rows):
        p=raw/f'trial_{i:03d}';assert r['trial']==i and r['status']=='valid' and r['config']==configs[r['config_id']]
        assert r==read(p/'result.json') and r['process']==read(p/'process_receipt.json') and r['metrics']==read(p/'metrics.json')
        m=r['metrics'];assert m['version']=='2.3.232' and m['rows']==100000 and m['scored_queries']==6144 and m['warmup_queries']==1536
        assert all(m[k]==v for k,v in r['config'].items()) and math.isfinite(m['query_seconds']) and m['query_seconds']>0
        receipt=r['process'];assert receipt['exit_code']==0 and receipt['termination_reason'] is None and receipt['wall_seconds']<60
        assert receipt['sampled_maxima']['rss_bytes']<2*1024**3 and receipt['sampled_maxima']['scratch_bytes']<128*1024**2
        s=dict(line.split('=',1) for line in (p/'settings.txt').read_text().splitlines());assert s['OPTIMIZE_REUSE_RESULTS_ENGINE']=='false' and s['RECOMPILE_ALWAYS']==str(r['config']['recompile']).lower() and s['ANALYZE_AUTO']=='0' and s['QUERY_CACHE_SIZE']=='8'
        indexes={}
        for name,col,ordinal in csv.reader((p/'indexes.csv').read_text().splitlines()):
            if name.startswith('IDX'):indexes.setdefault(name,[]).append((int(ordinal),col))
        assert indexes=={'IDX'+str(k):list(enumerate(cols[k].split(','),1)) for k in range(6) if r['config']['mask']&(1<<k)}
        seen=set()
        with (p/'answers.csv').open() as f:
            for answer in csv.DictReader(f):
                key=tuple(int(answer[k]) for k in ['round','query','parameter']);assert key in allowed and key not in seen;seen.add(key)
                assert (int(answer['count']),int(answer['sum']))==truth[key[1],key[2]]
        assert seen==allowed and sha(p/'answers.csv')==r['answers_sha256']
    for case,reported,seed in zip(cases,analysis['cases'],[11,23,37,53,71]):
        assert case['seed']==reported['seed']==seed and case['complete'];prefix=case['prefix'];assert len(prefix)==10 and prefix[0]['config_id']==prior
        pp=raw/f'prefix_{seed}.json';assert read(pp)['observations']==prefix and sha(pp)==case['prefix_sha256']
        for arm in ['rf_lcb','random','prior']:
            obs=case['branches'][arm];a=reported['arms'][arm];assert len(obs)==a['logical_evaluations']==(3 if arm=='prior' else 20)
            assert len({o['physical_trial'] for o in obs})==len(obs)
            if arm!='prior':assert obs[:10]==prefix and len({o['config_id'] for o in obs[:17]})==17
            else:assert all(o['config_id']==prior for o in obs)
            for o in obs:
                r=rows[o['physical_trial']];assert r['seed']==seed and r['config_id']==o['config_id'] and r['metrics']['query_seconds']==o['query_seconds']
            selected=prior if arm=='prior' else min(obs[:17],key=lambda o:(o['query_seconds'],o['config_id']))['config_id']
            assert selected==case['selected'][arm]==a['selected_config_id'] and all(o['config_id']==selected for o in obs[-3:])
            times=[o['query_seconds'] for o in obs[-3:]];assert times==a['confirmation_seconds'] and statistics.median(times)==a['median_seconds']
            spread=(max(times)-min(times))/statistics.median(times);assert spread==a['range_over_median'] and a['precision_pass']==(a['median_seconds']>=.1 and spread<=.2)
        for arm in ['rf_lcb','random']:
            a=reported['arms'][arm];gain=1-a['median_seconds']/reported['arms']['prior']['median_seconds'];assert gain==a['gain_vs_prior'] and (gain>=.1)==a['material_gain_flag']
    assert analysis['physical_trials']==165 and analysis['logical_rf_random_trials']==200 and analysis['logical_prior_trials']==15 and analysis['checked_scored_answers']==165*6144 and analysis['model_calls']==0
    print(json.dumps({'verified':True,'physical_trials':165,'exact_scored_answers':165*6144,'scope':'saved outcome reconstruction; no RF replay or fresh native execution'}))
if __name__=='__main__':check()
