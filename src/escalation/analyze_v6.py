"""Analysis of sealed policies; never fit on held-out outcomes."""
import csv,random
from pathlib import Path
import numpy as np
from .io import read,write,lines,digest
from .data import sha
from .router import group_mean,GRID
from .resources import Resources
from .config import load_config
from .study_v6 import OUT,outcome_rows,verify_freeze

def policy_masks(rows,seal):
    r=seal['benefit'];x=np.array([[row['features'][k] for k in r['features']] for row in rows])
    scores=((x-np.array(r['mean']))/np.array(r['scale']))@np.array(r['coefficient'])+r['intercept']
    threshold=float('inf') if r['threshold'] is None else r['threshold']
    benefit=scores>threshold;u=seal['uncertainty'];uth=float('inf') if u['threshold'] is None else u['threshold']
    rng=random.Random(20260924);rand=np.array([rng.random()<r['development_oof_rate'] for _ in rows])
    matched=np.zeros(len(rows),dtype=bool);matched[random.Random(20260924).sample(range(len(rows)),int(sum(benefit)))]=True
    return {'never':np.zeros(len(rows),dtype=bool),'always':np.ones(len(rows),dtype=bool),'benefit':benefit,
      'uncertainty':np.array([row['features']['uncertainty']>uth for row in rows]),'random_development_rate':rand,
      'random_matched_realized_rate_diagnostic':matched,'hindsight_oracle_diagnostic':np.array([row['gain']>0 for row in rows])},scores

