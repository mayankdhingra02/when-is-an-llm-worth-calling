"""Deterministic report and scientific figure from the completed nested analysis."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/study_v147';OUT=ROOT/'results/v147_router'
def main():
    d=json.loads((OUT/'comparison.json').read_text());folds=json.loads((OUT/'folds.json').read_text());rows=json.loads((ART/'inputs.json').read_text())['rows']
    models=['smollm3_3b','qwen3_8b'];policies=['never','always','benefit_all','benefit_no_cardinality','benefit_trajectory','uncertainty','benefit_80pct','uncertainty_80pct']
    lines=['# V147: does benefit prediction transfer across the paired-model cohort?','',
           '**Exploratory nested evaluation of seven previously exposed software families.** All 55 paired cases per model are included; Spark contributes 25 cases but only one-seventh of the primary aggregate. No new model call or objective acquisition occurred. One historical interrupted SmolLM call retains its classical fallback. This analysis does not create a fresh holdout or establish journal readiness.','',
           'Each outer fold holds out a whole family. Six development families supply inner group folds, all standardization, ridge fitting and threshold selection. The primary ridge uses the seven pre-decision V132 features. Every declared ablation is shown. Adaptive outcomes never select a threshold. All-feature and uncertainty 80th-percentile policies use development quantiles and are fixed diagnostics against trivial no-call solutions, not tuned test rates.','',
           '| Model / policy | Calls /55 | Family gain vs sequential | Gain above matched random | >1% harmful calls | Missed >1% wins |','|---|---:|---:|---:|---:|---:|']
    for m in models:
        for p in policies:
            s=d['models'][m]['policies'][p]
            lines.append(f"| {m} / {p} | {s['calls']} | {100*s['family_mean_gain']:+.4f}% | {100*s['gain_above_matched_random']:+.4f}% | {s['harmful_calls']} | {s['missed_useful_calls']} |")
    lines += ['', 'Random reference matches each policy’s realized call count **within each family** and samples without observing outcomes. Its analytic expected gain is subtracted above; this is a retrospective matched-rate diagnostic. 10,000 fixed-seed random draws supply reference bands in comparison.json. These bands describe random selection on these saved cases, not population uncertainty or a confirmatory significance test. Call rate and pooled-case means are also saved; primary results give families equal weight.', '',
              '| Model / family | Primary benefit calls / n | Primary gain | Always gain | Matched-random expectation |','|---|---:|---:|---:|---:|']
    for m in models:
        for x in d['models'][m]['policies']['benefit_all']['groups']:
            a=next(z for z in d['models'][m]['policies']['always']['groups'] if z['group']==x['group'])
            lines.append(f"| {m} / {x['group']} | {x['calls']}/{x['n']} | {100*x['gain']:+.4f}% | {100*a['gain']:+.4f}% | {100*x['random_expected_gain']:+.4f}% |")
    lines+=['','## Headroom, support and strong-control checks','']
    for m in models:
        s=d['models'][m];p=s['policies']['benefit_all'];out_of_support=sum(bool(v) for f in folds[m] for v in f['variants']['all']['outside_training_range'].values())
        lines.append(f"{m}: {s['practical_opportunities']}/55 >1% opportunities against sequential in families {', '.join(s['groups_with_practical_opportunity'])}; {s['joint_practical_opportunities']}/55 exceed both sequential and adaptive by >1%. Hindsight family-mean gain {100*s['hindsight_oracle_family_mean_gain']:.4f}% is a non-deployable upper reference. Primary policy gain against adaptive {100*p['family_mean_gain_vs_adaptive']:+.4f}%; joint useful calls {p['joint_useful_calls']}. {out_of_support}/55 cases have at least one feature outside their outer-training min/max range. Primary aggregate after omitting each one family ranges from {100*p['leave_one_family_mean_range'][0]:+.4f}% to {100*p['leave_one_family_mean_range'][1]:+.4f}%; this is sensitivity, not a confidence interval.")
    lines+=['','Against adaptive, a no-call decision deploys the actual sequential arm and therefore can still lose to adaptive. Never-call is not silently replaced with a hindsight-best classical portfolio. Domain cardinality removal is motivated by the already observed Spark extrapolation; its result is an exposed-data ablation, not independent confirmation.','',
            '## Costs and reproducibility','',
            'New collection: zero requests, zero objective acquisitions, zero native executions. Historical cohort collection: 110 real generation starts, 109 complete responses and one interrupted request with unknown usage; 1,100 model-continuation acquisitions plus original prefixes and classical controls. Prior acquisition/request totals are unchanged. Raw provenance and collection costs stay in V141–V145; this is reuse, not free historical inference.', '']
    for m in models:
        rs=[r for r in rows if r['model']==m];known=sum(r['usage']['generated_tokens'] or 0 for r in rs);prefill=sum(r['usage']['prefill_tokens'] or 0 for r in rs);unknown=sum(r['usage']['generated_tokens'] is None for r in rs)
        lines.append(f"{m}: historical generated≥{known}, prefill≥{prefill} tokens; unknown-usage requests {unknown}. Hypothetical policy deployment calls equal the table counts and use B20 each. Per-family replayed request runtime and generated-token lower bounds are saved for selected branches. They exclude model startup/amortization and unknown interrupted runtime, and are evaluation quantities, never router inputs. No dollars or native-time savings inferred.")
    lines+=['','Commands:', '','```sh','.venv/bin/python scripts/verify_router_v147.py','MPLCONFIGDIR=/tmp/mpl-v147 .venv/bin/python scripts/report_router_v147.py','```','',
            'The create-once fitting command was `scripts/router_v147.py run`; its input/protocol/source hashes are in artifacts/study_v147/freeze.json and runtime is in runtime.json. Full inner/outer models, transformations, calibration grids, support flags and decisions: results/v147_router/folds.json. Per-case paired inputs: artifacts/study_v147/inputs.json. Independent replay uses augmented least squares, separately checks prefix features and raw paired targets, and rejects semantic mutations.','',
            '## Limits and next action','',
            'Seven groups, two fixed quantized models, heterogeneous nominal/numeric proposal representations, reused classical prefixes and exposed outcomes limit generalization. The family-held-out mechanics prevent direct fold leakage; they do not undo earlier human/agent inspection or provide a prospective replication. Source correctness/noise/contamination limitations and the Spark missing-data amendment persist. Repeated seeds/workloads are dependent. No classifier accuracy, non-inferiority, equivalence or journal-quartile claim is justified by this table.','',
            'The next priority is an outcome-unexposed, source-validated configuration cohort with enough independent families, then one frozen controller test. The V146 source audit excluded PTSS metric dictionaries, incomplete Cassandra trace exports and Hyrise’s 36-valid-setting scan partitions without relaxing admission to obtain more favorable evidence. A usable original per-configuration Cassandra outcome matrix is a concrete missing artifact; its current elite logs do not substitute for one.']
    (ROOT/'reports/router_v147.md').write_text('\n'.join(lines)+'\n')
    import matplotlib
    matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v147'
    import matplotlib.pyplot as plt
    labels=['Never','Always','Benefit: all','Benefit: no cardinality','Benefit: trajectory','Uncertainty','Benefit: dev q80','Uncertainty: dev q80']
    fig,axes=plt.subplots(1,2,figsize=(12,5.3),layout='constrained')
    for mi,m in enumerate(models):
        ax=axes[mi];vals=[100*d['models'][m]['policies'][p]['family_mean_gain'] for p in policies]
        ax.barh(range(len(policies)),vals,color='#346b91')
        for j,p in enumerate(policies):
            s=d['models'][m]['policies'][p];ax.plot(100*s['random_matched_expected_gain'],j,'o',color='#ce7d31',markersize=4)
        ax.axvline(0,color='black',lw=.7);ax.set_yticks(range(len(policies)),labels if mi==0 else []);ax.invert_yaxis();ax.set_xlabel('Equal-family mean gain vs sequential (%)');ax.set_title(m);ax.grid(axis='x',alpha=.2)
    axes[0].plot([],[],'o',color='#ce7d31',label='Matched random expectation');axes[0].legend(loc='lower left',fontsize=8)
    fig.suptitle('Exploratory nested family validation • 7 families, 55 cases/model\nAll Spark workloads and seeds stay in one fold; no new collection')
    fig.savefig(OUT/'policies.png',dpi=160);fig.savefig(OUT/'policies.svg',metadata={'Date':None});plt.close(fig)
    print('Saved reports/router_v147.md and results/v147_router/policies.{png,svg}')
if __name__=='__main__':main()
