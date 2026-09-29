"""Independent recorded-state replay and post-decision descriptive evaluation."""
import csv,hashlib,json,math,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.offline_live_v17 import FEATURES,REFERENCES
from escalation.resources import Resources


def read(p):return json.loads((ROOT/p).read_text())
def close(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
def manual_choice(xs,order,ids,labels,cap,method):
    available=[i for i in order if i not in ids]
    if method=='random':return available[0]
    estimates=[]
    for position,index in enumerate(available):
        nearest=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[index],xs[ids[j]])),j))[:3]
        predicted=[sum(labels[j][k] for j in nearest)/3 for k in (0,1)]
        estimates.append((index,position,*predicted))
    feasible=[r for r in estimates if r[3]<=cap]
    if feasible:return min(feasible,key=lambda r:(r[2],r[1]))[0]
    return min(estimates,key=lambda r:(r[3],r[2],r[1]))[0]


def main():
    out=ROOT/'results/v17_classical'
    if (out/'summary.json').exists():raise RuntimeError('Completed analysis retained')
    before=read('artifacts/resource_ledger_v2.json')
    if before.get('active_since') or 1800-before['experiment_seconds']<5:raise RuntimeError('Analysis allowance unavailable')
    config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    records=[];expected_journal=[]
    with Resources(config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for name,h in read('reports/protocol_v17_expansion.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
        assert hashlib.sha256((ROOT/'results/v17_measurements/configuration_summary.csv').read_bytes()).hexdigest()==read('artifacts/study_v17/recorded_table_binding.json')['sha256']
        with (ROOT/'results/v17_measurements/configuration_summary.csv').open(newline='') as f:source={(r['family'],r['config_id']):[float(r['median_compression_ms']),float(r['compressed_bytes'])] for r in csv.DictReader(f)}
        for dataset in read('data/live_manifest_v17.json')['datasets']:
            family=dataset['system_group'];settings=dataset['configurations'];names=FEATURES[family]
            xs=[tuple(float(r[n]) for n in names) for r in settings]
            labels={i:source[family,s['config_id']] for i,s in enumerate(settings)}
            reference=next(i for i,s in enumerate(settings) if all(s[k]==v for k,v in REFERENCES[family].items()))
            for seed in [11,23,37,53,71]:
                key=f'{family}_{seed}';prefix=read(f'results/v17_classical/prefixes/{key}.json')
                order=list(range(len(settings)));random.Random(seed).shuffle(order)
                initial=[reference]+[i for i in order if i!=reference][:3]
                assert prefix['order']==order and prefix['ids'][:4]==initial
                cap=labels[reference][1];assert prefix['size_cap']==cap
                seen=initial[:];acquired=[labels[i] for i in seen]
                for step in prefix['prefix_steps']:
                    chosen=manual_choice(xs,order,seen,acquired,cap,'joint_3nn');assert step['row_id']==chosen
                    seen.append(chosen);acquired.append(labels[chosen])
                assert len(seen)==10 and prefix['ids']==seen and prefix['labels']==acquired
                for i in seen:expected_journal.append((family,seed,'prefix',i))
                arms={}
                for method in ['joint_3nn','random']:
                    arm=read(f'results/v17_classical/{method}/{key}.json');ids=seen[:];ys=[v[:] for v in acquired]
                    assert arm['ids'][:10]==prefix['ids'] and arm['labels'][:10]==prefix['labels']
                    for step in arm['steps']:
                        chosen=manual_choice(xs,order,ids,ys,cap,method);assert step['row_id']==chosen,(family,seed,method,step,chosen)
                        ids.append(chosen);ys.append(labels[chosen]);expected_journal.append((family,seed,method,chosen))
                    assert len(ids)==len(set(ids))==20 and ids==arm['ids'] and ys==arm['labels']
                    best=min((y[0],i) for i,y in zip(ids,ys) if y[1]<=cap)
                    assert best==(arm['best_feasible_ms'],arm['best_row'])
                    arms[method]=arm
                # Hidden-label diagnostic occurs only after saved decisions are verified.
                ideal=min(y[0] for y in labels.values() if y[1]<=cap)
                cheap=arms['joint_3nn']['best_feasible_ms'];random_runtime=arms['random']['best_feasible_ms']
                records.append({'family':family,'seed':seed,'size_cap_bytes':cap,'cheap_ms':cheap,'random_ms':random_runtime,
                                'cheap_gain_over_random':(random_runtime-cheap)/random_runtime,
                                'hindsight_fulltable_ms':ideal,'hindsight_headroom_over_cheap':(cheap-ideal)/cheap})
        journal=[json.loads(line) for line in (out/'acquisitions.jsonl').read_text().splitlines()]
        assert len(journal)==len(expected_journal)==450
        assert [(r['family'],r['seed'],r['arm'],r['row_id']) for r in journal]==expected_journal
        assert all(r['charged_recorded_vector']==1 for r in journal)
        groups=[]
        for family in ['zstd','lz4','zlib']:
            rows=[r for r in records if r['family']==family]
            groups.append({'family':family,'cases':len(rows),'mean_gain_over_random':statistics.mean(r['cheap_gain_over_random'] for r in rows),
                           'wins':sum(r['cheap_gain_over_random']>0 for r in rows),'losses':sum(r['cheap_gain_over_random']<0 for r in rows),
                           'mean_hindsight_headroom':statistics.mean(r['hindsight_headroom_over_cheap'] for r in rows),
                           'headroom_above_10pct':sum(r['hindsight_headroom_over_cheap']>.1 for r in rows)})
        summary={'scope':'exploratory classical-only on exposed development measurement tables; no LLM evidence',
                 'cases':records,'groups':groups,'equal_family_mean_gain':statistics.mean(g['mean_gain_over_random'] for g in groups),
                 'recorded_vector_lookups':450,'physical_trials_in_this_stage':0,'new_model_requests':0,'completed_arms':30,'intended_arms':30}
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        with (out/'outcomes.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
        verification={'verified':True,'independent_acquired_only_choice_replay':True,'cases':15,'arms':30,'recorded_vector_lookups':450,'shared_prefix':10,'inclusive_arm_budget':20,'all_development_no_heldout_claim':True}
        (ROOT/'artifacts/study_v17/verification.json').write_text(json.dumps(verification,indent=2)+'\n')
        resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==128 and after['active_since'] is None
    (ROOT/'artifacts/study_v17/final_ledger.json').write_text(json.dumps(after,indent=2)+'\n')
    print(json.dumps({'groups':groups,'equal_family_mean_gain':summary['equal_family_mean_gain'],'remaining_runtime_seconds':1800-after['experiment_seconds']},indent=2))


if __name__=='__main__':main()