def analyze():
    verify_freeze();completed=read(OUT/'completed.json')
    if not completed['complete']:
        write(OUT/'analysis_blocked.json',{'reason':'incomplete intended collection; no complete-case policy comparison','completion':completed});return
    seal=read(OUT/'router_seal.json')
    assert sha(OUT/'router_seal.json')==read(OUT/'router_seal.sha256.json')['sha256']
    manifest=read('data/manifest_v6.json');dev=outcome_rows(manifest,'development');test=outcome_rows(manifest,'test')
    assert digest(dev)==seal['development_rows_sha256']
    write(OUT/'outcomes.json',dev+test);masks,scores=policy_masks(test,seal);groups=[r['system_group'] for r in test]
    policies=[];case_rows=[]
    for name,mask in masks.items():
        losses=np.array([r['llm_loss'] if m else r['classical_loss'] for r,m in zip(test,mask)])
        harms=sum(bool(m and r['gain']<-.02) for r,m in zip(test,mask));missed=sum(bool(not m and r['gain']>.02) for r,m in zip(test,mask))
        def usage(field):return None if any(r[field] is None for r,m in zip(test,mask) if m) else sum(r[field] for r,m in zip(test,mask) if m)
        times=[]
        for r,m,l in zip(test,mask,losses):
            k=r['dataset']+'_'+str(r['seed']);p=read(OUT/'prefixes'/f'{k}.json');a=read(OUT/'classical'/f'{k}.json');b=read(OUT/'paired'/f'{k}.json')
            seconds=p['prefix_seconds']+(b['branch_seconds'] if m else a['arms']['centroid_nominal']['branch_seconds'])
            times.append(seconds);case_rows.append({'policy':name,'dataset':r['dataset'],'seed':r['seed'],'escalated':bool(m),'loss':float(l),'estimated_deployment_seconds_excluding_load_fit':seconds})
        policies.append({'policy':name,'group_mean_loss':group_mean(losses,groups),'escalations':int(sum(mask)),'cases':len(test),
          'escalation_rate':group_mean(mask,groups),'missed_material_benefits':missed,'harmful_escalations':harms,
          'estimated_deployment_objective_accesses':20*len(test),'estimated_deployment_requests':int(sum(mask)),
          'selected_observed_input_tokens':usage('input_tokens'),'selected_observed_output_tokens':usage('output_tokens'),
          'estimated_deployment_seconds_excluding_load_fit':sum(times),
          'nondeployable':name.endswith('_diagnostic')})
    curves=[]
    for threshold in GRID:
        mask=scores>threshold;l=[r['llm_loss'] if m else r['classical_loss'] for r,m in zip(test,mask)]
        curves.append({'threshold':None if np.isinf(threshold) else threshold,'group_mean_loss':group_mean(l,groups),'escalation_rate':group_mean(mask,groups),'role':'descriptive frozen grid, no test selection'})
    systems=[]
    for group in sorted({r['system_group'] for r in dev+test}):
        rs=[r for r in dev+test if r['system_group']==group]
        systems.append({'system_group':group,'split':rs[0]['split'],'n':len(rs),**{k:float(np.mean([r[k] for r in rs])) for k in ['classical_loss','llm_loss','projection_loss','random_loss']},
          'material_help':sum(r['gain']>.02 for r in rs),'material_harm':sum(r['gain']<-.02 for r in rs)})
    req=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl');events=[e for p in (OUT/'paired').glob('*.json') for e in read(p)['events']]
    cost={'actual_objective_acquisitions':len(lines(OUT/'acquisitions.jsonl')),'actual_request_attempts':len(starts),
      'synthetic_format_attempts':sum(r['namespace']=='synthetic_real_inference_v6' for r in starts),'measured_pair_attempts':sum(r['namespace']=='measured_v6' for r in starts),
      'observed_input_tokens':sum(r['input_tokens'] for r in req) if all(r['input_tokens'] is not None for r in req) else None,
      'observed_output_tokens':sum(r['output_tokens'] for r in req) if all(r['output_tokens'] is not None for r in req) else None,
      'request_wall_seconds':sum(r['wall_seconds'] for r in req),'model_startup_seconds':read(OUT/'model_runtime.json')['startup_wall_seconds'],
      'development_fit_seconds':seal['benefit']['fit_seconds'],'external_spend_usd':0,
      'projection_events':sum(e.get('projected',False) for e in events),'duplicate_events':sum(e.get('duplicate',False) for e in events),
      'collision_events':sum(e.get('collision',False) for e in events),'fallback_events':sum(e.get('fallback',False) for e in events),'proposal_denominator':len(events),
      'scope':'actual collection; not policy deployment. Synthetic inference included, synthetic objective values excluded.'}
    summary={'scope':manifest['scope'],'systems':systems,'held_out_policies':policies,'frozen_threshold_curve':curves,'collection_cost':cost,
      'generalization_evidence':'insufficient: only three development and three held-out software families; no significance claim',
      'runtime_ledger_at_analysis':read('artifacts/resource_ledger_v2.json')}
    write(OUT/'summary.json',summary)
    for name,rows in [('system_summary',systems),('policies',policies),('policy_cases',case_rows)]:
        with (OUT/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.6))
    held=[s for s in systems if s['split']=='test'];positions=np.arange(len(held))
    for offset,field,label in [(-.27,'random_loss','Random'),(-.09,'classical_loss','Classical'),(.09,'llm_loss','Local LLM'),(.27,'projection_loss','Uniform projection')]:
        axes[0].bar(positions+offset,[s[field] for s in held],.18,label=label)
    axes[0].set_xticks(positions,[s['system_group'] for s in held],rotation=15);axes[0].set_ylabel('Mean normalized loss (lower better)');axes[0].legend(fontsize=8)
    for p in policies:
        label={'random_development_rate':'Random rate','random_matched_realized_rate_diagnostic':'Matched random*','hindsight_oracle_diagnostic':'Oracle*'}.get(p['policy'],p['policy'].capitalize())
        axes[1].scatter(p['escalation_rate'],p['group_mean_loss']);axes[1].annotate(label,(p['escalation_rate'],p['group_mean_loss']),xytext=(4,5),textcoords='offset points',fontsize=7)
    axes[1].set_xlabel('Fraction escalated');axes[1].set_ylabel('Held-out group mean loss');axes[1].set_xlim(-.05,1.22)
    fig.suptitle('V6 exploratory smoke: 3 held-out families × 5 seeds; * diagnostic only',fontsize=11);fig.tight_layout()
    fig.savefig(OUT/'quality_cost.png',dpi=180);fig.savefig(OUT/'quality_cost.svg');plt.close(fig)
    print('Analysis saved:',len(dev),'development,',len(test),'test cases')
    print(__import__('json').dumps(summary,indent=2))

if __name__=='__main__':
    with Resources(load_config('configs/followup_v3.yaml'),'artifacts/resource_ledger_v2.json') as r:r.check();analyze();r.check()
