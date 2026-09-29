"""Execute frozen paired classical controls; labels stay behind a charged oracle."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.offline_live_v17 import candidates,RecordedOracle,make_prefix,continuation
from escalation.resources import Resources


def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def append(p,d):
    import os
    with (ROOT/p).open('a') as f:f.write(json.dumps(d)+'\n');f.flush();os.fsync(f.fileno())


def main():
    out=Path('results/v17_classical')
    if (ROOT/out/'started.json').exists():raise RuntimeError('Preserve started/completed study; no automatic recollection')
    for name,h in read('reports/protocol_v17_expansion.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
    before=read('artifacts/resource_ledger_v2.json')
    if before.get('active_since') or 1800-before['experiment_seconds']<10:raise RuntimeError('Insufficient inactive runtime allowance')
    measurement=read('results/v17_measurements/summary.json')
    if measurement['status_counts']!={'ok':846} or measurement['unattempted_trials']!=0 or any(g['unstable_output_configurations'] for g in measurement['groups']):raise RuntimeError('Require complete stable-output grid; no filtering or imputation')
    write('artifacts/study_v17/recorded_table_binding.json',{'sha256':hashlib.sha256((ROOT/'results/v17_measurements/configuration_summary.csv').read_bytes()).hexdigest()})
    manifest=read('data/live_manifest_v17.json');cases=[(d,s) for d in manifest['datasets'] for s in [11,23,37,53,71]]
    write('artifacts/study_v17/classical_baseline_ledger.json',before)
    write(out/'started.json',{'intended_cases':15,'intended_arms':30,'intended_recorded_vector_lookups':450})
    resource_config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    complete=0
    with Resources(resource_config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for dataset,seed in cases:
            resource.check()
            family=dataset['system_group'];key=f'{family}_{seed}'
            c,ids,reference=candidates(dataset)
            def journal(arm):return lambda row:append(out/'acquisitions.jsonl',dict(row,family=family,seed=seed,arm=arm))
            source=ROOT/'results/v17_measurements/configuration_summary.csv'
            initial=RecordedOracle(source,family,ids,journal('prefix'),budget=10)
            prefix=make_prefix(c,ids,reference,seed,initial)
            write(out/'prefixes'/f'{key}.json',prefix)
            arms={}
            for method in ['joint_3nn','random']:
                resource.check()
                oracle=RecordedOracle(source,family,ids,journal(method),budget=20,prefix=dict(zip(prefix['ids'],copy.deepcopy(prefix['labels']))))
                arms[method]=continuation(c,prefix,oracle,method)
                write(out/method/f'{key}.json',arms[method])
            complete+=1
            write(out/'progress.json',{'intended_cases':15,'completed_cases':complete,'completed_arms':complete*2,'remaining_cases':15-complete})
        resource.checkpoint()
    write('artifacts/study_v17/classical_collection_ledger.json',read('artifacts/resource_ledger_v2.json'))
    print('Completed15 pairs/30 arms;450 recorded-vector lookups;0 model calls/physical trials.')


if __name__=='__main__':main()
