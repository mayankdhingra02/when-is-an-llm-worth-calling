"""Evaluate exact random subset distributions from acquired V41 journals only."""
import hashlib,os,sys,time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines,now
from escalation.resources import Resources
from escalation.transfer_v41 import current_config
from escalation.selection_reference_v42 import best,gain,random_distribution,compare

def main():
    out=Path('results/v42_selection_reference')
    if out.exists():raise ValueError('Preserve post-hoc result')
    for p,h in read('reports/protocol_v42_selection_reference.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Changed frozen V42input')
    before=read('artifacts/resource_ledger_v2.json');case_rows=[];model_rows=[];ceilings=[]
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        deadline=time.monotonic()+30;resource.check();observed=defaultdict(dict)
        for path in ('results/v41_transfer/acquisitions.jsonl','results/v41_models/acquisitions.jsonl'):
            for e in lines(path):
                key=(e['dataset'],e['seed']);value=F(e['raw_target']);i=e['row_id']
                if value<=0 or (i in observed[key] and observed[key][i]!=value):raise ValueError('Invalid/conflicting acquired outcome')
                observed[key][i]=value
        m=read('data/manifest_v41.json')
        for spec in m['datasets']:
            for seed in m['seeds']:
                resource.check()
                if time.monotonic()>deadline:raise RuntimeError('30-second analytic stage bound')
                key=f"{spec['id']}_{seed}";p=read(f'results/v41_transfer/prefixes/{key}.json');values=observed[(spec['id'],seed)]
                ids=p['pool']['ranked'];prefix=p['state']['ids'];direction=spec['direction']
                if len(ids)!=20 or len(set(ids))!=20 or len(prefix)!=10 or set(ids)&set(prefix):raise ValueError('Wrong candidate/prefix budget')
                if not set(ids+prefix)<=set(values):raise ValueError('Incomplete observed coverage; do not impute/drop')
                prefix_best=best([values[i] for i in prefix],direction);dist=random_distribution([values[i] for i in ids],prefix_best,direction)
                case={'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'direction':direction,
                    'candidate_ids':ids,'acquired_candidate_targets':[str(values[i]) for i in ids],'prefix_best':str(prefix_best),
                    'distribution':[{'target':str(v),'subsets':count} for v,count in sorted(dist['counts'].items())],
                    'subset_denominator':dist['denominator'],'shortlist_ceiling':str(dist['ceiling'])}
                case_rows.append(case)
                for size in ('0.5','1.5'):
                    arm=read(f'results/v41_models/{size}/arms/{key}.json');state=arm['state']
                    if state['ids'][:10]!=prefix or len(state['ids'])!=20 or not set(state['ids'][10:])<=set(ids):raise ValueError('Actual arm outside paired shortlist')
                    if any(float(values[i])!=y[0] for i,y in zip(state['ids'],state['labels'])):raise ValueError('Actual acquired model state mismatch')
                    target=best([values[i] for i in state['ids']],direction);result=compare(dist,target,direction)
                    model_rows.append({'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'model_size':size,
                        'model_best':str(target),'attains_shortlist_ceiling':target==dist['ceiling'],
                        **{k:float(v) for k,v in result.items()},'exact':{k:str(v) for k,v in result.items()}})
                for mode in ('batch_3nn','full_sequential_3nn'):
                    arm=read(f'results/v41_transfer/arms/{key}_{mode}.json');target=best([values[i] for i in arm['state']['ids']],direction)
                    effect=gain(target,dist['ceiling'],direction)
                    ceilings.append({'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'reference':mode,
                        'reference_best':str(target),'ceiling_best':str(dist['ceiling']),'ceiling_gain':float(effect),'exact_ceiling_gain':str(effect),
                        'ceiling_strictly_better':effect>0,'ceiling_equal':effect==0,'ceiling_worse':effect<0})
        families=sorted({s['system_group'] for s in model_rows});model_summary=[];ceiling_summary=[]
        for size in ('0.5','1.5'):
            rows=[r for r in model_rows if r['model_size']==size]
            by_family={g:sum(F(r['exact']['expected_relative_gain']) for r in rows if r['system_group']==g)/5 for g in families}
            model_summary.append({'model_size':size,'cases':len(rows),'families':len(families),
                'equal_family_expected_gain_vs_uniform':float(sum(by_family.values())/len(families)),
                'family_expected_gain_vs_uniform':{g:float(v) for g,v in by_family.items()},
                'model_attains_shortlist_ceiling':sum(r['attains_shortlist_ceiling'] for r in rows),
                'mean_probability_random_matches_or_beats':float(sum(F(r['exact']['probability_random_matches_or_beats']) for r in rows)/len(rows))})
        for mode in ('batch_3nn','full_sequential_3nn'):
            rows=[r for r in ceilings if r['reference']==mode]
            ceiling_summary.append({'reference':mode,'cases':len(rows),'can_strictly_improve':sum(r['ceiling_strictly_better'] for r in rows),
                'equal':sum(r['ceiling_equal'] for r in rows),'strictly_worse':sum(r['ceiling_worse'] for r in rows),
                'mean_best_possible_gain':float(sum(F(r['exact_ceiling_gain']) for r in rows)/len(rows))})
        write(out/'summary.json',{'at':now(),'scope':'Post-hoc exact conditional random-selection and shortlist-ceiling diagnostic, not a new experiment or policy',
            'cases':case_rows,'model_comparisons':model_rows,'ceiling_comparisons':ceilings,'model_summary':model_summary,
            'ceiling_summary':ceiling_summary,'actual_new_model_calls':0,'actual_new_acquisitions':0,'actual_new_physical_trials':0,
            'logical_random_arm_evaluations':20,'hypothetical_subsets_per_case':184756,'hypothetical_subsets_not_executed_as_experiments':5542680})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v42/analytic_accounting.json',{'seconds':after['experiment_seconds']-before['experiment_seconds'],'new_model_calls':0,'new_acquisitions':0})
    print(__import__('json').dumps({'models':model_summary,'ceilings':ceiling_summary},indent=2))
if __name__=='__main__':main()
