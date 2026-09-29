"""Select all historical V17 case roles before fresh physical measurements."""
import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines,now
from escalation.reliability_v32 import schedule

def main():
    out=Path('data/reliability_v32.json')
    if out.exists():raise RuntimeError('Preserve prepared manifest')
    datasets=read('data/live_manifest_v17.json')['datasets'];old=read('results/v17_classical/summary.json')
    physical=read('results/v17_measurements/summary.json')['settings'];trials=lines('results/v17_measurements/trials.jsonl')
    cases=[];selected={}
    sources=['data/live_manifest_v17.json','results/v17_classical/summary.json','results/v17_measurements/summary.json',
        'results/v17_measurements/trials.jsonl','artifacts/study_v15/environment.json','artifacts/study_v15/workload_manifest.json']
    for c in old['cases']:
        d=next(d for d in datasets if d['system_group']==c['family']);roles={}
        for mode in ('joint_3nn','random'):
            path=f"results/v17_classical/{mode}/{c['family']}_{c['seed']}.json";sources.append(path);arm=read(path)
            assert arm['best_feasible_ms']==c['cheap_ms' if mode=='joint_3nn' else 'random_ms']
            roles[mode]=d['configurations'][arm['best_row']]['config_id']
        allowed=[s for s in physical if s['family']==c['family'] and s['compressed_bytes']<=c['size_cap_bytes']]
        best=min(allowed,key=lambda s:(s['median_compression_ms'],s['config_id']))
        assert best['median_compression_ms']==c['hindsight_fulltable_ms']
        roles['historical_hindsight']=best['config_id']
        for role,config_id in roles.items():
            s=next(s for s in physical if s['config_id']==config_id)
            rows=[r for r in trials if r['setting']['config_id']==config_id]
            assert len(rows)==3 and all(r['status']=='ok' for r in rows)
            digests={r['compressed_sha256'] for r in rows};assert len(digests)==1
            selected[config_id]={'setting':s['setting'],'expected_compressed_bytes':s['compressed_bytes'],
                'expected_compressed_sha256':next(iter(digests)),'historical_median_ms':s['median_compression_ms']}
        cases.append({**c,'roles':roles})
    config={'scope':'Exploratory fresh remeasurement of fixed historical selections; no new optimizer or LLM arms',
        'created_at':now(),'cases':cases,'selected':list(sorted(selected.values(),key=lambda s:s['setting']['config_id'])),
        'repetitions':20,'schedule_seed':2026092532,'trial_timeout_seconds':2,'stage_wall_seconds':60,
        'intended_trials':20*len(selected),'allow_model_calls':False,
        'source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sorted(set(sources))}}
    assert len(cases)==15 and len(selected)<=45
    write(out,config);write('artifacts/study_v32/schedule.json',schedule([s['setting'] for s in config['selected']]))
    print(json.dumps({'cases':len(cases),'unique_settings':len(selected),'intended_physical_trials':config['intended_trials']},indent=2))

if __name__=='__main__':main()
