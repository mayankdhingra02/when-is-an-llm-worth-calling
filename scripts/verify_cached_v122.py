"""Source-cell and projection replay; no new acquisitions or inference."""
import csv,json
from table_check_v119 import ROOT,read,write,sha,candidates,MODES
from project_cached_v122 import project,frozen
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain

def main():
 frozen();s=read(ROOT/'results/v122_analysis/summary.json');assert s['complete'] and len(s['cases'])==5 and s['actual_new_acquisitions']==50 and s['new_model_requests']==0
 spec,c,_=candidates();responses={r['case']:r for r in [json.loads(x) for x in (ROOT/'results/v119_reasoning/responses.jsonl').read_text().splitlines()]};events=[json.loads(x) for x in (ROOT/'results/v122_analysis/acquisitions.jsonl').read_text().splitlines()];source=__import__('pathlib').Path(spec['path']).read_text().splitlines();header=next(csv.reader([source[0]]));assert len(events)==50
 seal=read(ROOT/'results/v122_projection/selection_seal.json')
 for n,h in seal['sha256'].items():assert sha(ROOT/n)==h
 for r in s['cases']:
  p=read(ROOT/r['prefix']);ids,trace=project(responses[r['key']]['response']['content'],c,p);assert ids==r['selected_rows'] and trace==r['trace'];state=State(**p['state']).clone();es=[e for e in events if e['key']==r['key']];assert [e['row_id'] for e in es]==ids
  for e in es:
   assert e['source_line']==c.source_ids[e['row_id']];value=dict(zip(header,next(csv.reader([source[e['source_line']-1]]))))['latency'];assert value==e['raw_target'];state.observe(e['row_id'],[float(value)],('-',))
  assert state.record()==r['state'] and len(set(state.ids))==20 and best(state,'-')==r['target']
  for m,v in r['references'].items():
   ref=read(ROOT/(f"results/v120_analysis/arms/{r['key']}.json" if m=='presentation_first10' else f"results/v119_classical/arms/{r['key']}_{m}.json"));assert best(State(**ref['state']),'-')==v and relative_gain(v,r['target'],'-')==r['gains'][m]
 result={'verified':True,'cases':5,'source_events_replayed':50,'new_acquisitions':0,'new_model_requests':0};write(ROOT/'artifacts/study_v122/verification.json',result);print(result)
if __name__=='__main__':main()
