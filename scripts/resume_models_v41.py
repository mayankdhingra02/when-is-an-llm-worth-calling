"""Recover only unattempted 1.5B cases after the recorded OpenMP startup failure.

No request retry, completed case replacement, model/prompt change or cap increase.
The initial failed startup remains included in cumulative stage accounting.
"""
import hashlib,os,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,append,lines,digest,now
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import parse_ids
from escalation.transfer_v41 import restrict,IndexedOracle,rank
from escalation.resources import Resources
from escalation.order_probe_v19 import StageResources
from escalation.provider_v22 import LargerProvider
from run_models_v41 import authorized_config
from run_transfer_v41 import verify_freeze

OUT=Path('results/v41_models')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    verify_freeze();cfg=authorized_config(read('configs/authorization_v41.json'),sha('reports/protocol_v41_transfer.freeze.json'))
    ledger=read('artifacts/resource_ledger_v2.json');initial=read('artifacts/study_v41/model_accounting.json')
    if ledger['requests']!=260 or ledger['active_since'] is not None or initial['requests']!=30 or initial['new_accesses']!=300:
        raise ValueError('Recovery only from exact thirty completed0.5B cases')
    if lines(OUT/'1.5/request_starts.jsonl') or list((OUT/'1.5').glob('arms/*.json')):raise ValueError('No1.5B request may already be attempted')
    if read(OUT/'progress.json')['stop_reason']!='EOFError: ' or 'OMP: Error #179' not in Path('artifacts/study_v41/model_collection.log').read_text():raise ValueError('Different failure; no automatic recovery')
    if len(list((OUT/'0.5/arms').glob('*.json')))!=30:raise ValueError('Incomplete initial model denominator')
    for p,h in read('results/v41_transfer/collection_seal.json')['sha256'].items():
        if sha(p)!=h:raise ValueError('Changed fixed collection input')
    for p,h in read('results/v41_policy_precommit/analysis_seal.json')['sha256'].items():
        if sha(p)!=h:raise ValueError('Changed policy precommit')
    history=Path('artifacts/study_v41/recovery_attempt1')
    if history.exists():raise ValueError('Recovery is one-shot')
    history.mkdir()
    for p in [OUT/'progress.json',Path('artifacts/study_v41/model_accounting.json'),Path('artifacts/study_v41/model_collection.log')]:shutil.copy2(p,history/p.name)
    preserved={str(p):sha(p) for p in (OUT/'0.5').rglob('*') if p.is_file()}
    remaining_stage=700-initial['charged_seconds'];stop=None;acquired=0
    write(history/'recovery_plan.json',{'at':now(),'reason':'OpenMP shared-memory failure during1.5B startup before requests; execution recovery only',
        'remaining_stage_seconds':remaining_stage,'new_request_limit':30,'new_access_limit':300,'completed0.5_files':preserved,
        'script_sha256':sha(__file__),'initial_failure_retained':True,'original_protocol_unchanged':True})
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        if resource.remaining()<remaining_stage+10:raise RuntimeError('Insufficient unchanged global reserve')
        stage=StageResources(resource,remaining_stage)
        try:
            with LargerProvider(cfg,stage,OUT/'1.5/requests.jsonl') as model:
                for spec in read('data/manifest_v41.json')['datasets']:
                    c,subset=restrict(load_candidates(spec),spec['fixed_features'])
                    if subset!=spec['subset']:raise ValueError('Changed domain')
                    for seed in read('data/manifest_v41.json')['seeds']:
                        stage.check();key=f"{spec['id']}_{seed}";p=read(f'results/v41_transfer/prefixes/{key}.json');state=State(**p['state'])
                        if digest(state.record())!=p['prefix_hash'] or digest(p['messages'])!=p['prompt_hash']:raise ValueError('Prefix/prompt changed')
                        context={'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'model_size':'1.5',
                            'namespace':'measured_v41_llm','prefix_hash':p['prefix_hash'],'grammar_mode':'candidate_order_v19','prompt_version':'candidate_ids_v8'}
                        response=model.request(p['messages'],context);fallback=None
                        try:
                            if response['status']!='response':raise ValueError('Model request failed')
                            selected=parse_ids(response['raw_output'],p['pool'])
                        except Exception as e:fallback=str(e);selected=rank(c,state,p['pool']['ranked'])[:10]
                        oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{**context,**e,'at':now()}))
                        for row in selected:
                            stage.check()
                            if acquired>=300:raise RuntimeError('Remaining access cap')
                            acquired+=1;state.observe(row,oracle.acquire(row),c.directions)
                            write(OUT/'1.5/checkpoints'/f'{key}.json',state.record())
                        write(OUT/'1.5/arms'/f'{key}.json',{**context,'status':'completed','state':state.record(),'fallback':fallback,
                            'request_id':response['request_id'],'logical_evaluations':20,'actual_new_accesses':oracle.new_accesses})
                        print('1.5',key,'completed',flush=True)
        except Exception as e:stop=f'{type(e).__name__}: {e}'
        finally:
            m=read('data/manifest_v41.json')
            statuses=[{'model_size':size,'dataset':d['id'],'seed':seed,'status':'completed' if (OUT/size/'arms'/f"{d['id']}_{seed}.json").exists() else 'incomplete_or_unattempted'} for size in ('0.5','1.5') for d in m['datasets'] for seed in m['seeds']]
            write(OUT/'progress.json',{'arms':statuses,'complete':all(r['status']=='completed' for r in statuses),'stop_reason':stop,
                'prior_startup_failure':'recovery_attempt1 retains original EOF/OpenMP failure; no1.5request retry'})
    after=read('artifacts/resource_ledger_v2.json')
    for p,h in preserved.items():
        if sha(p)!=h:raise ValueError('Completed0.5B evidence changed')
    write('artifacts/study_v41/model_accounting.json',{'requests':initial['requests']+after['requests']-ledger['requests'],
        'charged_seconds':initial['charged_seconds']+after['experiment_seconds']-ledger['experiment_seconds'],
        'new_accesses':initial['new_accesses']+acquired,'external_spend_usd':0,'startup_failures':1,
        'request_retries':0,'preserved_completed0.5_files':len(preserved),'recovery_seconds':after['experiment_seconds']-ledger['experiment_seconds']})
    if stop:raise RuntimeError(stop)

if __name__=='__main__':main()
