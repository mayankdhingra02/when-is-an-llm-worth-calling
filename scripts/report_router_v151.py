"""Deterministic full exploratory results, including nonwinning variants."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'results/v151_router';A=ROOT/'artifacts/study_v151'
def main():
 d=json.loads((O/'comparison.json').read_text());folds=json.loads((O/'folds.json').read_text());runtime=json.loads((A/'runtime.json').read_text());models=['smollm3_3b','qwen3_8b']
 lines=['# V151: rare-benefit prediction and related-system sensitivity','', '**Exploratory analysis of70existing real paired cases/model; no new LLM calls or acquired objectives.** The fixed candidate models are original ridge, richer18-feature ridge, depth2tree and RBFkernel ridge. Nested whole-group folds fit preprocessing, models, thresholds and model selection on development only. Prior exposure still prevents a confirmatory claim. All variants appear below.','', 'V149 was rejected by independent replay because Spark/Hadoop short case names collided. Its invalid outputs are retained but excluded from all tables here. V151 qualifies case keys by original engine family and adds a collision regression test before refreezing/rerunning the identical analysis. Historical experiments remain intact.','']
 for grouping,label in [('engine','Eight execution-engine groups'),('ecosystem','Seven groups: Spark and Hadoop merged')]:
  lines += ['## '+label,'','| Model / policy | Calls /70 | Equal-group gain | Above matched random | Useful >1% | Harmful >1% | Joint useful | Missed useful |','|---|---:|---:|---:|---:|---:|---:|---:|']
  for m in models:
   for p,s in d['models'][grouping][m]['policies'].items():lines.append(f"| {m} / {p} | {s['calls']} | {100*s['family_mean_gain']:+.5f}% | {100*s['gain_above_random']:+.5f}% | {s['useful']} | {s['harmful']} | {s['joint_useful']} | {s['missed']} |")
 lines += ['', 'The selected predictor uses inner development utility to choose among allfourfixed models; the table also retains each separate predictor and its development80th-percentile policy. Matched random is a retrospective expected score at the same held-group call count; no outcome informs its selection. Never-call has zero gain by definition. A positive difference from random can still be a loss against never-call.','',
 'With eight engine groups, SmolLM selected one useful Spark call: equal-group gain+0.00754%, above matched random+0.00809percentage points. It missed9/10useful opportunities and selected no joint >1%win over both sequential and adaptive. Qwen selected no calls. When Spark/Hadoop are one ecosystem group, both selected predictors choose zero calls. This small apparent success is therefore insufficient evidence of independent-system transfer or a practically useful general router. It must not be promoted to a successful method by selecting only the favorable grouping.','',
 '| Grouping / model | Oracle equal-group gain | Useful-opportunity groups | Joint-opportunity groups |','|---|---:|---|---|']
 for grouping in ['engine','ecosystem']:
  for m in models:
   s=d['models'][grouping][m];lines.append(f"| {grouping} / {m} | {100*s['oracle_family_gain']:.5f}% | {', '.join(s['opportunity_groups'])} | {', '.join(s['joint_opportunity_groups'])} |")
 lines += ['', 'Oracle is diagnostic hindsight, not deployable. Per-family ranking AUCs, all inner/outer training memberships and fitted coefficients/trees, threshold grids, prediction scores, decisions, exact selected case IDs, pooled means, leave-one-group aggregate ranges, usage/fallback counters and fixed random selections are stored in folds.json/comparison.json. AUC is undefined in one-class families; those remain null, not zero or silently excluded cases.','',
 f"Analysis consumed{runtime['wall_seconds']:.3f}seconds/{runtime['cap_seconds']}second cap. Selected-token/time fields reuse observed historical costs as counterfactual deployment estimates; original data-collection costs remain paid in the project ledger. One historical interrupted SmolLM request stays as fallback with unknown usage. No new native run, request, token or acquisition is caused by this analysis.", '',
 'Independent replay verifies140cases,30outer folds, ridge/RBF fits via augmented least-squares algebra, tree split optimality, group exclusions, calibration, decisions and primary aggregates, and rejects four in-memory semantic mutations. Saved normalization is authenticated against independently recomputed moments and then used at exact tree split boundaries to prevent verifier-only roundoff from changing a branch. The initial verifier boundary/quantile diagnostic logs are retained. Figures and this report are deterministic.','',
 'Limitations: onlysevenecosystems, most practical wins in the shared Spark/Hadoop ecosystem, heterogeneous representations/targets, prior inspection and repeated seeds, tiny gain at one selected case, and no prospective validation of these new predictors. The practical margin remains1%per case; it is not an aggregate non-inferiority margin. No population confidence/significance, equivalence, novelty or journal acceptance claim follows. The native Memcached feasibility check is separate and does not enter these aggregates.']
 (ROOT/'reports/router_v151.md').write_text('\n'.join(lines)+'\n')
 import matplotlib
 matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v151'
 import matplotlib.pyplot as plt
 policies=['always','ridge_original','ridge_extended','tree_extended','rbf_extended','selected_predictor','uncertainty','ridge_original_q80','tree_extended_q80','uncertainty_q80']
 labels=['Always','Original ridge','Extended ridge','Shallow tree','RBF ridge','Selected predictor','Uncertainty','Original ridge q80','Tree q80','Uncertainty q80']
 fig,axs=plt.subplots(2,2,figsize=(12,9),layout='constrained')
 for i,grouping in enumerate(['engine','ecosystem']):
  for j,m in enumerate(models):
   ax=axs[i,j];ss=d['models'][grouping][m]['policies'];vals=[100*ss[p]['family_mean_gain'] for p in policies];ax.barh(range(len(policies)),vals,color='#336b87')
   ax.scatter([100*ss[p]['random_expected_gain'] for p in policies],range(len(policies)),color='#ca7736',s=18,label='Matched random expectation',zorder=3)
   ax.axvline(0,color='black',lw=.7);ax.set_yticks(range(len(policies)),labels if j==0 else []);ax.invert_yaxis();ax.set_xlim(-5.7,.3);ax.grid(axis='x',alpha=.2);ax.set_title(m+' • '+('8 engine groups' if i==0 else '7 ecosystem groups'));ax.set_xlabel('Equal-group gain vs sequential (%)')
 axs[0,0].legend(fontsize=8,loc='lower left');fig.suptitle('Exploratory nested routing: grouping changes the apparent success\n70 real historical cases/model; only prefix features; no new inference')
 fig.savefig(O/'policies.png',dpi=150);fig.savefig(O/'policies.svg',metadata={'Date':None});plt.close(fig)
 print('Saved V151 full report and figures')
if __name__=='__main__':main()
