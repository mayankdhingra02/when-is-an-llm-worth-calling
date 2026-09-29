"""Collect five saved prefixes, precommit policies, then four isolated controls."""
import json,time
from table_check_v121 import ROOT,read,write,append,sha,now,frozen,candidates,MODES,SEEDS
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.finite_v6 import features
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import IndexedOracle,branch,messages
from escalation.policy_transfer_v41 import predecision_masks
from escalation.io import digest
from portfolio_v115 import portfolio
OUT=ROOT/'results/v121_classical'

def main():
    for n,h in read(ROOT/'artifacts/study_v121/router_inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    frozen();cfg=read(ROOT/'configs/study_v121.json');spec,c,subset=candidates()
    assert not OUT.exists();OUT.mkdir();start=time.monotonic();count=0;stop=None;context={};prepared=[]
    intended=[{'seed':seed,'arm':arm} for seed in SEEDS for arm in ('prefix',)+MODES]
    write(OUT/'started.json',{'at':now(),'intended':intended,'cap':300,'subset':subset,'scope':'Recorded author labels only; utility/correctness unverified'})
    def journal(e):append(OUT/'acquisitions.jsonl',{'namespace':'measured_v121_recorded','at':now(),**context,**e})
    try:
        for seed in SEEDS:
            key=f"{spec['id']}_{seed}";context={'key':key,'seed':seed,'dataset':spec['id'],'system_group':'mongodb','arm':'prefix'}
            oracle=IndexedOracle(spec,c,journal=journal);state=initial_state(c,seed);t=time.perf_counter()
            def acquire(row):
                nonlocal count
                if count>=300 or time.monotonic()-start>=180:raise RuntimeError('Classical stage cap')
                count+=1;return oracle.acquire(row)
            for _ in range(10):
                row=recommend(c,state);state.observe(row,acquire(row),c.directions)
                write(OUT/'prefix_checkpoints'/f'{key}.json',state.record())
            pool=shortlist(c,state,seed);fs,feature_seconds=features(c,state,seed)
            p={**context,'state':state.record(),'pool':pool,'features':fs,'messages':messages(c,state,pool),
               'prefix_hash':digest(state.record()),'actual_new_accesses':10,'prefix_seconds':time.perf_counter()-t,'feature_seconds':feature_seconds}
            write(OUT/'prefixes'/f'{key}.json',p);prepared.append((key,seed,state,pool,p));print(key,'prefix saved',flush=True)
        rows=[{k:p[k] for k in ('dataset','seed','system_group','features')} for *_,p in prepared]
        seal=read(ROOT/'results/v121_router/router_seal.json');training=read(ROOT/'results/v121_router/development_outcomes.json')
        assert sha(ROOT/'results/v121_router/router_seal.json')==read(ROOT/'results/v121_router/router_seal.sha256.json')['sha256']
        assert digest(training)==seal['development_rows_sha256'] and 'mongodb' not in {r['system_group'] for r in training}
        masks,scores=predecision_masks(rows,seal)
        first_masks,first_scores=predecision_masks(rows,read(ROOT/'results/v121_router/router_first10_seal.json'))
        write(OUT/'policy_precommit.json',{'at':now(),'rows':rows,'masks':masks,'scores':scores,'controller_sha256':sha(ROOT/'results/v121_router/router_seal.json'),
          'first10_masks':first_masks,'first10_scores':first_scores,'continuation_outcomes_used':False,'fitted_on_new_data':False,'training_groups':sorted({r['system_group'] for r in training})})
        for key,seed,prefix,pool,p in prepared:
            for mode in MODES:
                context={'key':key,'seed':seed,'dataset':spec['id'],'system_group':'mongodb','arm':mode}
                oracle=IndexedOracle(spec,c,prefix.record(),journal);t=time.perf_counter()
                if mode=='presentation_first10':
                    state=prefix.clone();trace=None
                    for i in '0123456789':
                        row=pool['mapping'][i];state.observe(row,acquire(row),c.directions)
                elif mode=='single_portfolio':state,trace=portfolio(c,prefix,pool['ranked'],acquire)
                else:state=branch(c,prefix,pool['ranked'],seed,mode,acquire);trace=None
                assert state.ids[:10]==prefix.ids and state.labels[:10]==prefix.labels and len(state.ids)==20 and oracle.new_accesses==10
                write(OUT/'arms'/f'{key}_{mode}.json',{**context,'state':state.record(),'trace':trace,'status':'completed','logical_evaluations':20,'actual_new_accesses':10,'branch_seconds':time.perf_counter()-t,'prefix_sha256':sha(OUT/'prefixes'/f'{key}.json')})
            print(key,'four controls completed',flush=True)
    except Exception as e:stop=repr(e)
    finally:
        statuses=[{**r,'status':'completed' if (OUT/('prefixes' if r['arm']=='prefix' else 'arms')/(f"{spec['id']}_{r['seed']}"+('' if r['arm']=='prefix' else '_'+r['arm'])+'.json')).exists() else 'incomplete_or_unattempted'} for r in intended]
        write(OUT/'progress.json',{'complete':stop is None and all(r['status']=='completed' for r in statuses),'stop_reason':stop,'intended':statuses,'actual_new_acquisitions':count,'stage_seconds':time.monotonic()-start,'new_model_requests':0})
    if stop:raise RuntimeError(stop)
    assert count==300
    jobs=[{'key':key,'base_key':key,'dataset':spec['id'],'system_group':'mongodb','seed':11,'sampling_seed':11,'optimization_seed':seed,'mode':'nonthinking','prefix':str((OUT/'prefixes'/f'{key}.json').relative_to(ROOT))} for key,seed,*_ in prepared]
    write(ROOT/'artifacts/study_v121/jobs.json',jobs)
    paths=[OUT/'policy_precommit.json',ROOT/'artifacts/study_v121/jobs.json']+list((OUT/'prefixes').glob('*.json'))
    write(ROOT/'artifacts/study_v121/classical_inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}})

if __name__=='__main__':main()
