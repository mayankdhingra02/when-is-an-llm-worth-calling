"""Execute only the frozen, non-LLM control on previously exposed v3 prefixes."""
import os,time
from pathlib import Path
from .config import load_config
from .core import State
from .data import Oracle,read_table,sha,validate_manifest
from .evaluator import evaluate
from .io import append,digest,lines,now,read,write
from .projection_control import VERSION,continue_projection,proposal_seed
from .resources import Resources

ROOT=Path(__file__).resolve().parents[2]
OUT=Path('results/v4_projection_diagnostic')


def verify_freeze():
    frozen=read('reports/protocol_v4.freeze.json')
    for path,expected in frozen['sha256'].items():
        if sha(path)!=expected:raise RuntimeError(f'frozen input changed: {path}')
    return frozen


def main():
    os.chdir(ROOT);freeze=verify_freeze()
    if OUT.exists():raise RuntimeError('refusing overwrite/repeat diagnostic; use audited versioned output')
    data=read('data/manifest_v3.json');validate_manifest(data)
    config=load_config('configs/followup_v3.yaml')
    write(OUT/'manifest.json',{'started':now(),'namespace':'measured_non_llm_projection_diagnostic',
          'intended_runs':15,'protocol_sha256':sha('reports/protocol_v4.md'),
          'freeze':freeze,'data_manifest_sha256':sha('data/manifest_v3.json'),
          'comparison_input_sha256':{p:sha(p) for p in ['results/v3/runs.jsonl','results/v3/classical/runs.jsonl']},
          'method':VERSION,'new_llm_requests':0,'scope':'exploratory on exposed v3 systems'})
    stop=None
    with Resources(config,'artifacts/resource_ledger_v2.json') as resource:
        for dataset in data['datasets']:
            c,labels,_=read_table(dataset['path'])
            for seed in config['seed_list']:
                p=read(f'results/v3/classical/prefixes/{dataset["id"]}_{seed}.json')
                if p['prefix_hash']!=digest(p['state']) or p['data_sha256']!=dataset['sha256']:
                    raise RuntimeError('prefix integrity failed')
                state=State(**p['state']);oracle=Oracle(labels,prefix=p['state'])
                checkpoint=OUT/f'checkpoints/{dataset["id"]}_{seed}.json'
                def save(s,events):write(checkpoint,{'state':s.record(),'events':events,'prefix_hash':p['prefix_hash']})
                status='blocked' if stop else 'completed';events=[];start=time.perf_counter()
                derived_seed=proposal_seed(dataset['sha256'],seed)
                if not stop:
                    try:events=continue_projection(c,state,oracle,derived_seed,save,resource)
                    except Exception as error:
                        stop=f'{type(error).__name__}: {error}';status='failed'
                if not events and checkpoint.exists():events=read(checkpoint)['events']
                append(OUT/'runs.jsonl',{'dataset':dataset['id'],'system_group':dataset['system_group'],
                    'split':'exposed_pilot_diagnostic','seed':seed,'derived_proposal_seed':derived_seed,
                    'method':VERSION,'namespace':'measured_non_llm_projection_diagnostic',
                    'status':status,'error':stop,'ids':state.ids,'labels':state.labels,
                    'prefix_hash':p['prefix_hash'],'data_sha256':dataset['sha256'],
                    'logical_evaluations':len(state.ids),'actual_new_accesses':oracle.new_accesses,
                    'requests':0,'input_tokens':0,'output_tokens':0,
                    'branch_seconds':time.perf_counter()-start,'prefix_seconds':p['prefix_seconds'],
                    'events':events,**evaluate(labels,c.directions,state.ids)})
                print(dataset['id'],seed,status,flush=True)
                resource.checkpoint()
    records=lines(OUT/'runs.jsonl')
    write(OUT/'completed.json',{'finished':now(),'intended':15,'completed':sum(r['status']=='completed' for r in records),
                              'actual_new_label_accesses':sum(r['actual_new_accesses'] for r in records),'model_requests':0,'stop_reason':stop})

if __name__=='__main__':main()
