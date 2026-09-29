"""Independent Decimal/source, combinatorial-survival and exhaustive checks."""
import bisect, csv, itertools, json, math, time
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];getcontext().prec=45
def read(p):return json.loads((ROOT/p).read_text(),parse_float=Decimal)
def close(a,b):
    if abs(a-b)>max(Decimal('1e-11'),abs(a)*Decimal('1e-12')):raise ValueError(f'{a} != {b}')
def choose(n,k):return math.comb(n,k) if n>=k else 0
def avg(xs):return sum(xs,Decimal(0))/len(xs)

def main():
    start=time.perf_counter();result=read('results/v31_random/summary.json');manifest=read('data/manifest_v30.json')
    all_pairs=[];exhaustive=0;source_checks=0;supports=0;ceilings=[]
    for spec in manifest['datasets']:
        targets=[];seen=set()
        with (ROOT/spec['path']).open(newline='') as stream:
            for row in csv.DictReader(stream,delimiter=spec['delimiter']):
                if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
                x=tuple(Decimal(row[k]) for k in spec['feature_names'])
                if x in seen:continue
                seen.add(x);targets.append(Decimal(row[spec['primary_objective']]))
        lo,hi=min(targets),max(targets)
        for seed in manifest['seeds']:
            key=f"{spec['id']}_{seed}";p=read(f'results/v30_transfer/prefixes/{key}.json');incumbent=min(v[0] for v in p['state']['labels'])
            for mode in ('random_full','random_shortlist'):
                arm=read(f'results/v31_random/arms/{key}_{mode}.json');state=arm['state']
                assert state['labels']==[[targets[i]] for i in state['ids']];source_checks+=20
                target=min(targets[i] for i in state['ids']);loss=(target-lo)/(hi-lo)
                pool=sorted(set(p['state']['order'])-set(p['state']['ids'])) if mode=='random_full' else p['pool']['ranked']
                values=sorted(min(incumbent,targets[i]) for i in pool);total=choose(len(values),10)
                counts={}
                # Survival difference handles ties and incumbent clipping without
                # the evaluator's minimum-index enumeration formula.
                for value in sorted(set(values)):
                    ge=len(values)-bisect.bisect_left(values,value);gt=len(values)-bisect.bisect_right(values,value)
                    count=choose(ge,10)-choose(gt,10)
                    if count:counts[value]=count
                assert sum(counts.values())==total
                saved=next(r for r in result['exact_distributions'] if r['dataset']==spec['id'] and r['seed']==seed and r['arm']==mode)
                assert {r['loss']:r['subsets'] for r in saved['support']}==counts and saved['subsets']==total
                supports+=len(counts)
                if mode=='random_shortlist':
                    brute=Counter(min(subset) for subset in itertools.combinations(values,10))
                    assert brute==counts and sum(brute.values())==184756;exhaustive+=184756
                expected=sum(v*n for v,n in counts.items())/total;close(expected,saved['expected_loss'])
                case=next(r for r in result['cases'] if r['dataset']==spec['id'] and r['seed']==seed and r['arm']==mode)
                for field,value in [('sampled_target',target),('sampled_loss',loss),('exact_expected_target',expected),('exact_expected_loss',(expected-lo)/(hi-lo))]:close(value,case[field])
                for pair in [r for r in result['paired_gains'] if r['dataset']==spec['id'] and r['seed']==seed and r['arm']==mode]:
                    b=read(f"results/v30_transfer/arms/{key}_{pair['comparator']}.json")['state'];baseline=min(targets[i] for i in b['ids'])
                    assert b['labels']==[[targets[i]] for i in b['ids']]
                    if mode=='random_shortlist' and pair['comparator']=='centroid_shortlist':
                        best=min(incumbent,min(targets[i] for i in pool))
                        assert best==min(counts)
                        ceilings.append({'dataset':spec['id'],'seed':seed,'baseline_target':str(baseline),
                            'best_attainable_within_prefix_and_shortlist':str(best),'zero_headroom':best==baseline,
                            'relative_hindsight_ceiling':str((baseline-best)/baseline)})
                    checked={**{k:pair[k] for k in ('dataset','system_group','seed','arm','comparator')},
                        'sampled_normalized_gain':(baseline-target)/(hi-lo),'sampled_relative_gain':(baseline-target)/baseline,
                        'exact_expected_normalized_gain':(baseline-expected)/(hi-lo),'exact_expected_relative_gain':(baseline-expected)/baseline,
                        'probability_random_strictly_better':Decimal(sum(n for v,n in counts.items() if v<baseline))/total,
                        'probability_random_no_worse':Decimal(sum(n for v,n in counts.items() if v<=baseline))/total}
                    for field in list(checked)[5:]:close(checked[field],pair[field])
                    all_pairs.append(checked)
    metrics=('sampled_normalized_gain','sampled_relative_gain','exact_expected_normalized_gain','exact_expected_relative_gain','probability_random_strictly_better','probability_random_no_worse')
    for summary in result['comparisons']:
        rows=[r for r in all_pairs if r['arm']==summary['arm'] and r['comparator']==summary['comparator']]
        for metric in metrics:
            means=[]
            for family in summary['families']:
                m=avg([r[metric] for r in rows if r['system_group']==family['system_group']]);close(m,family[metric]);means.append(m)
            close(avg(means),summary[metric])
        vals=[r['sampled_normalized_gain'] for r in rows]
        assert summary['sampled_wins']==sum(v>Decimal('1e-12') for v in vals)
        assert summary['sampled_ties']==sum(abs(v)<=Decimal('1e-12') for v in vals)
        assert summary['sampled_losses']==sum(v<Decimal('-1e-12') for v in vals)
    print(json.dumps({'verified':True,'source_label_checks_including_reused_prefixes':source_checks,
        'exact_distributions_checked':20,'support_counts_checked':supports,'shortlist_subsets_exhaustively_verified':exhaustive,
        'paired_metric_checks':len(all_pairs)*6,'family_metric_checks':120,'aggregate_metric_checks':60,'win_tie_loss_checks':30,
        'post_hoc_ceiling_interpretation_not_deployable':ceilings,'zero_shortlist_headroom_cases':sum(c['zero_headroom'] for c in ceilings),
        'verification_seconds':time.perf_counter()-start,'new_objective_acquisitions':0,'new_model_calls':0},indent=2))

if __name__=='__main__':main()
