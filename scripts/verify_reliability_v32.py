"""Independent selection/Decimal checks and fresh decode of every saved payload."""
import argparse,csv,hashlib,json,os,subprocess,sys,time,zlib
from decimal import Decimal,getcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT);getcontext().prec=40
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config
from escalation.io import write
def read(p):return json.loads(Path(p).read_text(),parse_float=Decimal)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def avg(xs):return sum(xs,Decimal(0))/len(xs)
def median(xs):
    values=sorted(Decimal(v) for v in xs);n=len(values)
    return values[n//2] if n%2 else (values[n//2-1]+values[n//2])/2
def close(a,b):
    if abs(a-b)>Decimal('1e-12'):raise ValueError(f'{a} != {b}')

def verify():
    start=time.perf_counter();m=read('data/reliability_v32.json');r=read('results/v32_reliability/summary.json')
    env=read('artifacts/study_v15/environment.json');workload=read('artifacts/study_v15/workload_manifest.json')
    for p,h in env['sha256'].items():assert sha(p)==h
    payload=Path(workload['workload_path']).read_bytes();assert hashlib.sha256(payload).hexdigest()==workload['workload_sha256']
    with Path('results/v17_measurements/configuration_summary.csv').open(newline='') as f:
        source={(s['family'],s['config_id']):(Decimal(s['median_compression_ms']),Decimal(s['compressed_bytes'])) for s in csv.DictReader(f)}
    datasets=read('data/live_manifest_v17.json')['datasets'];selected=set()
    for case in m['cases']:
        d=next(d for d in datasets if d['system_group']==case['family']);roles=case['roles'];cap=case['size_cap_bytes']
        for mode in ('joint_3nn','random'):
            a=read(f"results/v17_classical/{mode}/{case['family']}_{case['seed']}.json")
            assert a['labels']==[list(source[case['family'],d['configurations'][i]['config_id']]) for i in a['ids']]
            best=min((y[0],i) for i,y in zip(a['ids'],a['labels']) if y[1]<=cap)
            assert roles[mode]==d['configurations'][best[1]]['config_id']
        hindsight=min((y[0],cid) for (family,cid),y in source.items() if family==case['family'] and y[1]<=cap)
        assert roles['historical_hindsight']==hindsight[1]
        selected.update(roles.values())
    assert selected=={s['setting']['config_id'] for s in m['selected']}
    trials=[json.loads(line) for line in Path('results/v32_reliability/trials.jsonl').read_text().splitlines()]
    assert len(trials)==m['intended_trials'] and all(t['status']=='ok' for t in trials)
    times={cid:{} for cid in selected};decode_records=[]
    for t in trials:
        b=Path(t['compressed_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==t['compressed_sha256'] and len(b)==t['compressed_bytes']
        family=t['setting']['family']
        if family=='zlib':decoded=zlib.decompress(b)
        else:
            p=subprocess.run([env['binary_paths'][family],'-q','-d','-c'],input=b,capture_output=True,timeout=2,check=True)
            decoded=p.stdout
        assert decoded==payload
        cid=t['setting']['config_id'];rep=t['repetition'];assert rep not in times[cid]
        times[cid][rep]=t['compression_ns'];decode_records.append({'trial_id':t['trial_id'],'compressed_sha256':t['compressed_sha256'],'decoded_equal':True})
    assert all(set(v)==set(range(20)) for v in times.values())
    computed=[]
    for c in r['cases']:
        values={k:[times[c[k]][i] for i in range(20)] for k in ('cheap_config_id','random_config_id','historical_hindsight_config_id')}
        cheap=values['cheap_config_id'];random=values['random_config_id'];historical=values['historical_hindsight_config_id']
        close(median(cheap)/Decimal(1000000),c['fresh_cheap_median_ms']);close(median(random)/Decimal(1000000),c['fresh_random_median_ms'])
        for prefix,candidate,reference in [('',cheap,random),('historical_reference_',historical,cheap)]:
            gain=(median(reference)-median(candidate))/median(reference);close(gain,c[prefix+'relative_gain_of_medians'])
            paired=sorted((Decimal(b)-Decimal(a))/Decimal(b) for a,b in zip(candidate,reference))
            close(median(paired),c[prefix+'median_paired_relative_gain'])
            for key,q in [('paired_p10',Decimal('.1')),('paired_p90',Decimal('.9'))]:
                position=Decimal(19)*q;i=int(position);value=paired[i]+(position-i)*(paired[i+1]-paired[i]);close(value,c[prefix+key])
            assert c[prefix+'rounds_faster']==sum(v>0 for v in paired)
            assert c[prefix+'rounds_equal']==sum(v==0 for v in paired)
            assert c[prefix+'rounds_slower']==sum(v<0 for v in paired)
        computed.append({'family':c['family'],'gain':(median(random)-median(cheap))/median(random),
            'historical_gain':(median(cheap)-median(historical))/median(cheap)})
    for g in r['groups']:
        close(avg([c['gain'] for c in computed if c['family']==g['family']]),g['fresh_mean_cheap_gain'])
        close(avg([c['historical_gain'] for c in computed if c['family']==g['family']]),g['fresh_mean_historical_reference_gain'])
    close(avg([g['fresh_mean_cheap_gain'] for g in r['groups']]),r['equal_family_fresh_gain'])
    return {'verified':True,'historical_case_selections_checked':15,'unique_configurations_checked':len(selected),
        'saved_payloads_independently_decoded':len(decode_records),'case_comparisons_checked':30,
        'decimal_statistic_checks':120,'paired_round_count_checks':90,'verification_seconds':time.perf_counter()-start,
        'decode_records':decode_records,'new_compressions':0,'new_optimizer_acquisitions':0,'new_model_calls':0,
        'scope':'Decoding retained bytes checks correctness, not a new objective measurement; verification computation separately charged'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        receipt=verify();print(json.dumps({k:v for k,v in receipt.items() if k!='decode_records'},indent=2));return
    output=Path('artifacts/study_v32/independent_verification.json')
    if output.exists():raise RuntimeError('Preserve completed verification; use --verify-only')
    before=json.loads(Path('artifacts/resource_ledger_v2.json').read_text())
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),json.loads(Path('configs/authorization_v22.json').read_text()))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check();receipt=verify();write(output,receipt);resource.check()
    after=json.loads(Path('artifacts/resource_ledger_v2.json').read_text())
    write('artifacts/study_v32/verification_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_physical_trials':0,'new_optimizer_acquisitions':0,'new_model_calls':0,'active_since':after['active_since']})
    print(json.dumps({k:v for k,v in receipt.items() if k!='decode_records'},indent=2))

if __name__=='__main__':main()
