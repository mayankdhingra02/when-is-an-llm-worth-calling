"""Explicitly optimistic validation-minimum sensitivity, never the primary reference."""
import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'results/v165_headroom'
def main():
 d=json.loads((O/'comparison.json').read_text());rows=[];summary=[]
 for x in d['targets']:
  if x['kind']!='prefix':continue
  best=min((v for v in d['validation_cells'] if v['engine']==x['engine'] and v['valid']),key=lambda v:(v['median'],v['row_id']));rows.append({'case':x['case'],'engine':x['engine'],'checkpoint':x['checkpoint'],'prefix_id':x['row_id'],'validation_minimum_id':best['row_id'],'optimistic_observed_headroom':(x['validation_median']-best['median'])/x['validation_median']})
 for e in ['ripgrep','hnswlib']:
  for k in [4,7,10]:
   rr=[r['optimistic_observed_headroom'] for r in rows if r['engine']==e and r['checkpoint']==k];summary.append({'engine':e,'checkpoint':k,'mean':statistics.mean(rr),'maximum':max(rr),'minimum':min(rr),'descriptive_above_ten_percent':sum(v>.1 for v in rr)})
 out={'scope':'Post-hoc sensitivity using validation to select and score its minimum. Optimistically biased descriptive finite-sample comparison, not independent validation, a deployable policy, or a true-optimum bound. Primary selected-reference analysis unchanged.','rows':rows,'summary':summary};(O/'posthoc_validation_minimum.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
