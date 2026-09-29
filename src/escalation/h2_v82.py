"""Outcome-blind H2 domain and independent exact SQL-result oracle."""
import itertools,csv
COLS=['GRP','ACCT','SCORE','GRP,SCORE','ACCT,GRP','TICK']
def grid():return [{'mask':m,'recompile':r,'analyze_sample':a} for m in range(64) if bin(m).count('1')<=3 for r,a in itertools.product([False,True],[0,100,2000,10000])]
PROFILES={'reference':{'mask':0,'recompile':False,'analyze_sample':10000},'prior':{'mask':56,'recompile':False,'analyze_sample':10000},'contrast':{'mask':56,'recompile':True,'analyze_sample':100}}
ORDER=['reference','prior','contrast','prior','contrast','reference','contrast','reference','prior']
def expected(n=100000):
    result={}
    for q in range(3):
        for t in range(16):
            count=total=0
            for i in range(n):
                g=i*37%97;acct=i*29%997;score=i*13%10000
                match=(g==t*7%97 and t*431%9000<=score<=t*431%9000+500) if q==0 else (acct==t*43%997 and g==t*11%97) if q==1 else (t*5701%90000<=i<t*5701%90000+1000)
                if match:count+=1;total+=i*7919%100000
            result[q,t]=(count,total)
    return result

def validate(folder,config,truth):
    import json
    metrics=json.loads((folder/'metrics.json').read_text())
    assert metrics['version']=='2.3.232' and metrics['rows']==100000 and metrics['scored_queries']==192 and metrics['warmup_queries']==48
    assert all(metrics[k]==v for k,v in config.items())
    settings=dict(line.split('=',1) for line in (folder/'settings.txt').read_text().splitlines())
    assert settings['RECOMPILE_ALWAYS'].lower()==str(config['recompile']).lower()
    assert settings['QUERY_CACHE_SIZE']=='8' and settings['ANALYZE_AUTO']=='0' and settings['OPTIMIZE_REUSE_RESULTS_ENGINE'].lower() in ['false','0']
    indexes={}
    for name,col,ordinal in csv.reader((folder/'indexes.csv').read_text().splitlines()):
        if name.startswith('IDX'):indexes.setdefault(name,[]).append((int(ordinal),col))
    assert indexes=={'IDX'+str(i):list(enumerate(COLS[i].split(','),1)) for i in range(6) if config['mask']&(1<<i)}
    rows=list(csv.DictReader((folder/'answers.csv').open()));assert len(rows)==192
    seen=set()
    for r in rows:
        key=tuple(int(r[k]) for k in ['round','query','parameter']);assert key not in seen and key in set(itertools.product(range(4),range(3),range(16)));seen.add(key)
        assert (int(r['count']),int(r['sum']))==truth[key[1],key[2]]
    return metrics
