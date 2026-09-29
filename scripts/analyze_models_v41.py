"""Analyze only real, provenance-checked V41 model branches; no inference/cache synthesis."""
import csv, hashlib, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines,digest,now
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain,MODES,current_config
from escalation.policy_transfer_v41 import predecision_masks,family_contrast,evaluate_policies,observed_usage
from escalation.resources import Resources
from escalation.selection_v8 import parse_ids
from run_transfer_v41 import verify_freeze

MODELS={'0.5':('Qwen/Qwen2.5-0.5B-Instruct','7ae557604adf67be50417f59c2c2f167def9a775'),
        '1.5':('Qwen/Qwen2.5-1.5B-Instruct','989aa7980e4cf806f80c7fef2b1adb7bc71aa306')}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def unique_records(records):
    result={}
    for r in records:
        key=r['request_id']
        if key in result:raise ValueError('Duplicate request ID; denominator cannot be silently reduced')
        result[key]=r
    return result

def checked_state(record,prefix,events,spec):
    state=State(**prefix['state'])
    if len(events)!=10:raise ValueError('Ten continuation acquisitions required')
    for e in events:
        if e['row_id'] in state.ids or e['source_line']!=spec['subset']['source_lines'][e['row_id']]:raise ValueError('Acquisition identity')
        value=float(e['raw_target'])
        if not __import__('math').isfinite(value) or value<=0:raise ValueError('Invalid measured target')
        state.observe(e['row_id'],[value],(spec['direction'],))
    if state.record()!=record['state'] or record['prefix_hash']!=prefix['prefix_hash'] or len(state.ids)!=20:
        raise ValueError('Shared prefix/recorded state replay mismatch')
    if record['logical_evaluations']!=20 or record['actual_new_accesses']!=10:raise ValueError('Budget accounting')
    return state

