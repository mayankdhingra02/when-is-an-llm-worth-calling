"""Post-outcome representation diagnostic, expressly not a new policy or tuning."""
import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v168';O=ROOT/'results/v168_native'
def read(p):return json.loads(p.read_text())
def main():
 out=[]
 for j in read(A/'jobs.json'):
  p=read(ROOT/j['prefix']);base=min(y[0] for y in p['labels'])
  for arm in ['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal','smollm3_3b','qwen3_8b']:
   r=read(O/'search'/f"{j['key']}__{arm}.json");s=r['state'];best=min(range(17),key=lambda i:s['labels'][i][0]);diag=r['projection'];out.append({'case':j['key'],'engine':j['engine'],'arm':arm,'selected_in_prefix':best<10,'best_search_relative_improvement':(base-s['labels'][best][0])/base,'proposed_count':len(diag),'evaluated_projected_count':sum(d['distance']>0 for d in diag[:7]),'evaluated_duplicate_count':sum(d['duplicate_proposal'] for d in diag[:7]),'evaluated_prefix_matching_count':sum(d['matches_prefix'] for d in diag[:7])})
 summary=[]
 for engine in ['polars','xgboost']:
  for arm in ['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal','smollm3_3b','qwen3_8b']:
   rs=[r for r in out if r['engine']==engine and r['arm']==arm];summary.append({'engine':engine,'arm':arm,'prefix_selected_cases':sum(r['selected_in_prefix'] for r in rs),'cases':len(rs),'search_mean_relative_improvement':statistics.mean(r['best_search_relative_improvement'] for r in rs),'evaluated_proposals':35 if rs[0]['proposed_count'] else 0,'projected':sum(r['evaluated_projected_count'] for r in rs),'duplicate':sum(r['evaluated_duplicate_count'] for r in rs),'prefix_match':sum(r['evaluated_prefix_matching_count'] for r in rs)})
 result={'scope':'Post-outcome exploratory mechanism audit; noisy search minima are not fresh validation or proof of global optimality; no calls/acquisitions or policy changes','rows':out,'summary':summary};(O/'representation_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
