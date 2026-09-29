"""Acquire only selected outcomes, replay paired budgets, then report every comparator."""
import csv, hashlib, json, os, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.core import State
from escalation.io import read,write,append,digest,lines
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict,IndexedOracle,best,relative_gain,MODES
from escalation.policy_transfer_v41 import family_contrast

SOURCE=Path('results/v47_smollm');OUT=Path('results/v47_analysis')
def main():
    if OUT.exists():raise ValueError('Preserve evaluated evidence; no reacquisition')
    started=time.monotonic()
    cfg=read('configs/study_v47.json');jobs=read('artifacts/study_v47/jobs.json')
    for path,h in read('reports/protocol_v47_smollm.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=h:raise ValueError('Changed frozen input '+path)
    ledger=read(SOURCE/'ledger.json')
    if ledger['completed_cases']!=30 or any(not (SOURCE/'choices'/f"{j['key']}.json").exists() for j in jobs):
        write('artifacts/study_v47/incomplete.json',{'intended_cases':30,'observed':ledger,'primary_aggregates':False})
        raise ValueError('Incomplete denominator: no complete-case primary means')
    if ledger['stage_seconds']>600 or ledger['requests']>300:raise ValueError('Exceeded model budget')
    OUT.mkdir();manifest=read('data/manifest_v41.json');specs={d['id']:d for d in manifest['datasets']}
    candidates={k:restrict(load_candidates(s),s['fixed_features'])[0] for k,s in specs.items()}
    requests=lines(SOURCE/'request_starts.jsonl');responses=lines(SOURCE/'responses.jsonl')
    response_map={r['request_id']:r for r in responses}
    if len(response_map)!=len(responses) or len(requests)!=ledger['requests']:raise ValueError('Request identity')
    rows=[];accesses=0
    for job in jobs:
        p=read(job['prefix']);choice=read(SOURCE/'choices'/f"{job['key']}.json")
        spec=specs[job['dataset']];c=candidates[job['dataset']]
        state=State(**p['state']).clone()
        if len(state.ids)!=10 or digest(state.record())!=p['prefix_hash']:raise ValueError('Prefix budget/hash')
        if choice['prefix_hash']!=p['prefix_hash']:raise ValueError('Wrong shared prefix')
        selected=choice['selected_ids']
        if choice['fallback_reason'] is None:
            if len(selected)!=10 or len(set(selected))!=10:raise ValueError('Invalid selection')
            if [response_map[i]['response']['content'] for i in choice['request_ids']]!=selected:raise ValueError('Response identity')
            selected_rows=[p['pool']['mapping'][i] for i in selected]
        else:
            saved=read(f"results/v41_transfer/arms/{job['key']}_batch_3nn.json")
            selected_rows=saved['state']['ids'][10:]
        oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'case':job['key'],**e}))
        for row in selected_rows:
            if accesses>=cfg['max_new_objective_accesses']:raise ValueError('Acquisition cap')
            accesses+=1;state.observe(row,oracle.acquire(row),c.directions)
        if len(state.ids)!=20 or len(set(state.ids))!=20 or oracle.new_accesses!=10:raise ValueError('Arm budget')
        write(OUT/'arms'/f"{job['key']}.json",{**choice,'state':state.record(),'logical_evaluations':20,'actual_new_accesses':10})
        target=best(state,spec['direction']);references={}
        for mode in MODES:
            a=read(f"results/v41_transfer/arms/{job['key']}_{mode}.json")
            if a['state']['ids'][:10]!=p['state']['ids'] or a['state']['labels'][:10]!=p['state']['labels']:raise ValueError('Unpaired comparator')
            references[mode]=best(State(**a['state']),spec['direction'])
        for size in ('0.5','1.5'):
            a=read(f"results/v41_models/{size}/arms/{job['key']}.json")
            if a['state']['ids'][:10]!=p['state']['ids'] or a['state']['labels'][:10]!=p['state']['labels']:raise ValueError('Unpaired Qwen')
            references['qwen_'+size]=best(State(**a['state']),spec['direction'])
        rr=[response_map[i] for i in choice['request_ids'] if i in response_map]
        def total(field):
            vals=[r['response'].get(field) for r in rr]
            return sum(vals) if len(rr)==len(choice['request_ids']) and all(isinstance(x,(int,float)) for x in vals) else None
        rows.append({**job,'target':target,'references':references,
            'gains':{k:relative_gain(v,target,spec['direction']) for k,v in references.items()},
            'fallback_reason':choice['fallback_reason'],'generation_requests':len(choice['request_ids']),
            'case_seconds':choice['case_seconds'],'input_tokens_full_context_sum':total('tokens_evaluated'),
            'output_tokens':total('tokens_predicted')})
    groups=[r['system_group'] for r in rows]
    contrasts={k:family_contrast([r['gains'][k] for r in rows],groups) for k in rows[0]['gains']}
    decisions=read('results/v41_policy_precommit/decisions.json')
    index={(r['dataset'],r['seed']):i for i,r in enumerate(decisions['rows'])}
    policies=[]
    for ref in ('batch_3nn','full_sequential_3nn'):
        gains=[r['gains'][ref] for r in rows]
        masks={k:[v[index[(r['dataset'],r['seed'])]] for r in rows] for k,v in decisions['masks'].items()}
        masks['hindsight_oracle_diagnostic']=[g>0 for g in gains]
        for name,mask in masks.items():
            policies.append({'policy':name,'comparator':ref,'selected_cases':sum(mask),
                'generation_requests_if_deployed':sum(r['generation_requests'] for r,m in zip(rows,mask) if m),
                'observed_model_seconds_selected':sum(r['case_seconds'] for r,m in zip(rows,mask) if m),
                'cost_excludes':'startup, objective access, controller cost; historical classical timings separately available in V41',
                'nondeployable_diagnostic':name.endswith('_diagnostic'),
                'contrast':family_contrast([g if m else 0 for g,m in zip(gains,mask)],groups)})
    meaningful=all(contrasts[k]['family_mean_gain']>0 and contrasts[k]['bootstrap95'][0]>0 for k in ('batch_3nn','full_sequential_3nn'))
    summary={'intended_cases':30,'completed_cases':len(rows),'families':len(set(groups)),
        'fallbacks':sum(r['fallback_reason'] is not None for r in rows),'contrasts':contrasts,'policies':policies,
        'meets_predeclared_screening_criterion':meaningful,
        'qualification':'Exploratory exposed-system cross-model/runtime bundle robustness. Not held-out or journal-readiness evidence.',
        'collection':{'new_generation_requests':ledger['requests'],'new_semantic_continuations':30,
            'new_objective_accesses':accesses,'generation_stage_seconds':ledger['stage_seconds'],
            'evaluation_seconds':time.monotonic()-started,'external_spend_usd':0,
            'historical_research_followup_requests':350,'v46_hardware_requests':2,
            'followup_request_total_including_this_stage':352+ledger['requests'],
            'all_requests_including_original100':452+ledger['requests'],
            'historical_recorded_accesses':14408,'cumulative_recorded_accesses':14408+accesses,
            'deployment_scope':'per-policy selected branch only, historical collection not free'}}
    write(OUT/'cases.json',rows);write(OUT/'summary.json',summary)
    with (OUT/'contrasts.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['case','family','comparator','smollm_target','reference_target','relative_gain'])
        for r in rows:
            for k,g in r['gains'].items():w.writerow([r['key'],r['system_group'],k,r['target'],r['references'][k],g])
    print(json.dumps({k:{a:v[a] for a in ('family_mean_gain','bootstrap95','wins','ties','harms')} for k,v in contrasts.items()},indent=2))

if __name__=='__main__':main()