def main():
    source=Path('results/v41_models');out=Path('results/v41_model_analysis')
    if not (source/'started.json').exists():raise RuntimeError('No real V41 model collection exists; do not create model results')
    verify_freeze()
    seal=read('results/v41_policy_precommit/analysis_seal.json')
    for path,h in seal['sha256'].items():
        if sha(path)!=h:raise ValueError('Changed analysis/policy precommit: '+path)
    if sha('reports/protocol_v41_transfer.freeze.json')!=seal['original_protocol_freeze_sha256']:raise ValueError('Protocol binding')
    if seal['at']>=read(source/'started.json')['at']:raise ValueError('Policy seal must precede model collection')
    for path,h in read('results/v41_transfer/collection_seal.json')['sha256'].items():
        if sha(path)!=h:raise ValueError('Changed classical collection input')
    m=read('data/manifest_v41.json');decisions=read('results/v41_policy_precommit/decisions.json')
    masks,scores=predecision_masks(decisions['rows'],read('results/v6/router_seal.json'))
    if masks!=decisions['masks'] or scores!=decisions['benefit_scores']:raise ValueError('Policy prediction replay')
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check();starts=[];responses=[]
        for size in MODELS:
            starts+=lines(source/size/'request_starts.jsonl');responses+=lines(source/size/'requests.jsonl')
        starts_by_id=unique_records(starts);responses_by_id=unique_records(responses)
        if not set(responses_by_id)<=set(starts_by_id):raise ValueError('Response without request start')
        missing=set(starts_by_id)-set(responses_by_id);acquisitions=lines(source/'acquisitions.jsonl')
        progress=read(source/'progress.json') if (source/'progress.json').exists() else {'complete':False,'stop_reason':'No terminal progress receipt'}
        intended={(size,d['id'],seed) for size in MODELS for d in m['datasets'] for seed in m['seeds']}
        observed={(r['model_size'],r['dataset'],r['seed']) for r in starts}
        if not observed<=intended or len(starts)>60 or len(acquisitions)>600:raise ValueError('Off-protocol or excess collection')
        accounting={'intended_cases':60,'request_attempts_observed':len(starts),'request_responses_observed':len(responses),
            'missing_response_records':sorted(missing),'new_objective_accesses_observed':len(acquisitions),
            'research_collection_including_classical_objective_accesses':2400+len(acquisitions),
            'observed_input_tokens':None if missing else observed_usage(responses,'input_tokens'),
            'observed_output_tokens':None if missing else observed_usage(responses,'output_tokens'),
            'observed_request_wall_seconds':observed_usage(responses,'wall_seconds'),
            'request_time_complete':not missing,'errors':sum(r['status']!='response' for r in responses),
            'external_spend_usd':0,'new_live_physical_trials':0,
            'stage_accounting':read('artifacts/study_v41/model_accounting.json') if Path('artifacts/study_v41/model_accounting.json').exists() else None}
        write(out/'collection_cost.json',accounting)
        if not progress['complete'] or missing or observed!=intended or len(starts)!=60 or len(responses)!=60 or len(acquisitions)!=600:
            write(out/'incomplete.json',{'at':now(),'primary_aggregate_computed':False,'intended_cases':60,
                'observed_cases':[list(t) for t in sorted(observed)],'progress':progress,
                'reason':'Incomplete intended collection retained; no complete-case quality/policy aggregate'})
            print('Incomplete collection retained; primary aggregates refused')
            return
        all_rows=[];contrasts=[];policies=[];groups=[r['system_group'] for r in decisions['rows']]
        specifications={d['id']:d for d in m['datasets']}
        for size,(model_id,revision) in MODELS.items():
            runtime=read(source/size/'model_runtime.json')
            if (runtime['model_id'],runtime['revision'],runtime['provider'])!=(model_id,revision,'local_transformers'):
                raise ValueError('Wrong model provenance')
            requests=[];case_states=[];prefix_seconds=[]
            for identity in decisions['rows']:
                resource.check();dataset,seed=identity['dataset'],identity['seed'];key=f'{dataset}_{seed}';spec=specifications[dataset]
                p=read(f'results/v41_transfer/prefixes/{key}.json');arm=read(source/size/'arms'/f'{key}.json')
                response=responses_by_id[arm['request_id']];start=starts_by_id[arm['request_id']]
                for record in (start,response):
                    if (record['dataset'],record['seed'],record['system_group'],record['model_size'],record['model_id'],record['revision'])!=(dataset,seed,spec['system_group'],size,model_id,revision):raise ValueError('Request identity mismatch')
                    if record['namespace']!='measured_v41_llm' or record['messages']!=p['messages'] or record['prefix_hash']!=p['prefix_hash']:raise ValueError('Prompt/prefix/provenance mismatch')
                    if record['parameters']!={'do_sample':False,'max_new_tokens':20}:raise ValueError('Wrong inference parameters')
                if response['input_tokens'] is not None and response['input_tokens']>4096:raise ValueError('Input token cap')
                events=[e for e in acquisitions if (e['model_size'],e['dataset'],e['seed'])==(size,dataset,seed)]
                state=checked_state(arm,p,events,spec)
                if arm['fallback'] is None:
                    if response['status']!='response' or parse_ids(response['raw_output'],p['pool'])!=state.ids[10:]:raise ValueError('Model proposal replay')
                else:
                    control=read(f'results/v41_transfer/arms/{key}_batch_3nn.json')
                    if state.record()!=control['state']:raise ValueError('Fallback is not frozen batch control')
                requests.append(response);case_states.append((p,spec,state,arm));prefix_seconds.append(p['prefix_seconds'])
            for mode in MODES:
                gains=[];classical_seconds=[]
                for p,spec,state,arm in case_states:
                    key=f"{p['dataset']}_{p['seed']}";control=read(f'results/v41_transfer/arms/{key}_{mode}.json')
                    target=best(state,spec['direction']);reference=best(State(**control['state']),spec['direction'])
                    gain=relative_gain(reference,target,spec['direction']);gains.append(gain);classical_seconds.append(control['branch_seconds'])
                    all_rows.append({'model_size':size,'dataset':p['dataset'],'system_group':spec['system_group'],'seed':p['seed'],
                        'reference':mode,'reference_best':reference,'llm_best':target,'relative_gain':gain,
                        'fallback':arm['fallback'] is not None,'prefix_hash':p['prefix_hash']})
                contrasts.append({'model_size':size,'reference':mode,**family_contrast(gains,groups)})
                if mode in ('batch_3nn','full_sequential_3nn'):
                    policies += [{'model_size':size,'reference':mode,**r} for r in evaluate_policies(gains,groups,masks,requests,prefix_seconds,classical_seconds)]
        write(out/'summary.json',{'at':now(),'intended_cases':60,'completed_cases':60,'contrasts':contrasts,'policies':policies,
            'collection_cost':accounting,'scope':'Six-family exploratory transfer; old routers were not refit; two sizes of one model family; no journal-readiness certification'})
        with (out/'paired_cases.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=all_rows[0].keys());writer.writeheader();writer.writerows(all_rows)
        write(out/'analysis_inputs.json',{'sha256':{str(p):sha(p) for p in sorted(source.rglob('*')) if p.is_file()}})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/model_analysis_accounting.json',{'seconds':after['experiment_seconds']-before['experiment_seconds'],
        'new_model_calls':after['requests']-before['requests'],'new_objective_acquisitions':0})
    print('Verified and analyzed all60 real model cases;420 paired comparator rows')

if __name__=='__main__':main()
