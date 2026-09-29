"""Post-hoc descriptive ID-order diagnostic; no new labels/inference/policy tuning."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines
from escalation.study_v8 import manifest,verify,run_config
from escalation.resources import Resources

def main():
    verify();m=manifest();responses=lines('results/v8/requests.jsonl');cases=[]
    for d in m['datasets']:
        for seed in m['seeds']:
            path=Path('results/v8/llm')/(d['id']+'_'+str(seed)+'.json')
            if not path.exists():continue
            r=read(path);q=next(q for q in responses if q['request_id']==r['request_id'])
            first_ids=list(r['pool']['mapping'])[:10];first_rows=[r['pool']['mapping'][i] for i in first_ids]
            selected=q['raw_output'].strip().splitlines() if q.get('raw_output') else None
            cases.append({'dataset':d['id'],'seed':seed,'request_id':q['request_id'],'status':r['status'],
              'selected_ids':selected,'first_displayed_ids':first_ids,'exact_display_order_match':selected==first_ids,
              'first_half_rows_equal_actual_model_acquisitions':r['state']['ids'][10:]==first_rows})
    result={'scope':'post-hoc descriptive diagnostic; not an additional randomized experiment or measured model-free arm',
      'intended_cases':15,'observed_cases':len(cases),'exact_first_ten_display_order_matches':sum(c['exact_display_order_match'] for c in cases),
      'row_sequence_matches':sum(c['first_half_rows_equal_actual_model_acquisitions'] for c in cases),'cases':cases,
      'new_model_requests':0,'new_objective_acquisitions':0,
      'interpretation':'Every matching response is reproducible by taking the first ten displayed IDs. Since presentation is shuffled, this observed rule has the design distribution of a random ten-row subset. The run does not demonstrate learned ranking. This diagnosis does not establish behavior under untested prompts or reorderings.'}
    write('results/v8/selection_diagnostics.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:r.check();main();r.check()
