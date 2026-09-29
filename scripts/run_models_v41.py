"""Prepared real-model continuation; fail closed until exact extension is granted."""
import hashlib, os, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read, write, append, lines, digest, now
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import parse_ids
from escalation.transfer_v41 import restrict, IndexedOracle, rank, current_config
from escalation.resources import Resources
from escalation.order_probe_v19 import StageResources
from escalation.provider_v19 import OrderProbeProvider
from escalation.provider_v22 import LargerProvider
from run_transfer_v41 import verify_freeze

OUT=Path('results/v41_models')

def authorized_config(authorization, freeze_hash):
    required={'granted':True,'additional_requests':60,'request_cap':290,'runtime_cap_seconds':3600,
              'stage_seconds':700,'max_new_vectors':600,'external_spend_usd':0,'new_downloads':0,
              'protocol_freeze_sha256':freeze_hash}
    if any(authorization.get(k)!=v for k,v in required.items()) or not authorization.get('user_authorization'):
        raise PermissionError('Exact V41 extension is required: 60 local requests, cap230->290, unchanged3600s, USD0')
    cfg=current_config();cfg['inference'].update(max_new_model_requests=290,max_output_tokens_per_request=20,request_timeout_seconds=30)
    if cfg['inference']['allow_paid_api'] or cfg['inference']['max_external_spend_usd']!=0:raise PermissionError('Paid inference disabled')
    return cfg

def main():
    if OUT.exists():raise ValueError('Preserve prior attempt')
    verify_freeze()
    auth_path=Path('configs/authorization_v41.json')
    if not auth_path.exists():raise PermissionError('Model phase blocked: 230/230 calls used; exact60-call extension not yet granted')
    cfg=authorized_config(read(auth_path),hashlib.sha256(Path('reports/protocol_v41_transfer.freeze.json').read_bytes()).hexdigest())
    seal=read('results/v41_transfer/collection_seal.json')
    for path,h in seal['sha256'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=h:raise ValueError('Changed collection input')
    if not read('results/v41_transfer/model_preflight.json')['all_fit']:raise ValueError('Token preflight failure')
    m=read('data/manifest_v41.json');before=read('artifacts/resource_ledger_v2.json');stop=None;acquired=0
    if before['requests']!=230:raise ValueError('Expected initial ledger230')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        if resource.remaining()<710:raise RuntimeError('Need700-second stage and cleanup reserve')
        stage=StageResources(resource,700)
        write(OUT/'started.json',{'at':now(),'cases':60,'baseline_ledger':before})
        try:
            for size, provider in [('0.5',OrderProbeProvider),('1.5',LargerProvider)]:
                with provider(cfg,stage,OUT/size/'requests.jsonl') as model:
                    for spec in m['datasets']:
                        c,subset=restrict(load_candidates(spec),spec['fixed_features'])
                        if subset!=spec['subset']:raise ValueError('Changed candidate domain')
                        for seed in m['seeds']:
                            stage.check();key=f"{spec['id']}_{seed}";p=read(f'results/v41_transfer/prefixes/{key}.json')
                            state=State(**p['state'])
                            if digest(state.record())!=p['prefix_hash'] or digest(p['messages'])!=p['prompt_hash']:raise ValueError('Prefix/prompt hash mismatch')
                            context={'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'model_size':size,
                                     'namespace':'measured_v41_llm','prefix_hash':p['prefix_hash'],'grammar_mode':'candidate_order_v19','prompt_version':'candidate_ids_v8'}
                            response=model.request(p['messages'],context);fallback=None
                            try:
                                if response['status']!='response':raise ValueError('Model request failed')
                                selected=parse_ids(response['raw_output'],p['pool'])
                            except Exception as e:
                                fallback=str(e);selected=rank(c,state,p['pool']['ranked'])[:10]
                            oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{**context,**e,'at':now()}))
                            for row in selected:
                                stage.check()
                                if acquired>=600:raise RuntimeError('600-vector cap')
                                acquired+=1;state.observe(row,oracle.acquire(row),c.directions)
                                write(OUT/size/'checkpoints'/f'{key}.json',state.record())
                            write(OUT/size/'arms'/f'{key}.json',{**context,'status':'completed','state':state.record(),'fallback':fallback,
                                'request_id':response['request_id'],'logical_evaluations':20,'actual_new_accesses':oracle.new_accesses})
                            print(size,key,'completed',flush=True)
        except Exception as e:stop=f'{type(e).__name__}: {e}'
        finally:
            statuses=[{'model_size':size,'dataset':d['id'],'seed':seed,'status':'completed' if (OUT/size/'arms'/f"{d['id']}_{seed}.json").exists() else 'incomplete_or_unattempted'} for size in ('0.5','1.5') for d in m['datasets'] for seed in m['seeds']]
            write(OUT/'progress.json',{'arms':statuses,'complete':all(r['status']=='completed' for r in statuses),'stop_reason':stop})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/model_accounting.json',{'requests':after['requests']-before['requests'],
        'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'new_accesses':acquired,'external_spend_usd':0})
    if stop:raise RuntimeError(stop)

if __name__=='__main__':main()
