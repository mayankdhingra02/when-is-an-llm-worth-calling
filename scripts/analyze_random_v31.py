"""Separate evaluator: random-arm replay and exact finite-pool references."""
import argparse, csv, hashlib, json, math, os, random, sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read, write, lines
from escalation.selection_null_v9 import uniform_minimum_distribution, event_probability
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config, require
from verify_reproduction_v26 import observe
OUT=Path('results/v31_random')
MODES=('random_full','random_shortlist')
BASES=('full_classical','static_rank','centroid_shortlist','batch_3nn','sequential_3nn')

def source(spec):
    features=[];targets=[];source_lines=[];seen=set()
    with Path(spec['path']).open(newline='') as f:
        for number,row in enumerate(csv.DictReader(f,delimiter=spec['delimiter']),2):
            if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
            x=tuple(float(row[k]) for k in spec['feature_names'])
            if x in seen:continue
            seen.add(x);features.append(x);targets.append(float(row[spec['primary_objective']]));source_lines.append(number)
    require(len(targets)==spec['rows'] and all(math.isfinite(v) and v>0 for v in targets),'Source domain')
    return targets,source_lines

def calculate():
    freeze=read('reports/protocol_v31_random.freeze.json')
    for name,h in freeze['sha256'].items():require(hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,'Changed input: '+name)
    manifest=read('data/manifest_v30.json');progress=read(OUT/'progress.json');journal=lines(OUT/'acquisitions.jsonl')
    require(progress['complete'] and len(progress['arms'])==20 and len(journal)==200,'Completed denominator')
    require(all(e['at']>freeze['created_at'] for e in journal),'Frozen before acquisitions')
    cases=[];pairs=[];distributions=[]
    for spec in manifest['datasets']:
        targets,source_lines=source(spec);lo,hi=min(targets),max(targets)
        for seed in manifest['seeds']:
            key=f"{spec['id']}_{seed}";p=read(f'results/v30_transfer/prefixes/{key}.json');incumbent=min(v[0] for v in p['state']['labels'])
            bases={mode:read(f'results/v30_transfer/arms/{key}_{mode}.json') for mode in BASES}
            for mode in MODES:
                pool=sorted(set(p['state']['order'])-set(p['state']['ids'])) if mode=='random_full' else sorted(p['pool']['ranked'])
                entropy=hashlib.sha256(f"v31|{spec['id']}|{seed}|{mode}".encode()).hexdigest()
                selected=random.Random(int(entropy,16)).sample(pool,10)
                arm=read(OUT/'arms'/f'{key}_{mode}.json');state=json.loads(json.dumps(p['state']))
                events=[e for e in journal if e['dataset']==spec['id'] and e['seed']==seed and e['arm']==mode]
                require(len(events)==arm['actual_new_accesses']==10 and arm['logical_evaluations']==20,'Per-arm budget')
                require(arm['selection']['selected']==selected and arm['selection']['seed_sha256']==entropy,'Independent seeded selection')
                require(arm['prefix_hash']==p['prefix_hash'],'Shared prefix hash')
                for row,event in zip(selected,events):
                    require(event['row_id']==row and event['source_line']==source_lines[row] and float(event['raw_target'])==targets[row],'Source journal')
                    observe(state,row,targets[row],'-')
                require(state==arm['state'] and len(set(state['ids']))==20,'Independent final state')
                target=min(targets[i] for i in state['ids']);loss=(target-lo)/(hi-lo)
                dist=uniform_minimum_distribution([targets[i] for i in pool],incumbent,10)
                expected=dist['expected_loss'];expected_loss=(expected-lo)/(hi-lo)
                identity={'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'arm':mode}
                cases.append({**identity,'sampled_target':target,'sampled_loss':loss,'exact_expected_target':expected,
                    'exact_expected_loss':expected_loss,'pool_size':len(pool),'branch_seconds':arm['branch_seconds']})
                distributions.append({**identity,'namespace':'retrospective_exact_reference_not_measured_arm',**dist})
                for base,b in bases.items():
                    require(b['state']['labels']==[[targets[i]] for i in b['state']['ids']],'Historical source labels')
                    baseline=min(targets[i] for i in b['state']['ids']);base_loss=(baseline-lo)/(hi-lo)
                    pairs.append({**identity,'comparator':base,'sampled_normalized_gain':base_loss-loss,
                        'sampled_relative_gain':(baseline-target)/baseline,'exact_expected_normalized_gain':base_loss-expected_loss,
                        'exact_expected_relative_gain':(baseline-expected)/baseline,
                        'probability_random_strictly_better':event_probability(dist,lambda y:y<baseline),
                        'probability_random_no_worse':event_probability(dist,lambda y:y<=baseline)})
    groups=[];comparisons=[]
    for mode in MODES:
        for group in sorted({r['system_group'] for r in cases}):
            rows=[r for r in cases if r['arm']==mode and r['system_group']==group]
            groups.append({'system_group':group,'arm':mode,**{k:mean(r[k] for r in rows) for k in ('sampled_loss','exact_expected_loss')}})
        for base in BASES:
            family=[]
            metrics=('sampled_normalized_gain','sampled_relative_gain','exact_expected_normalized_gain','exact_expected_relative_gain','probability_random_strictly_better','probability_random_no_worse')
            rows=[r for r in pairs if r['arm']==mode and r['comparator']==base]
            for group in sorted({r['system_group'] for r in rows}):
                family.append({'system_group':group,**{k:mean(r[k] for r in rows if r['system_group']==group) for k in metrics}})
            comparisons.append({'arm':mode,'comparator':base,'families':family,**{k:mean(g[k] for g in family) for k in metrics},
                'sampled_wins':sum(r['sampled_normalized_gain']>1e-12 for r in rows),
                'sampled_ties':sum(abs(r['sampled_normalized_gain'])<=1e-12 for r in rows),
                'sampled_losses':sum(r['sampled_normalized_gain']< -1e-12 for r in rows)})
    return {'scope':'Exploratory random controls after V30; exact references are evaluator mathematics, not LLM or measured arms',
        'complete':True,'cases':cases,'paired_gains':pairs,'families':groups,'comparisons':comparisons,
        'new_objective_acquisitions':200,'new_model_calls':0,'logical_evaluations':400,'intended_arms':20,
        'exact_distributions':distributions}

def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    old=read('results/v30_transfer/summary.json');fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,group in zip(axes,old['families']):
        refs=[next(r for r in result['families'] if r['system_group']==group['system_group'] and r['arm']==m) for m in MODES]
        values=[group['static_rank'],group['centroid_shortlist'],group['sequential_3nn'],refs[0]['exact_expected_loss'],refs[1]['exact_expected_loss']]
        bars=ax.bar(range(5),values,color=['#80909c','#597787','#176b93','#c3a96b','#a98943'])
        for b in bars[-2:]:b.set_hatch('//')
        ax.set_xticks(range(5),['Static\nrank','Shortlist\ncentroid','Sequential\n3NN','Full random\nexpectation','Shortlist random\nexpectation'],fontsize=8)
        ax.set_title(group['system_group']);ax.set_ylabel('Normalized loss (lower is better)')
    fig.suptitle('V31: exact random references against observed classical outcomes')
    fig.text(.5,.02,'Hatched bars are conditional expectations, not measured arms. Two exposed families × five seeds. Separate panel scales.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.07,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'comparison.{ext}',dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved result differs');print('20 random arms,200 acquisitions,all source states and exact references replayed.');return
    require(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'));before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check();result=calculate();write(OUT/'summary.json',result)
        for name,rows in [('cases',result['cases']),('paired_gains',result['paired_gains'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(result);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v31/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_objective_acquisitions':0,'new_model_calls':0,'active_since':after['active_since']})
    print(json.dumps({'families':result['families'],'comparisons':result['comparisons']},indent=2))

if __name__=='__main__':main()
