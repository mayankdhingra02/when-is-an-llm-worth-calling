"""Post-hoc, acquisition-free sample/ranking stability diagnostics."""
import json,statistics
from collect_smollm_v47 import ROOT,read,write
from surrogate_v124 import IDS,SEEDS,parse,predictions,choose

def main():
 raw=[json.loads(x) for x in (ROOT/'results/v124_surrogate/responses.jsonl').read_text().splitlines()];scores={};invalid=[]
 for r in raw:
  try:scores[r['key']]=parse(r['response'])
  except ValueError:invalid.append({'key':r['key'],'raw':r['response'].get('content'),'stop_type':r['response'].get('stop_type'),'tokens_predicted':r['response'].get('tokens_predicted')})
 rows=[]
 for j in read(ROOT/'artifacts/study_v124/cases.json'):
  key=j['key'];p=read(ROOT/j['prefix']);values={i:[scores[f'{key}_{i}_{s}'] for s in SEEDS if f'{key}_{i}_{s}' in scores] for i in IDS};complete=sum(len(v)==3 for v in values.values());accepted=all(len(v)>=2 for v in values.values());r={'key':key,'system_group':j['system_group'],'three_valid_candidates':complete,'accepted_family':accepted,'identical_samples_candidates':sum(len(v)>=2 and len(set(v))==1 for v in values.values()),'leave_one_seed_out':[]}
  if accepted:
   full=predictions(values,p);ids,_=choose(full,p,'ei');means=[x['mean'] for x in full.values()];ys=[x[0] for x in p['state']['labels']];r.update(predicted_means_range=[min(means),max(means)],acquired_performance_range=[min(ys),max(ys)],mean_prediction_range_over_acquired_range=None if max(ys)==min(ys) else (max(means)-min(means))/(max(ys)-min(ys)))
   for omitted in SEEDS:
    subset={i:[scores[f'{key}_{i}_{s}'] for s in SEEDS if s!=omitted and f'{key}_{i}_{s}' in scores] for i in IDS};record={'omitted_seed':omitted,'complete':all(len(v)==2 for v in subset.values())}
    if record['complete']:
     sub=predictions(subset,p);chosen,_=choose(sub,p,'ei');a,b=set(ids),set(chosen);record.update(selected_ids=chosen,jaccard=len(a&b)/len(a|b),common_configurations=len(a&b))
    r['leave_one_seed_out'].append(record)
  rows.append(r)
 result={'scope':'Post-hoc descriptive sample stability; no added model requests, target acquisitions, quality threshold or replacement primary policy','cases':rows,'invalid_responses':invalid};write(ROOT/'results/v124_analysis/sample_stability.json',result)
 lines=['# V124 post-hoc sample and format diagnostics','','This analysis uses only real responses and acquired prefix labels. It adds no objective evaluations and changes no declared choices or primary result. Removing one sampling seed is a descriptive stability check, not a confidence interval or a new optimization arm. Missing two-sample candidate sets remain unavailable.','','| Family | Candidates with3valid samples /20 | Identical valid samples | Accepted family |','|---|---:|---:|---|']
 for r in rows:lines.append(f"| {r['system_group']} | {r['three_valid_candidates']} | {r['identical_samples_candidates']} | {r['accepted_family']} |")
 lines+=['','EI selection overlap with the original10choices after omitting one sampling seed:']
 for r in rows:
  values=[f"seed{x['omitted_seed']}: {x.get('common_configurations','unavailable')}/10" for x in r['leave_one_seed_out']];lines.append(f"- {r['system_group']}: "+('; '.join(values) if values else 'family fallback; no LLM ranking evaluated'))
 lines+=['',f"Invalid returned scalar responses: {len(invalid)}. Exact texts, finish reasons and token counts are in results/v124_analysis/sample_stability.json. Placeholder echoes are retained failures, not repaired predictions. All original responses remain in the source journal. Three stochastic samples per candidate cannot establish calibrated uncertainty. Sampling-derived features also require model calls, so they are not cheap pre-escalation controller inputs."]
 (ROOT/'reports/sample_stability_v124.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'cases':rows,'invalid_returned':len(invalid)},indent=2))
if __name__=='__main__':main()
