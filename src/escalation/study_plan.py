"""Produce a fail-closed collection plan. This module cannot start inference."""
import hashlib
from .registry import split_groups,validate_assignments


def preflight(config,registry,ledger,current_config):
    split=split_groups(registry['datasets'],config['system_groups_required'],config['test_groups'])
    seeds=config['seeds'];n=config['system_groups_required'];runs=n*len(seeds)
    requests=runs*config['model_requests_per_llm_continuation']+config['feasibility_model_requests']
    labels=runs*(2*config['total_evaluations_per_arm']+2*(config['total_evaluations_per_arm']-config['checkpoint']))
    remaining=current_config['inference']['max_new_model_requests']-ledger['requests']
    seconds=current_config['resources']['max_experiment_runtime_minutes']*60-ledger['experiment_seconds']
    reasons=[]
    if not split['ready']:reasons.append(split['reason'])
    if requests>remaining:reasons.append('planned_requests_exceed_existing_remaining_allowance')
    if not config['proposed_limits_authorized']:reasons.append('proposed_larger_resource_limits_not_authorized')
    if seconds<=0:reasons.append('existing_runtime_exhausted')
    if config['allow_paid_api'] or config['max_external_spend_usd']!=0:reasons.append('paid_inference_forbidden')
    tasks=[]
    if split['ready']:
        selected=[]
        for group in split['assignments']:
            choices=[r for r in registry['datasets'] if r['system_group']==group and not r['exclusion_reasons']]
            selected.append(min(choices,key=lambda r:r['upstream_path']))
        validate_assignments(selected,split['assignments'])
        for row in selected:
            for seed in seeds:
                tasks.append({'dataset_id':row['dataset_id'],'system_group':row['system_group'],
                              'split':split['assignments'][row['system_group']], 'seed':seed,
                              'sha256':row['sha256'],'path':row['path'],'status':'not_collected'})
    return {'ready':not reasons,'reasons':reasons,'split':split,
            'planned_paired_instances':runs,'planned_classical_arms':2*runs,
            'planned_projection_arms':runs,'planned_model_requests':requests,
            'planned_new_label_accesses':labels,'existing_requests_remaining':remaining,
            'existing_seconds_remaining':seconds,'tasks':tasks,
            'execution_implemented':False,
            'scope':'Frozen design/admission audit, not evidence of a larger experiment. A versioned full collector is still required.'}
