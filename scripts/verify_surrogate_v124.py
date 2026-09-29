"""Saved-evidence replay: requests, raw acquired prompt values and source cells."""
import json,csv,math
from collect_smollm_v47 import ROOT,read,write,sha
from analyze_surrogate_v124 import frozen,make_choices,candidates,references,OUT
from surrogate_v124 import messages,payload,SEEDS,IDS
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain

def main():
 frozen();jobs=read(ROOT/'artifacts/study_v124/jobs.json');jm={j['key']:j for j in jobs};starts=[json.loads(x) for x in (ROOT/'results/v124_surrogate/generation_starts.jsonl').read_text().splitlines()];raw=[json.loads(x) for x in (ROOT/'results/v124_surrogate/responses.jsonl').read_text().splitlines()];ledger=read(ROOT/'results/v124_surrogate/ledger.json')
 assert len(starts)==ledger['generation_requests']<=180 and len(raw)<=len(starts) and len({r['key'] for r in raw})==len(raw);assert ledger['allocated_output_tokens']==32*len(starts)<=5760 and ledger['retries']==ledger['external_spend_usd']==0;assert ledger['peak_server_rss_bytes']<=8589934592 and ledger['stage_seconds']<=1500 and ledger['server_exit_code']==0
 assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]];sm={s['identity']:s for s in starts}
 for n,h in read(ROOT/'results/v124_surrogate/preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h
 for s in starts:
  j=jm[s['identity']];p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);pre=read(ROOT/f"results/v124_surrogate/preflight/{j['key']}.json");assert pre['messages']==read(ROOT/j['messages_path'])==messages(p,j['candidate_id'],spec['meaning']);assert s['payload']==payload(pre['rendered']['prompt'],j['sampling_seed']);assert len(pre['prompt_tokens'])+32<=4096
  body=json.loads(pre['messages'][1]['content']);assert body['new_configuration']==list(c.x[p['pool']['mapping'][j['candidate_id']]])
  import numpy as np
  order=np.random.RandomState(0).permutation(10)
  assert body['observed_examples']==[{'settings':list(c.x[p['state']['ids'][int(i)]]),'performance':f"{p['state']['labels'][int(i)][0]:.6f}"} for i in order]
 for r in raw:
  p=sm[r['key']]['payload'];assert r['response']['prompt']==p['prompt']
  for k in ['seed','n_predict','temperature','repeat_penalty','top_p','top_k','min_p']:
   actual=r['response']['generation_settings'][k];assert math.isclose(actual,p[k],rel_tol=0,abs_tol=1e-6) if type(p[k]) is float else actual==p[k],(r['key'],k)
  assert not r['response']['generation_settings'].get('grammar')
 choices,d=make_choices();assert d==read(OUT/'diagnostics.json')
 for n,h in read(OUT/'selection_seal.json')['sha256'].items():assert sha(ROOT/n)==h
 summary=read(OUT/'summary.json');assert summary['complete'] and len(summary['cases'])==6 and summary['actual_new_acquisitions']==60;events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==60
 for choice in choices:
  assert choice==read(OUT/'choices'/f"{choice['key']}.json");p=read(ROOT/choice['prefix']);spec,c=candidates(choice['dataset']);state=State(**p['state']).clone();source=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([source[0]],delimiter=spec['delimiter']));es=[e for e in events if e['key']==choice['key']];assert [e['row_id'] for e in es]==choice['selected_rows']
  for e in es:
   assert e['source_line']==c.source_ids[e['row_id']];row=dict(zip(header,next(csv.reader([source[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];assert tuple(float(row[n]) for n in c.names)==c.x[e['row_id']];state.observe(e['row_id'],[float(e['raw_target'])],c.directions)
  arm=read(OUT/'arms'/f"{choice['key']}.json");assert state.record()==arm['state'] and len(set(state.ids))==20 and best(state,spec['direction'])==arm['target'];refs=references({**choice,'key':choice['base_key']},p,spec['direction']);assert refs==arm['references'] and arm['gains']=={m:relative_gain(v,arm['target'],spec['direction']) for m,v in refs.items()}
 result={'verified':True,'requests_replayed':len(starts),'responses':len(raw),'source_events_replayed':60,'paired_arms':6,'independent_families':3,'new_acquisitions':0,'new_inference':0};write(ROOT/'artifacts/study_v124/verification.json',result);print(result)
if __name__=='__main__':main()
